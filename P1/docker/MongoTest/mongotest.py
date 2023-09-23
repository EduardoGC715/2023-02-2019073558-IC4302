from flask import Flask, request, render_template_string
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)

documents = [
    {
        "PageId": 4,
        "PageTitle": "Special Page 4",
        "PageNamespace": "Unique Namespace",
        "PageRedirect": "Custom Redirect",
        "PageHasRedirect": True,
        "PageRestrictions": ["Restriction E", "Restriction F"],
        "PageLastModified": "2023-09-26",
        "PageLastModifiedUser": "Alice Smith",
        "PageBytes": 400,
        "PageText": "Special content for Page 4",
        "PageWikipediaLink": "https://en.wikipedia.org/special_page_4",
        "pageWikipediaGenerated": "https://en.wikipedia.org/special_page_4/generated",
        "PageLinks": ["Linkingpark", "Link Y", "Link Z"],
        "PageNumberLinks": 6,
        "SiteInfoName": "Unique Site",
        "SiteInfoDBName": "unique_db",
        "SiteLanguage": "German"
    },
    {
        "PageId": 5,
        "PageTitle": "Extraordinary Page 5",
        "PageNamespace": "Unique Namespace",
        "PageRedirect": "Custom Redirect",
        "PageHasRedirect": False,
        "PageRestrictions": ["Restriction G", "Restriction H"],
        "PageLastModified": "2023-09-27",
        "PageLastModifiedUser": "Bob Johnson",
        "PageBytes": 500,
        "PageText": "Extraordinary content for Page 5",
        "PageWikipediaLink": "https://en.wikipedia.org/extraordinary_page_5",
        "pageWikipediaGenerated": "https://en.wikipedia.org/extraordinary_page_5/generated",
        "PageLinks": ["Link P", "Link Q", "Link R"],
        "PageNumberLinks": 7,
        "SiteInfoName": "Unique Site",
        "SiteInfoDBName": "unique_db",
        "SiteLanguage": "Spanish"
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

def textSearchQuery(searchQuery):
    pipeline = [
  {
    "$search": {
      "index": "mainIndex",
      "facet": {
        "operator": {
          "compound": {
            "must": [
              {
                "text": {
                  "query": searchQuery,
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
    results = list(mongo.db.pages.aggregate(textSearchQuery("Doe")))
    print(results)
    for i, item in enumerate(results, 1):
        print(f"Item {i}: {item}")
    #app.run()