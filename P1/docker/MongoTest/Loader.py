from pymongo import MongoClient

def mongoDBConnection (): 
    try:
        mongo = MongoClient("mongodb+srv://eduardogc715:BasesII2023@bibliotec.6l341ym.mongodb.net/bibliotec")
        return mongo
    except Exception as e:
        print(f"An error occurred: {e}")

def upsertDocument(insert_id, values, mongo):
    try:
        db = mongo["bibliotec"]
        query = {"_id": insert_id}
        if len(values) > 3:
            update = {
                "PageId": values[0],
                "PageTitle": values[1],
                "PageNamespace": values[2],
                "PageRedirect": [3],
                "PageHasRedirect": values[4],
                "PageLastModified": values[5],
                "PageLastModifiedUser": values[6],
                "PageBytes": values[7],
                "PageText": values[8],
                "SiteInfoDBName": values[9],
                "SiteInfoName": values[10],
                "SiteLanguage": values[11],
                "pageWikipediaGenerated": values[12],
                "PageRestrictions": values[13]}
        else:
            update = {
                "PageWikipediaLink": values[0],
                "PageLinks": values[1],
                "PageNumberLinks": values[2]}
        
        updateQuery = {"$set": update}
        
        db["pages"].update_one(query, updateQuery, upsert=True)
    except Exception as e:
        raise e