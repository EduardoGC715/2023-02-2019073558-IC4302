import oci
import pytz
from datetime import datetime, timedelta, timezone
import logging
import mwxml
from bigxml import Parser, xml_handle_element, xml_handle_text, BigXmlError, HandlerTypeHelper, XMLElement, XMLText
from dataclasses import dataclass, field
from typing import List
import os
import oracledb
import json
import time
import hashlib
from pymongo import MongoClient

# Código basado de
# https://docs.oracle.com/en-us/iaas/tools/python/2.112.0/api/object_storage/client/oci.object_storage.ObjectStorageClient.html
# https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.112.0/objectstorage/get_object.py.html
# https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.112.0/objectstorage/list_objects.py.html

@xml_handle_element("feed", "doc")
@dataclass
class Doc:
    title: str = 'N/A'
    url: str = 'N/A'
    sublinks: List[str] = field(default_factory=list)
    sublink: List[str] = field(default_factory=list)

    @xml_handle_element("title")
    def handle_title(self, node):
        self.title = node.text

    @xml_handle_element("url")
    def handle_url(self, node):
        self.url = node.text

    @xml_handle_element("links", "sublink", "anchor")
    def handle_sublink_anchor(self, node):
        self.sublink = [node.text]
    
    @xml_handle_element("links", "sublink", "link")
    def handle_sublink_link(self, node):
        self.sublink.append(node.text)
        self.sublinks.append(self.sublink)

def transformLinks(links, pageTitleKey):
    for link in links:
        link.append(pageTitleKey)

def transformRestrictions(restrictions, pageTitleKey):
    result = []
    for restriction in restrictions:
        result.append([restriction, pageTitleKey])
    return result

config = {
   "key_content": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDM7xOlheMG9Jvn
DUOry1A+XuB6zuCi5nRSiGOqmbQfR/2/20wKteKTbIfRVe6MGGdHdpFTM1ZFZCPd
Vpru6KBk6Aona+iQWXK7tMKfhNjOTkpj88oeFBPx07mELTQLednaZDaojUhPmWZ6
/tE0BgzAVeu4nyu0KyxmFAL8x2ncXi/BFJgEsRaU0OkUns/VfUtFEUWD8BIzlPbR
L/Gi36ZxhqkMPpMs6FwUikYT1eU9KJ4oFgnxX3D4Vi9Fzcg0wrgRFYnNfEOGJZYE
rOLnrqFeowARYAH+nzowjkQ6CSb1QadGq7hzjismxQmxRs56SASKYkrVYVCSBG37
BMwfYDjrAgMBAAECggEAA8NIBbwFmnUXVRC7SLDnp52FBaboHQBE69cGmB/7sgSt
C2lyu1JHohQAvRPqLgxXU8qWNIQ2y04MEoj/40Rw3X7H4PLBnGo9XxDx7zfjOzaD
ddOzcbCbWnoGvVSPJhQgrzqJKQ3JtsccSJnb1tay7pJ6ojMvUZQ8BnZ2ROnsbwK1
62uoZG7XmHaqQJY7z2JZ1a/6Tt6YP2ufaAZxs8tqbfqKM369LIL/QKJNxkEsAncN
/eAiKjyhgPMPfOLxGnS/dWZgPdNjy92+Nw9iYs+5NVqRGiJpiGf4ovWNNPiIG3oL
KbVDhXt3ynwqIS6g6j5ILWicpiUmtstKOeU4oMIOAQKBgQD/sDU/BZ7ljjTQpb/p
YJvRGITpHcXovyH5z/GK6s3gCaJq9/tUihXzaZH5s1V5UOUFVb923KYbUKalyGlF
GRusMF5GWiI55cqFXI3R9KFlu4UJAglXuCxsWHejweRBV2a4DiVOlj45WuyLeJLR
jsL4CvflVMTZsgVIrObB/Ti9awKBgQDNLweqq44ksVDGMKWEZIlIz0PjPUSWhIDa
eUMjuazjLxiJ8yiUmf4AE7vK6SoiP9uudx2xWnnZyVIe/PJXseFbINuBh0k9jU6R
H8SOSLFS85TcrCl+ImNDygHiczxaVuiykjYpLIaPqT/BTayXnGiX+xBSwweA9Ng1
pZni2fXSgQKBgGfMM8Fy2a+dDEnLj94BDyBSUNqF8KrstLFCPm9DpPIXVy0PoKMQ
L5sSN2Vj7QYD1gVVaxWou3IJSq2wbzPS3o4HUK5EtvJEG/QJv7UFF2RCPN6MShin
NrmBLIh5FN2FyrhbXb/KdFY6WB7Cgu+5geLKKRqbUBKEF2sKbd9AmgEjAoGATg93
ZjnwUQtYhJ4bSlwJUrbvx/MWNgFhGD0MCvpnyOKw/kKRDL/tP1BCoLbGPdN3m09b
745RT0blRD7NYAmfh9DfUc8LUSyCWHnyiIMlWz6qQq4I9yDUDQU8ZE+dBW2NB+rS
SiXTZ7JnO/52DBQIQtHUavgh0bDU1MwU2JY9jIECgYEA4GumexTeBxhwomIKd4bn
5wbYGAgdg6TPym7mGHpEVwVc/SYg1mTeOp988ZIbzdLcjQLY9E5Kpd/dZzVZ5izs
IzI5Mtbaa6QFL3QyhFnyiANbyfuw4rJTGdkUgKlP/jsabVVfMw2x+w5lwPI8oU5E
wf4QTCyd9noRs4piFx6/9A0=
-----END PRIVATE KEY-----""",
  "user": "ocid1.user.oc1..aaaaaaaaxmr6fc3rqsoest3yfqamz3yjrulxovyua2xuwibxb6bdjlyj6lmq",
  "fingerprint": "aa:4e:83:38:68:4d:38:90:7c:14:b7:84:64:f6:c3:e1",
  "tenancy": "ocid1.tenancy.oc1..aaaaaaaab2j6gk2b33sutg2bhoga5zekg3j5su23tygzw6nw5es4jxdts4ya",
  "region": "us-chicago-1"
}

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
                "PageRedirect": values[3],
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

if __name__:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-chicago-1.oraclecloud.com))(connect_data=(service_name=gcea482f4f1b83b_ic4302_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
    connectionSQL=oracledb.connect(
     user="ADMIN",
     password="thisiswrongNereo08",
     dsn=cs)
    
    #connection to Mongo Atlas
    mongodb = mongoDBConnection()

    oci.config.validate_config(config)
    object_storage = oci.object_storage.ObjectStorageClient(config)
    compartment_id = config['tenancy']
    namespace = object_storage.get_namespace().data
    bucket_name = "bibliotec"

    # crea el folder donde se almacenarán los abstracts
    if not os.path.exists("abstracts"):
        os.mkdir("abstracts")
    # Crea el folder donde se almacenarán los multistreams
    if not os.path.exists("multistreams"):
        os.mkdir("multistreams")
    
    while True:
        try:
            # lee el último timestamp procesado.
            with open("processedLog.json", 'r') as processedLog:
                data = json.load(processedLog)
                lastProcessedTimestamp = datetime.fromisoformat(data["lastProcessedTimestamp"])
        except Exception as e:
            print(e)
            tz = pytz.timezone('UTC')
            lastProcessedTimestamp = tz.localize(datetime(1970, 1, 1, 0, 0)) # inicia con el valor del epoch

        logger.debug("Checking Object Storage...")

        list_objects_response = object_storage.list_objects(namespace, bucket_name, fields="timeCreated")
        objectList = sorted(list_objects_response.data.objects, key=lambda x: x.time_created, reverse=True)
        print(objectList)

        objectProcessList = [] # lista donde se guardará el orden de los archivos a procesar.

        # recorremos todos los objetos y agregamos a la lista de iteración solo a los que son más nuevos que el último límite de procesamiento
        for objectReference in objectList:
            print(objectReference.time_created, lastProcessedTimestamp, objectReference.time_created > lastProcessedTimestamp)
            if objectReference.time_created > lastProcessedTimestamp:
                objectProcessList.insert(0, objectReference)
            else:
                break

        print("objectList", objectProcessList)
        for objectReference in objectProcessList:
            print(objectReference.name)

            if objectReference.name.find("abstract") == -1:
                # Descargamos el archivo del object storage. Escribimos los bytes en un archivo para que pueda ser procesado por mwxml.
                if not os.path.exists(f"multistreams/{objectReference.name}"):
                    xmlReference = object_storage.get_object(namespace, bucket_name, objectReference.name).data
                    xmlFile = open(f"multistreams/{objectReference.name}", 'wb')
                    xmlFile.write(xmlReference.content)
                    xmlFile.close()
                    print("written")
            #   print(type(xmlFile))

                # abrimos el archivo para procesarlo con mwxml.
                xmlFile = open(f"multistreams/{objectReference.name}", 'rb')
                xmlDump = mwxml.Dump.from_file(xmlFile)

                # extraemos siteinfo
                siteInfo = xmlDump.site_info

                # cursor para los operaciones de SQL
                cursorSQL = connectionSQL.cursor()

                # revisamos si ya hay un siteinfo igual en la base de datos, para usar ese mismo como FK.
                cursorSQL.execute("""SELECT siteInfoId, siteInfoName, siteInfoDBName FROM siteInfos WHERE siteInfoName = :name AND siteInfoDBName = :dbname""",
                                [siteInfo.name, siteInfo.dbname])
                row = cursorSQL.fetchone()
                siteInfoId = cursorSQL.var(int)

                # si no hay un siteinfo, lo inserta a la base de datos y guadra el id generado en siteInfoId.
                if row is None:
                    cursorSQL.execute("""
                        INSERT INTO siteInfos (siteInfoName, siteInfoDBName, siteLanguage) VALUES (:siteInfoName, :siteInfoDBName, 'English')
                                    RETURNING siteInfoId INTO :siteInfoId""", ["Wakanda", siteInfo.dbname, siteInfoId])
                    connectionSQL.commit()
                    siteInfoId = siteInfoId.getvalue()[0]
                    logger.info("INSERTED SITEINFO")
                # si ya hay un siteInfo con ese nombre y dbname, guarda el siteInfoId para insertarlo como FK.
                else:
                    siteInfoId = row[0]

                #guardar el primer id y el page
                for page in xmlDump.pages:
                    pageHasRedirect = 1 if page.redirect else 0
                    pageHasRedirect4Mongo = "True" if page.redirect else "False"
                    revisions = sorted(page, key=lambda x: x.timestamp, reverse=True)
                    latestRevision = revisions[0]
                    latestRevision.timestamp = datetime.fromtimestamp(latestRevision.timestamp.unix())
                    latestRevision4Mongo = latestRevision.timestamp.isoformat()
                    hashkey = hashlib.md5(page.title.encode('UTF-8'))
                    pageTitleKey = hashkey.hexdigest()

                    # Insert multistream data into Mongo Atlas
                    data4MongoMS = [
                        page.id, 
                        page.title, 
                        page.namespace, 
                        page.redirect, 
                        pageHasRedirect4Mongo, 
                        latestRevision4Mongo, 
                        latestRevision.user.text, 
                        latestRevision.bytes,
                        latestRevision.text,
                        siteInfo.dbname,
                        siteInfo.name,
                        "English",
                        f"http://en.wikipedia.org/?curid={page.id}",
                        page.restrictions
                    ]
                    
                    upsertDocument(pageTitleKey, data4MongoMS, mongodb)

                    try:
                        print(len(latestRevision.text))
                        print([pageTitleKey, page.id, page.title, page.namespace, page.redirect, pageHasRedirect, latestRevision.timestamp, latestRevision.user.text, latestRevision.bytes,
                            None, f"http://en.wikipedia.org/?curid={page.id}", None, siteInfoId, pageTitleKey])
                        cursorSQL.execute("""
                            MERGE INTO pages
                            USING (
                                SELECT
                                    :pageTitleKey as pageTitleKey,
                                    :pageId AS pageId,
                                    :pageTitle AS pageTitle,
                                    :pageNamespace AS pageNamespace,
                                    :pageRedirect AS pageRedirect,
                                    :pageHasRedirect AS pageHasRedirect,
                                    :pageLastModified AS pageLastModified,
                                    :pageLastModifiedUser AS pageLastModifiedUser,
                                    :pageBytes AS pageBytes,
                                    :pageWikipediaLink AS pageWikipediaLink,
                                    :pageWikipediaGenerated AS pageWikipediaGenerated,
                                    :pageNumberLinks AS pageNumberLinks,
                                    :siteInfoId AS siteInfoId
                                FROM dual
                            ) pageDump
                            ON (pages.pageTitleKey = HEXTORAW(pageDump.pageTitleKey))
                            WHEN MATCHED THEN
                                UPDATE SET
                                    pages.pageId = pageDump.pageId,
                                    pages.pageNamespace = pageDump.pageNamespace,
                                    pages.pageRedirect = pageDump.pageRedirect,
                                    pages.pageHasRedirect = pageDump.pageHasRedirect,
                                    pages.pageLastModified = pageDump.pageLastModified,
                                    pages.pageLastModifiedUser = pageDump.pageLastModifiedUser,
                                    pages.pageBytes = pageDump.pageBytes,
                                    pages.pageWikipediaGenerated = pageDump.pageWikipediaGenerated,
                                    pages.siteInfoId = pageDump.siteInfoId
                            WHEN NOT MATCHED THEN
                                INSERT (pageTitleKey, pageId, pageTitle, pageNamespace, pageRedirect, pageHasRedirect, pageLastModified, pageLastModifiedUser, pageBytes,
                                    pageWikipediaLink, pageWikipediaGenerated,
                                    pageNumberLinks, siteInfoId) VALUES
                                    (pageDump.pageTitleKey, pageDump.pageId, pageDump.pageTitle, pageDump.pageNamespace, pageDump.pageRedirect, pageDump.pageHasRedirect,
                                    pageDump.pageLastModified,
                                    pageDump.pageLastModifiedUser, pageDump.pageBytes,
                                    pageDump.pageWikipediaLink, pageDump.pageWikipediaGenerated,
                                    pageDump.pageNumberLinks, pageDump.siteInfoId)
                            """,
                            [pageTitleKey, page.id, page.title, page.namespace, page.redirect, pageHasRedirect, latestRevision.timestamp, latestRevision.user.text, latestRevision.bytes,
                            None, f"http://en.wikipedia.org/?curid={page.id}", None, siteInfoId]
                        )
                        cursorSQL.execute("""
                        UPDATE pages
                        SET pageText = :pageText
                        WHERE pageTitleKey = HEXTORAW(:pageTitleKey)      
                        """, [latestRevision.text, pageTitleKey])
                        if len(page.restrictions):
                            restrictions = transformRestrictions(page.restrictions, pageTitleKey)
                            cursorSQL.executemany(
                                """
                                INSERT INTO restrictions (name, pageTitleKey)
                                VALUES (:name, :pageTitleKey)
                                """, restrictions
                            )
                        connectionSQL.commit()
                        if latestRevision.bytes == 158291:
                            input()
                    except oracledb.IntegrityError as e:
                        continue

                # borrar el archivo
                xmlFile.close()
                os.remove(f"multistreams/{objectReference.name}")
            else:
                # Descargamos el archivo del object storage. Escribimos los bytes en un archivo para que pueda ser procesado por mwxml.
                if not os.path.exists(f"abstracts/{objectReference.name}"):
                    abstractReference = object_storage.get_object(namespace, bucket_name, objectReference.name).data
                    abstractFile = open(f"abstracts/{objectReference.name}", 'wb')
                    abstractFile.write(abstractReference.content)
                    abstractFile.close()
                    print("written")

                print("opening...")
                abstract = open(f"abstracts/{objectReference.name}", 'rb')
                print("Opened")

                cursorSQL = connectionSQL.cursor()

                for item in Parser(abstract).iter_from(Doc):
                    url = item.url
                    links = item.sublinks
                    pageTitle = item.title[11:]
                    hashkey = hashlib.md5(pageTitle.encode('UTF-8'))
                    pageTitleKey = hashkey.hexdigest()

                    # Insert abstract data into Mongo Atlas
                    data4MongoA = [
                        url,
                        links,
                        len(links)
                    ]
                    upsertDocument(pageTitleKey, data4MongoA, mongodb)

                    try:
                        cursorSQL.execute(
                            """
                            MERGE INTO pages
                            USING (
                                SELECT
                                    :pageTitleKey as pageTitleKey,
                                    :pageTitle AS pageTitle,
                                    :pageWikipediaLink AS pageWikipediaLink,
                                    :pageNumberLinks AS pageNumberLinks
                                FROM dual
                            ) pageAbstract
                            ON (pages.pageTitleKey = HEXTORAW(pageAbstract.pageTitleKey))
                                WHEN MATCHED THEN
                                    UPDATE SET
                                        pages.pageWikipediaLink = pageAbstract.pageWikipediaLink,
                                        pages.pageNumberLinks = pageAbstract.pageNumberLinks
                                WHEN NOT MATCHED THEN
                                    INSERT (pageTitleKey, pageTitle,
                                        pageWikipediaLink, pageNumberLinks) VALUES
                                        (pageAbstract.pageTitleKey, pageAbstract.pageTitle, pageAbstract.pageWikipediaLink, pageAbstract.pageNumberLinks)
                            """,
                            [pageTitleKey, pageTitle, url, len(links)]
                        )
                        # print(pageId)
                        transformLinks(links, pageTitleKey)
                        # print(links)
                        cursorSQL.executemany(
                            """
                            INSERT INTO pageLinks (anchor, link, pageTitleKey)
                            VALUES (:anchor, :link, :pageTitleKey)""", links
                        )
                        connectionSQL.commit()
                    except oracledb.IntegrityError as e:
                        continue
                abstract.close()
                os.remove(f"abstracts/{objectReference.name}")
            with open("processedLog.json", 'w') as processedLog:
                data = {'lastProcessedTimestamp': objectReference.time_created.isoformat()}
                json.dump(data, processedLog)

        logger.debug("Finished checking Object Storage...")
        time.sleep(120)

