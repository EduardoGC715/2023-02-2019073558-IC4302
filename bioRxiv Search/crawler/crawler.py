import requests
import pika
import os
import json
from elasticsearch import Elasticsearch

def get_biorxiv_data(offset=None):
    base_url = 'https://api.biorxiv.org'
    endpoint = '/covid19/'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(base_url + endpoint + str(offset), headers=headers)
    print(base_url + endpoint + str(offset))
    #print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def callback(ch, method, properties, body):
    json_object = json.loads(body)
    print(f"Received {json_object}")
    jobId = json_object["jobId"]
    pageSize = int(json_object["pageSize"])
    splitNumber = int(json_object["splitNumber"])
    articles = []
    articleNumber = pageSize * splitNumber
    count = 0
    while(count < pageSize):
        data = get_biorxiv_data(articleNumber + count)
        articlesDownloaded = min(len(data["collection"]), pageSize - count)
        articles += data["collection"][:articlesDownloaded]
        count += articlesDownloaded

    json_object["status"] = 'DOWNLOADED'
    documentId = jobId + str(splitNumber)
    articlesJson = {documentId: articles}
    channel.basic_publish(exchange='', routing_key=SPACY_QUEUE, body=json.dumps(json_object))
    print(splitNumber, len(articles))
    resp = client.index(index=ESINDEX, id=documentId, document=json.dumps(articlesJson))


RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
CRAWLER_QUEUE=os.getenv('CRAWLER_QUEUE')
SPACY_QUEUE=os.getenv('SPACY_QUEUE')

ESENDPOINT=os.getenv('ESENDPOINT')
ESPASSWORD=os.getenv('ESPASSWORD')
ESINDEX=os.getenv('ESINDEX')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=CRAWLER_QUEUE, durable = True)
channel.queue_declare(queue=SPACY_QUEUE, durable = True)
channel.basic_consume(queue=CRAWLER_QUEUE, on_message_callback=callback, auto_ack=True)

client = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)

channel.start_consuming()

