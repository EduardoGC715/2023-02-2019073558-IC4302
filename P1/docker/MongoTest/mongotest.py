from flask import Flask, request, render_template_string
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)

documents = [
    {
        "PageId": 2,
        "PageTitle": "Sample Page 2",
        "PageNamespace": "Sample Namespace",
        "PageRedirect": "Redirected Page",
        "PageHasRedirect": True,
        "PageRestrictions": ["Restriction A", "Restriction B"],
        "PageLastModified": "2023-09-23",
        "PageLastModifiedUser": "John Doe",
        "PageBytes": 200,
        "PageText": "Sample content for Page 2",
        "PageWikipediaLink": "https://en.wikipedia.org/sample_page_2",
        "pageWikipediaGenerated": "https://en.wikipedia.org/sample_page_2/generated",
        "PageLinks": ["Link 1", "Link 2", "Link 3"],
        "PageNumberLinks": 3,
        "SiteInfoName": "Sample Site",
        "SiteInfoDBName": "sample_db",
        "SiteLanguage": "English"
    },
    {
        "PageId": 3,
        "PageTitle": "Sample Page 3",
        "PageNamespace": "Sample Namespace",
        "PageRedirect": "Redirected Page",
        "PageHasRedirect": False,
        "PageRestrictions": ["Restriction C", "Restriction D"],
        "PageLastModified": "2023-09-24",
        "PageLastModifiedUser": "Jane Doe",
        "PageBytes": 300,
        "PageText": "Sample content for Page 3",
        "PageWikipediaLink": "https://en.wikipedia.org/sample_page_3",
        "pageWikipediaGenerated": "https://en.wikipedia.org/sample_page_3/generated",
        "PageLinks": ["Link A", "Link B", "Link C"],
        "PageNumberLinks": 3,
        "SiteInfoName": "Sample Site",
        "SiteInfoDBName": "sample_db",
        "SiteLanguage": "English"
    },
    # Add more documents as needed
]

def mongoDBConnection (): 
    try:
        app.config["MONGO_URI"] = "mongodb+srv://eduardogc715:BasesII2023@bibliotec.6l341ym.mongodb.net/bibliotec"
        mongo = PyMongo(app)
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
    
@app.route("/")
def home():
    return render_template_string('''<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="css url"/>
    </head>
    <body>
        <p>Aplicación de Mongo!</p>
    </body>
</html>
''')

def searchQuery(searchQuery):
    pipeline = [
  {
    "$searchMeta": {
      "index": "mainIndex",
      "facet": {
        "operator": {
          "compound": {
            "must": [
              {
                "text": {
                  "query": "wikipedia",
                  "path": {
                    "wildcard": "*"
                  }
                }
              }
            ]
          }
        },
        "facets": {
          "PageNamespaceFacet": {
            "type": "string",
            "path": "PageNamespace"
          },
          "PageBytesFacet": {
            "type": "number",
            "path": "PageBytes",
            "boundaries": [0, 1000, 5000, 10000]
          },
          "PageHasRedirectFacet": {
            "type": "string",
            "path": "PageHasRedirect"
          },
          "PageRestrictionsFacet": {
            "type": "string",
            "path": "PageRestrictions"
          },
          "SiteInfoNameFacet": {
            "type": "string",
            "path": "SiteInfoName"
          },
          "SiteInfoDBNameFacet": {
            "type": "string",
            "path": "SiteInfoDBName"
          },
          "SiteLanguageFacet": {
            "type": "string",
            "path": "SiteLanguage"
          },
          "PageLastModifiedFacet": {
            "type": "date",
            "path": "PageLastModified",
            "boundaries": [
              datetime(2023, 9, 1),
              datetime(2023, 9, 18)
            ]
          },
          "PageLastModifiedUserFacet": {
            "type": "string",
            "path": "PageLastModifiedUser"
          },
          "PageNumberLinksFacet": {
            "type": "number",
            "path": "PageNumberLinks",
            "boundaries": [0, 10, 20]
          },
        }
      }
    }
  }
]
    return pipeline

if __name__ == "__main__":
    mongo = mongoDBConnection()
    print(searchQuery("Doe"))
    results = list(mongo.db.pages.aggregate(searchQuery("Doe")))
    print(results)
    for i, item in enumerate(results, 1):
        print(f"Item {i}: {item}")
    #app.run()