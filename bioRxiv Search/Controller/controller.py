import requests
import pika
import os
import json
import math

def get_biorxiv_data():
    base_url = 'https://api.biorxiv.org'
    endpoint = '/covid19/0'
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

# credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
# parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
parameters = pika.ConnectionParameters(host=RABBIT_MQ)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=CRAWLER_QUEUE, durable = True)

data = {
    "jobId": "1234",
    "pageSize": "100",
    "sleep": "2000"
}
jsonexample = json.dumps(data)

while True:
    # Revisa a que recibe el request del kibana service.
    jsonread = json.loads(jsonexample)
    pageSize = int(jsonread["pageSize"]) # extrae el page size del índice
    apiData = get_biorxiv_data()
    total = int(apiData["messages"][0]["total"])
    print(total)
    splits = math.ceil(total / pageSize)
    for split in range(splits):
        jsonread["splitNumber"] = split
        msg = json.dumps(jsonread)
        channel.basic_publish(exchange='', routing_key=CRAWLER_QUEUE, body=msg)
    break # para probar

connection.close()
