import requests
import pika
import os
import json
import math
import time
from elasticsearch import *

# Parámetros de conexión con RabbitMQ
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
CRAWLER_QUEUE=os.getenv('CRAWLER_QUEUE')

# Parámetros de conexión a Elasticsearch
ESENDPOINT=os.getenv('ESENDPOINT')
ESPASSWORD=os.getenv('ESPASSWORD')
ESINDEX=os.getenv('ESINDEX')

# Elasticsearch CLient
elasticClient = None

# Definicion del API URL
base_url = 'https://api.biorxiv.org'
endpoint = '/covid19/30'
headers = {'Content-Type': 'application/json'}

# API Biorxiv Response Code
success = 200

# RabbitMQ Connection Variables
credentials = None
parameters = None
rabbitMQConnection = None
channel = None

# Create Elasticsearch connection
def createElasticsearchConnection():

    # Init Elasticsearch connection
    elasticClient = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)

    # Crea el índice de jobs, o el dado en ESINDEX
    try:
        elasticClient.indices.create(index=ESINDEX)
        print(f"Index '{ESINDEX}' created successfully.")
    except Exception as e:
        print(f"Index '{ESINDEX}' already exists.")

# Close Elasticsearch connection
def closeElasticsearchConnection():
    rabbitMQConnection.close()

# Create RabbitMQ Connection
def createRabbitMQConnection():
    credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
    rabbitMQConnection = pika.BlockingConnection(parameters)
    channel = rabbitMQConnection.channel()
    channel.queue_declare(queue=CRAWLER_QUEUE, durable = True) # Cola por la cual se mandan mensajes al crawler.

# función que obtiene extrea datos del API de bioRxiv.
def get_biorxiv_data():

    response = requests.get(base_url + endpoint, headers=headers)

    if response.status_code != success:
        print(f"Error: {response.status_code} - {response.text}")
        return None
        
    return response.json()

def main():

    # Init Elasticsearch connection
    createElasticsearchConnection()

    # Init RabbitMQ connection
    createRabbitMQConnection()

    # loop donde el controller va a revisar el índice por mensajes no procesados.
    while True:

        print("Checking...")

        # Revisa hasta que recibe el request del kibana service.
        try:
            # busca las entradas que no estén procesadas.
            response = elasticClient.search(index=ESINDEX, query = {"term": {
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
                apiData = get_biorxiv_data() #Aqui el codigo se cae.....
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
                elasticClient.update(index=ESINDEX, id=hit['_id'], doc= {'processed': True}, refresh = True)
        time.sleep(5)

    # Close RabbitMQ Connection
    closeElasticsearchConnection()

if __name__ == '__main__':
    main()