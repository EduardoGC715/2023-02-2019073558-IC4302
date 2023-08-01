import time
import os
import sys
import pika
from datetime import datetime
import hashlib
import json

hostname = os.getenv('HOSTNAME')
interval = int(os.getenv('EVENT_INTERVAL'))
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
OUTPUT_QUEUE=os.getenv('OUTPUT_QUEUE')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=OUTPUT_QUEUE)

while True:
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    msg = "{\"data\": [ {\"msg\":\""+result+"\", \"hostname\": \""+hostname+"\"}]}"
    channel.basic_publish(exchange='', routing_key=OUTPUT_QUEUE, body=msg)
    print(result)
    time.sleep(interval)

connection.close()





