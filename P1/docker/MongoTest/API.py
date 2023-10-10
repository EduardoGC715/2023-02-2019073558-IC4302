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
                        "filter":[],
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
                        'boundaries': [0, 3000, 60000, 90000, 120000, 150000, 180000, 210000, 240000, 270000, 300000],
                        "default": "+300000"
                    }, 
                      'PageNumberLinksFacet': {
                        'type': 'number', 
                        'path': 'PageNumberLinks',
                        'boundaries': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
                        "default": "+50"
                    },
                      "PageLastModifiedFacet": {
                        "type": "date",
                        "path": "PageLastModified",
                        "boundaries": [ 
                            dt.datetime(2023, 1, 1, 0, 0, 0),
                            dt.datetime(2023, 2, 1, 0, 0, 0),
                            dt.datetime(2023, 3, 1, 0, 0, 0),
                            dt.datetime(2023, 4, 1, 0, 0, 0),
                            dt.datetime(2023, 5, 1, 0, 0, 0),
                            dt.datetime(2023, 6, 1, 0, 0, 0),
                            dt.datetime(2023, 7, 1, 0, 0, 0),
                            dt.datetime(2023, 8, 1, 0, 0, 0),
                            dt.datetime(2023, 9, 1, 0, 0, 0),
                            dt.datetime(2023, 10, 1, 0, 0, 0),
                            dt.datetime(2023, 11, 1, 0, 0, 0),
                            dt.datetime(2023, 12, 1, 0, 0, 0)
                        ],
                        "default": "Older"
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
                },
                "maxNumPassages": 1
            }
        }
    }, {
        '$facet': {
            'docs': [
                { 
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "PageBytes": 1,
                        "PageHasRedirect": 1,
                        "PageId": 1,
                        "PageLastModified": 1,
                        "PageLastModifiedUser": 1,
                        "PageLinks": 1,
                        "PageNamespace": 1,
                        "PageNumberLinks": 1,
                        "PageRedirect": 1,
                        "PageRestrictions": 1,
                        "PageText": 1,
                        "PageTitle": 1,
                        "PageWikipediaLink": 1,
                        "SiteInfoDBName": 1,
                        "SiteInfoName": 1,
                        "SiteLanguage": 1,
                        "pageWikipediaGenerated": 1,
                        "highlights": { "$meta": "searchHighlights" }
                    }
                }, {
                    "$limit": 1250
                }
            ], 
            'facets': [
                {
                    '$replaceWith': '$$SEARCH_META'
                }, {
                    '$limit': 1
                },
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

def filteredTextSearchQuery(searchQuery, PageLastModifiedUser, PageNamespace, SiteInfoName, SiteInfoDBName, SiteLanguage, PageRestrictions, PageBytes, PageNumberLinks, PageLastModified, PageHasRedirect):
    pipeline = textSearchQuery(searchQuery)
    if PageLastModifiedUser:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "PageLastModifiedUser", "query": PageLastModifiedUser}})
    if PageNamespace:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "PageNamespace", "query": PageNamespace}})
    if SiteInfoName:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "SiteInfoName", "query": SiteInfoName}})
    if SiteInfoDBName:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "SiteInfoDBName", "query": SiteInfoDBName}})
    if SiteLanguage:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "SiteLanguage", "query": SiteLanguage}})
    if PageRestrictions:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "PageRestrictions", "query": PageRestrictions}})
    if PageBytes:
        if PageBytes == "+300000":
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageBytes", "gte": 300000}})
        else:
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageBytes", "lt": (int(PageBytes)+30000), "gte": int(PageBytes)}})
    if PageNumberLinks:
        if PageNumberLinks == "+50":
                pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageNumberLinks", "gte": 50}})
        else:
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageNumberLinks", "lt": (int(PageNumberLinks)+5), "gte": int(PageNumberLinks)}})
    if PageLastModified:
        if PageLastModified == "Older":
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageLastModified", "lte": dt.datetime(2023, 1, 1, 0, 0, 0)}})
        else: 
            date_format = "%a, %d %b %Y %H:%M:%S %Z"
            # Parse the date string into a datetime object
            dateObj = dt.datetime.strptime(PageLastModified, date_format)
            newDate = dateObj + dt.timedelta(days=31)
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageLastModified", "lt": newDate, "gte": dateObj}})
    if PageHasRedirect:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "PageHasRedirect", "query": PageHasRedirect}})
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

@app.route("/mongodb/get_data/<query>", methods=["POST"])
def get_data (query):
    filters = request.get_json()
    pipeline = filteredTextSearchQuery(query, filters[0], filters[1], filters[2], filters[3], filters[4], filters[5], filters[6], filters[7], filters[8], filters[9])
    results = list(mongo.db.pages.aggregate(pipeline))[0]
    for doc in results["docs"]:
        for highlight in doc["highlights"]:
            doc[highlight["path"]] = highlight["texts"]
    return results

@app.route("/mongodb/get_doc/<id>/<query>", methods=["POST"])
def get_doc (id, query):
    pipeline = textSearchQuery(query)
    pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "_id", "query": id}})
    document = list(mongo.db.pages.aggregate(pipeline))[0]["docs"][0]
    toHighlight = []
    for dict in document["highlights"]:  
        toHighlight.append(dict["path"])
    toHighlight.remove("_id")

    for path in toHighlight:
        if isinstance(document[path], str):
            text = document[path].split(query)
            document[path] = []
            for index in range(len(text)):
                if text[index] != "":
                    if index == len(text)-1:
                        document[path].append({"type": "text", "value": text[index]})
                    else:
                        document[path].append({"type": "text", "value": text[index]})
                        document[path].append({"type": "hit", "value": query})
        
    return document

if __name__ == "__main__":
    mongo = mongoDBConnection()
    app.run()