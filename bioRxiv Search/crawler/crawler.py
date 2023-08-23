import requests
import pika
import os
import json
import time
from elasticsearch import Elasticsearch
# Página usada como referencia para el código de elasticsearch: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html

# Función que extrae datos desde el API de bioRxiv.
# Recibe el número de documento a partir va a descargar los 30 artículos
# Código basado en: https://requests.readthedocs.io/en/latest/user/quickstart/
def get_biorxiv_data(offset=None):
    base_url = 'https://api.biorxiv.org'
    endpoint = '/covid19/'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(base_url + endpoint + str(offset), headers=headers)
    print(base_url + endpoint + str(offset))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Función que se va a ejecutar cada vez que recibe un mensaje de la cola
# de CRAWLER_QUEUE en RabbitMQ
def callback(ch, method, properties, body):
    json_object = json.loads(body)
    print(f"Received {json_object}")
    jobId = json_object["jobId"]
    pageSize = int(json_object["pageSize"])
    splitNumber = int(json_object["splitNumber"])

    articles = []
    articleNumber = pageSize * splitNumber # se calcula el árticulo del cual a partir se va a empezar a descargar los 
    count = 0
    # se van descargando la cantidad de artículos en el pageSize
    while(count < pageSize):
        data = get_biorxiv_data(articleNumber + count)
        articlesDownloaded = min(len(data["collection"]), pageSize - count)
        articles += data["collection"][:articlesDownloaded]
        count += articlesDownloaded

    # se prepara el documento para enviarlo al SPACY_QUEUE
    json_object["status"] = 'DOWNLOADED'
    documentId = jobId + str(splitNumber)

    # Se alista el documento para subirlo al índice en elasticsearch.
    articlesJson = {"splitId": documentId, "articles" : articles}
    print(splitNumber, len(articles))
    resp = client.index(index=ESINDEX, id=documentId, document=json.dumps(articlesJson))

    # se publica el mensaje al SPACY_QUEUE
    channel.basic_publish(exchange='', routing_key=SPACY_QUEUE, body=json.dumps(json_object))
    time.sleep(int(json_object["sleep"])/1000)

# Configuración de RabbitMQ
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
CRAWLER_QUEUE=os.getenv('CRAWLER_QUEUE')
SPACY_QUEUE=os.getenv('SPACY_QUEUE')

# Configuración de Elasticsearch
ESENDPOINT=os.getenv('ESENDPOINT')
ESPASSWORD=os.getenv('ESPASSWORD')
ESINDEX=os.getenv('ESINDEX')

# Conexión con RabbitMQ
# Código usado de referencia: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=CRAWLER_QUEUE, durable = True) # cola que recibe mensajes
channel.queue_declare(queue=SPACY_QUEUE, durable = True) # cola que envía mensajes al Spacy Entity Extractor
channel.basic_consume(queue=CRAWLER_QUEUE, on_message_callback=callback, auto_ack=True)

client = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)

channel.start_consuming()

