from flask import Flask, request, render_template_string
from flask_pymongo import PyMongo
import datetime as dt

app = Flask(__name__)

def mongoDBConnection (): 
    try:
        app.config["MONGO_URI"] = "mongodb+srv://eduardogc715:BasesII2023@bibliotec.6l341ym.mongodb.net/bibliotec"
        mongo = PyMongo(app)
        return mongo
    except Exception as e:
        print(f"An error occurred: {e}")

def isValidDate(dateStr):
    try:
        dt.datetime.strptime(dateStr, "%Y-%m-%d")
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
                        "must":[],
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
                            dt.datetime(2000, 1, 1, 0, 0, 0),
                            dt.datetime(2005, 1, 1, 0, 0, 0),
                            dt.datetime(2010, 1, 1, 0, 0, 0),
                            dt.datetime(2015, 1, 1, 0, 0, 0),
                            dt.datetime(2020, 1, 1, 0, 0, 0),
                            dt.datetime(2025, 1, 1, 0, 0, 0)
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
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageLastModified", "value": dt.datetime.strptime(searchQuery, "%Y-%m-%d")}}) 
    return pipeline

def filteredTextSearchQuery(searchQuery, PageLastModifiedUser="", PageNamespace="", SiteInfoName="", SiteInfoDBName="", SiteLanguage="", PageRestrictions="", PageBytes="", PageNumberLinks="", PageLastModified="", PageHasRedirect="" ):
    pipeline = textSearchQuery(searchQuery)
    if PageLastModifiedUser:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"text": {"path": "PageLastModifiedUser", "query": PageLastModifiedUser}})
    if PageNamespace:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"text": {"path": "PageNamespace", "query": PageNamespace}})
    if SiteInfoName:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"text": {"path": "SiteInfoName", "query": SiteInfoName}})
    if SiteInfoDBName:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"text": {"path": "SiteInfoDBName", "query": SiteInfoDBName}})
    if SiteLanguage:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"text": {"path": "SiteLanguage", "query": SiteLanguage}})
    if PageRestrictions:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"text": {"path": "PageRestrictions", "query": PageRestrictions}})
    if PageBytes:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"equals": {"path": "PageBytes", "value": int(PageBytes)}})
    if PageNumberLinks:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"equals": {"path": "PageNumberLinks", "value": int(PageNumberLinks)}})
    if PageLastModified:
        dateObj = dt.datetime.fromisoformat(PageLastModified)
        newDate = dateObj - dt.timedelta(days=365*5)
        newIsoDate = newDate.isoformat()
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"range": {"path": "PageLastModified", "lt": PageLastModified, "gt": newIsoDate}})
    if PageHasRedirect:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["must"].append({"text": {"path": "PageHasRedirect", "query": PageHasRedirect}})
    return pipeline

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

if __name__ == "__main__":
    mongo = mongoDBConnection()
    results = list(mongo.db.pages.aggregate(filteredTextSearchQuery("content", PageLastModifiedUser="\"John Doe\"")))[0]
    print(results)
    #app.run()