import requests
import pika
import os
import json
import math
import time
from elasticsearch import Elasticsearch
from elasticsearch import TransportError

# función que obtiene extrea datos del API de bioRxiv.
def get_biorxiv_data():
    base_url = 'https://api.biorxiv.org'
    endpoint = '/covid19/30'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(base_url + endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
# Parámetros de conexión con RabbitMQ
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
CRAWLER_QUEUE=os.getenv('CRAWLER_QUEUE')

# Parámetros de conexión a Elasticsearch
ESENDPOINT=os.getenv('ESENDPOINT')
ESPASSWORD=os.getenv('ESPASSWORD')
ESINDEX=os.getenv('ESINDEX')

# Conexión con RabbitMQ
credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=CRAWLER_QUEUE, durable = True) # Cola por la cual se mandan mensajes al crawler.

# Conexión con elasticsearch
client = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)

index_settings = {
    "mappings": {
        "properties": {
            "jobId": {
                "type": "keyword"
            },
            "pageSize": {
                "type": "integer"
            },
            "sleep": {
                "type": "integer"
            },
            "processed": {
                "type": "boolean"
            }
        }
    }
}

# Crea el índice de jobs, o el dado en ESINDEX
try:
    client.indices.create(index=ESINDEX)
    print(f"Index '{ESINDEX}' created successfully.")
except Exception as e:
    print(f"Index '{ESINDEX}' already exists.")

# loop donde el controller va a revisar el índice por mensajes no procesados.
while True:
    print("Checking...")
    # Revisa hasta que recibe el request del kibana service.
    try:
        # busca las entradas que no estén procesadas.
        response = client.search(index=ESINDEX, query = {"term": {
            "processed": False
        }})
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
        continue
    
    # si encontró algún documento
    if len(response['hits']['hits']) != 0:
        print("Found...")
        for hit in response['hits']['hits']:
            jsonread = hit['_source']
            pageSize = int(jsonread["pageSize"]) # extrae el page size del índice
            apiData = get_biorxiv_data()
            total = int(apiData["messages"][0]["total"]) # cantidad total de mensajes
            print(total)
            print(jsonread)

            splits = math.ceil(total / pageSize) # cantidad total de splits

            # Se procesan los splits para publicarlos en la cola de RabbitMQ
            for split in range(splits):
                jsonread["splitNumber"] = split
                msg = json.dumps(jsonread)
                channel.basic_publish(exchange='', routing_key=CRAWLER_QUEUE, body=msg)
            jsonread['processed'] = True
            # Se actualiza el documento como procesado,
            client.update(index=ESINDEX, id=hit['_id'], doc= {'processed': True}, refresh = True)
    time.sleep(5)

connection.close()
