from flask import Flask, request, render_template_string
from flask_pymongo import PyMongo
from datetime import datetime
import json

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

def isValidDate(dateStr):
    try:
        datetime.strptime(dateStr, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def textSearchQuery(searchQuery):
    pipeline = [
    {
        '$search': {
            'index': 'mainIndex', 
            'facet': {
                'operator': {
                    "compound": {
                        "should": [
                            {
                                "text":{
                                    "path":{
                                        "wildcard": "*"
                                    },
                                    "query": str(searchQuery)
                                }
                            },
                        ],
                        "minimumShouldMatch": 1
                    }
                }, 
                'facets': {
                    'PageLastModifiedUserFacet': {
                        'type': 'string', 
                        'path': 'PageLastModifiedUser'
                    }, 
                    'PageNamespaceFacet': {
                        'type': 'string', 
                        'path': 'PageNamespace'
                    }, 
                    'SiteInfoNameFacet': {
                        'type': 'string', 
                        'path': 'SiteInfoName'
                    }, 
                    'SiteInfoDBNameFacet': {
                        'type': 'string', 
                        'path': 'SiteInfoDBName'
                    }, 
                    'SiteLanguageFacet': {
                        'type': 'string', 
                        'path': 'SiteLanguage'
                    }, 
                    'PageRestrictionsFacet': {
                        'type': 'string', 
                        'path': 'PageRestrictions'
                    },
                      'PageBytesFacet': {
                        'type': 'number', 
                        'path': 'PageBytes',
                        'boundaries': [0, 1000, 10000, 20000, 30000, 40000, 50000]
                    }, 
                      'PageNumberLinksFacet': {
                        'type': 'number', 
                        'path': 'PageNumberLinks',
                        'boundaries': [1, 2, 3, 4, 5]
                    },
                      "PageLastModifiedFacet": {
                        "type": "date",
                        "path": "PageLastModified",
                        "boundaries": [ 
                            datetime(2000, 1, 1, 0, 0, 0),
                            datetime(2005, 1, 1, 0, 0, 0),
                            datetime(2010, 1, 1, 0, 0, 0),
                            datetime(2015, 1, 1, 0, 0, 0),
                            datetime(2020, 1, 1, 0, 0, 0),
                            datetime(2025, 1, 1, 0, 0, 0)
                        ]
                    }, 
                      'PageHasRedirectFacet': {
                        'type': 'string', 
                        'path': 'PageHasRedirect',
                    }
                }
            }, 
            'highlight': {
                'path': {
                    'wildcard': '*'
                }
            }
        }
    }, {
        '$facet': {
            'docs': [], 
            'facets': [
                {
                    '$replaceWith': '$$SEARCH_META'
                }, {
                    '$limit': 1
                }
            ], 
            'highlights': [
                {
                    '$project': {
                        'highlights': {
                            '$meta': 'searchHighlights'
                        }
                    }
                }
            ]
        }
    }
]   
    if searchQuery.isnumeric():
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageBytes", "value": int(searchQuery)}})
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageId", "value": int(searchQuery)}})
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageNumberLinks", "value": int(searchQuery)}})
    elif isValidDate(searchQuery):
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageLastModified", "value": datetime.strptime(searchQuery, "%Y-%m-%d")}}) 
    return pipeline

def pretty_print_dict(d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            print('  ' * indent + f'{key}:')
            pretty_print_dict(value, indent + 1)
        else:
            print('  ' * indent + f'{key}: {value}')

if __name__ == "__main__":
    mongo = mongoDBConnection()
    results = list(mongo.db.pages.aggregate(textSearchQuery("Sample")))[0]
    for highlight in results["highlights"]:
      pretty_print_dict(highlight)
    #app.run()