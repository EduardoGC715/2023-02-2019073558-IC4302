from elasticsearch import Elasticsearch
import pika
import os
import json
import spacy

def callback(ch, method, properties, body):
    json_object = json.loads(body)
    print(f"Received {json_object}")
    jobId = json_object["jobId"]
    splitNumber = int(json_object["splitNumber"])
    
    documentId = jobId + str(splitNumber)
    query = {
            "term": {
                "splitId": documentId
            }
        }
    response = es.search(index=ESINDEX, query=query, size=100)
    
    for hit in response["hits"]["hits"]:
        source_dict = hit["_source"]  
        
        # Procesar y agregar las entidades
        processed_document = process_and_augment_document(source_dict)
        
        # Actualizar el documento en Elasticsearch con el campo "augmented"
        es.index(index=AUGMENTEDINDEX, id=hit["_id"], body=processed_document)
        print(f"Processed and updated document {hit['_id']}")

def perform_ner(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    return entities

def process_and_augment_document(document):
    text_to_process = document.get("articles") 
    
    processed_text_dict = json.loads(text_to_process)

    entities = perform_ner(processed_text_dict["rel_abs"])

    document["augmented"] = {"entities": entities}
    
    return document


ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD = os.getenv('ESPASSWORD')
ESINDEX = os.getenv('ESINDEX')
AUGMENTEDINDEX = os.getenv('AUGMENTEDINDEX')

RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
SPACY_QUEUE=os.getenv('SPACY_QUEUE')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=SPACY_QUEUE, durable = True)
channel.basic_consume(queue=SPACY_QUEUE, on_message_callback=callback, auto_ack=True)

# Establish the Elasticsearch connection
es = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)

# Cargar el modelo de Spacy para NER
nlp = spacy.load("en_core_web_sm")

channel.start_consuming()