from pymongo import MongoClient

def mongoDBConnection (): 
    try:
        mongo = MongoClient("mongodb+srv://eduardogc715:BasesII2023@bibliotec.6l341ym.mongodb.net/bibliotec")
        return mongo
    except Exception as e:
        print(f"An error occurred: {e}")

def addDocuments(documents, mongo):
    try:
        db = mongo.db  # Get the database object
        result = db["pages"].insert_many(documents)
        return result.inserted_ids
    except Exception as e:
        raise e
    
def updateDocumentsLinks(query, mongo):
    try:
        db = mongo.db  # Get the database object
        result = db["pages"].insert_many(query)
        return result.inserted_ids
    except Exception as e:
        raise e
    
# Cada documento tiene la soguiente estructura:
"""{
      "PageBytes": int
      "PageHasRedirect": "True" | "False", strings dependiendo del valor
      "PageId": int
      "PageLastModified": ISO format Date
      "PageLastModifiedUser": "string"
      "PageLinks": lista con los links, ["string"]
      "PageNamespace": "string"
      "PageNumberLinks": int
      "PageRedirect": "string"
      "PageRestrictions": lista con las restricciones, ["string"]
      "PageText": "string"
      "PageTitle": "string"
      "PageWikipediaLink": "string"
      "SiteInfoDBName": "string"
      "SiteInfoName": "string"
      "SiteLanguage": "string"
      "pageWikipediaGenerated": "string"
    }"""