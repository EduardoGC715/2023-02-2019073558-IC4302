import requests
import pika
import os
import json

def get_biorxiv_data(query=None):
    base_url = 'https://api.biorxiv.org'
    endpoint = '/covid19/0'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(base_url + endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def callback(ch, method, properties, body):
    json_object = json.loads(body)
    print(f"Received {json_object}")


RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
SPACY_QUEUE=os.getenv('SPACY_QUEUE')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=SPACY_QUEUE, durable = True)
channel.basic_consume(queue=SPACY_QUEUE, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

