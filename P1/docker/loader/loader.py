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

def transformLinks(links, pageId):
    for link in links:
        link.append(pageId)

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

if __name__:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-chicago-1.oraclecloud.com))(connect_data=(service_name=gcea482f4f1b83b_ic4302_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
    connectionSQL=oracledb.connect(
     user="ADMIN",
     password="thisiswrongNereo08",
     dsn=cs)

     

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

        abstract_objects_response = object_storage.list_objects(namespace, bucket_name, prefix="enwiki-latest-abstract", fields="timeCreated")
        abstractReferenceList = sorted(abstract_objects_response.data.objects, key=lambda x: x.time_created, reverse=True)
        print("", "abstract reference list")
        print(abstractReferenceList)


        list_objects_response = object_storage.list_objects(namespace, bucket_name, prefix="enwiki-latest-pages-articles-multistream", fields="timeCreated")
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
        # input()
        for objectReference in objectProcessList:
            print(objectReference.name)

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
            print("siteInfo:", siteInfo.name, siteInfo.dbname, siteInfo)

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
                print("INSERTED SITEINFO")
            # si ya hay un siteInfo con ese nombre y dbname, guarda el siteInfoId para insertarlo como FK.
            else:
                siteInfoId = row[0]

            first = False
            #guardar el primer id y el page
            for page in xmlDump.pages:
                try:
                    if not first:
                        firstPageId = page.id
                        firstPageTitle = page.title
                        first = True
                    # print(page.id)
                    # print(page.title)
                    # print(page.namespace)
                    # print(page.redirect)
                    # print(page.restrictions)
                    pageHasRedirect = 1 if page.redirect else 0
                    lastPageId = page.id
                    lastPageTitle = page.title
                except Exception as e:
                    continue
                # for revision in page:
                #     print(revision.id, revision.timestamp, revision.user)
                #     print("bytes: ", revision.bytes, "text: ", revision.text)
                revisions = sorted(page, key=lambda x: x.timestamp, reverse=True)
                latestRevision = revisions[0]
                latestRevision.timestamp = datetime.fromtimestamp(latestRevision.timestamp.unix())
                try:
                    cursorSQL.execute("""
                        INSERT INTO pages (pageId, pageTitle, pageNamespace, pageRedirect, pageHasRedirect, pageLastModified, pageLastModifiedUser, pageBytes, pageText,
                            pageWikipediaLink, pageWikipediaGenerated,
                            pageNumberLinks, siteInfoId) VALUES
                            (:pageId, :pageTitle, :pageNamespace, :pageRedirect, :pageHasRedirect, :pageLastModified, :pageLastModifiedUser, :pageBytes, :pageText,
                            :pageWikipediaLink, :pageWikipediaGenerated,
                            :pageNumberLinks, :siteInfoId)""",
                            [page.id, page.title, page.namespace, page.redirect, pageHasRedirect, latestRevision.timestamp, latestRevision.user.text, latestRevision.bytes,
                            latestRevision.text, None, f"http://en.wikipedia.org/?curid={page.id}", None, siteInfoId])
                    connectionSQL.commit()
                    # TODO: TODOS MENOS Links
                except oracledb.IntegrityError as e:
                    continue

            print(firstPageTitle, lastPageTitle)

            abstractFileList = []
            varianceInterval = 5
            for abstractReference in abstractReferenceList:
                # validar limite de procesamiento
                # si es más nuevo que el last processed timestamp, lo agrega al final para que luego se
                # empiece a leer a partir del más cercano al timestamp que sea más nuevo.
                if abstractReference.time_created > (objectReference.time_created - timedelta(minutes=varianceInterval)):
                    abstractFileList.insert(0, abstractReference)
                else:
                    # si es más viejo, se agrega al final, porque igual puede ser posible leerlo.
                    abstractFileList.append(abstractReference)

            print(abstractFileList)
            #input()
            started = False
            finished = False
            # recorrer abstracts nuevos para iterar y buscar page titles y links
            for abstractReference in abstractFileList:
                # si el abstract no está descargado todavía en la máquina virtual, lo descarga.
                if not os.path.exists(f"abstracts/{abstractReference.name}"):
                    abstractObject = object_storage.get_object(namespace, bucket_name, abstractReference.name).data
                    abstractFile = open(f"abstracts/{abstractReference.name}", 'wb')
                    abstractFile.write(abstractObject.content)
                    abstractFile.close()

                print("opening...")
                abstract = open(f"abstracts/{abstractReference.name}", 'rb')
                print("Opened")
                
                for item in Parser(abstract).iter_from(Doc):
                    if started or item.title[11:] == firstPageTitle:
                        if item.title[11:] == firstPageTitle:
                            print("First found...")
                        started = True
                        url = item.url
                        links = item.sublinks
                        pageId = cursorSQL.var(int)
                        cursorSQL.execute("""
                            UPDATE pages
                            SET pageWikipediaLink = :url, pageNumberLinks = :num
                            WHERE pageTitle = :title
                            RETURNING pageId INTO :pageId
                            """,
                            [url, len(links), item.title[11:], pageId]) #TODO: INFO DE LINKS
                        pageId = pageId.getvalue()[0]
                        # print(pageId)
                        transformLinks(links, pageId)
                        # print(links)
                        cursorSQL.executemany(
                            """
                            INSERT INTO pageLinks (anchor, link, pageId)
                            VALUES (:anchor, :link, :pageId)""", links
                        )
                        connectionSQL.commit()
                        if item.title[11:] == lastPageTitle:
                            print("Found Last")
                            url = item.url
                            links = item.sublinks
                            finished = True
                            break
                # si no ha leido todas las pages, continúa con el siguiente archivo de abstracts de la lista.
                if finished:
                    break
            # borrar el archivo
            xmlFile.close()
            os.remove(f"multistreams/{objectReference.name}")
            with open("processedLog.json", 'w') as processedLog:
                data = {'lastProcessedTimestamp': objectReference.time_created.isoformat()}
                json.dump(data, processedLog)
        
        logger.debug("Finished checking Object Storage...")
        time.sleep(120)
