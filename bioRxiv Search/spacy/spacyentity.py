from elasticsearch import Elasticsearch
from collections import defaultdict
import pika
import os
import json
import spacy
import time
# Página usada como referencia para el código de elasticsearch: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html

def callback(ch, method, properties, body):
    json_object = json.loads(body)
    print(f"Received {json_object}")
    jobId = json_object["jobId"]
    splitNumber = int(json_object["splitNumber"])
    
    documentId = jobId + str(splitNumber)
    response = es.search(index=ESINDEX, query={"term":  { "splitId": documentId }})
    print("DocumentId:", documentId, "Response:", response)

    # Para la extracción e inserción de dato en elasticsearch utilizamos como referencia https://www.elastic.co/guide/en/cloud/current/ec-getting-started-python.html
    for hit in response["hits"]["hits"]:
        source_dict = hit["_source"]  
        print("Unprocessed:", source_dict)
        articles = source_dict.get("articles")
        for article in articles:
            # Procesar y agregar las entidades
            process_and_augment_document(article)
        print("Processed:", source_dict)
        # Actualizar el documento en Elasticsearch con el campo "augmented"
        es.index(index=AUGMENTEDINDEX, id=hit["_id"], document=json.dumps(source_dict, default=set_encoder))
        print(f"Processed and updated document {hit['_id']}\n")
    time.sleep(int(json_object["sleep"])/1000)

def set_encoder(obj):
    # Asegurarse de que el tipo de dato que se este insertando a elasticsearch sea el debido
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def ner_institutions(institutions, author):

    doc = nlp(institutions)
    ents = defaultdict(set)
    if len(doc.ents) != 0:
        x=0
        for e in doc.ents:
          author["institutions"][e.label_+"_"+str(x)] = e.text
          x+= 1
    else:
      author["institutions"]["ORG_0"] = institutions
    return dict(ents)
  
def perform_ner(text):
    # Para la implementación de NER con spacy utilizamos como referencia https://spacy.io/usage/linguistic-features 
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    return entities

def process_and_augment_document(article):

    entities = perform_ner(article["rel_abs"])
    for author in article['rel_authors']: 
        if not (author["author_inst"]):
            author["author_inst"] = "No Institution"
        if not (author["author_name"]):
            author["author_name"]= "No Author"
        author["institutions"] = {}
        ner_institutions(author['author_inst'], author)
        author["institutions"] = json.dumps(author["institutions"]).replace('"', "'")

    article["entities"] = entities  



ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD = os.getenv('ESPASSWORD')
ESINDEX = os.getenv('ESINDEX')
AUGMENTEDINDEX = os.getenv('AUGMENTEDINDEX')

RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
SPACY_QUEUE=os.getenv('SPACY_QUEUE')

# Conexión con RabbitMQ
# Código usado de referencia: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
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
print(ESINDEX)
channel.start_consuming()