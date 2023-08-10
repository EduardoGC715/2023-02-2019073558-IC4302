import requests
import pika
import os
import json
import math
import time
from elasticsearch import Elasticsearch

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
    
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
CRAWLER_QUEUE=os.getenv('CRAWLER_QUEUE')

ESENDPOINT=os.getenv('ESENDPOINT')
ESPASSWORD=os.getenv('ESPASSWORD')
ESINDEX=os.getenv('ESINDEX')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=CRAWLER_QUEUE, durable = True)

data = {
    "jobId": "1234",
    "pageSize": "100",
    "sleep": "2000"
}
jsonexample = json.dumps(data)

client = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)

search_body = {
    "size": 1
}

while True:
    # Revisa a que recibe el request del kibana service.
    jsonread = client.search(index="jobs", body = search_body)

    pageSize = int(jsonread["pageSize"]) # extrae el page size del índice
    apiData = get_biorxiv_data()
    total = int(apiData["messages"][0]["total"])
    print(total)
    print(jsonread)

    splits = math.ceil(total / pageSize)
    for split in range(splits):
        jsonread["splitNumber"] = split
        msg = json.dumps(jsonread)
        channel.basic_publish(exchange='', routing_key=CRAWLER_QUEUE, body=msg)
    break # para probar

connection.close()
