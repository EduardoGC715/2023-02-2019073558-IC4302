import oci
import datetime
import logging
import mwxml
from bigxml import Parser, xml_handle_element, xml_handle_text, BigXmlError, HandlerTypeHelper, XMLElement, XMLText
from dataclasses import dataclass, field
from typing import List
import os
import oracledb

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

if __name__:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-chicago-1.oraclecloud.com))(connect_data=(service_name=gcea482f4f1b83b_ic4302_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
    connectionSQL=oracledb.connect(
     user="ADMIN",
     password="thisiswrongNereo08",
     dsn=cs)

    if not os.path.exists("abstracts"):
        os.mkdir("abstracts")

    oci.config.validate_config(config)
    object_storage = oci.object_storage.ObjectStorageClient(config)
    compartment_id = config['tenancy']
    namespace = object_storage.get_namespace().data
    bucket_name = "bibliotec"
    # upload_manager = oci.object_storage.UploadManager(object_storage, max_parallel_uploads=10)
    # upload_manager.upload_file(namespace, 'nereo', 'oc.py', 'oc.py')

    abstract_objects_response = object_storage.list_objects(namespace, bucket_name, prefix="enwiki-latest-abstract", fields="timeCreated")
    abstractReferenceList = sorted(abstract_objects_response.data.objects, key=lambda x: x.time_created, reverse=True)
    print("", "abstract reference list")
    print(abstractReferenceList)
    abstractFileList = []
    for abstractReference in abstractReferenceList:
        # validar limite de procesamiento
        abstractFileList.append(abstractReference.name)
        if not os.path.exists(f"abstracts/{abstractReference.name}"):
            abstractObject = object_storage.get_object(namespace, bucket_name, abstractReference.name).data
            abstractFile = open(f"abstracts/{abstractReference.name}", 'wb')
            abstractFile.write(abstractObject.content)
            abstractFile.close()

    if not os.path.exists("multistreams"):
        os.mkdir("multistreams")

    list_objects_response = object_storage.list_objects(namespace, bucket_name, prefix="enwiki-latest-pages-articles-multistream", fields="timeCreated")
    objectList = sorted(list_objects_response.data.objects, key=lambda x: x.time_created, reverse=True)
    print(objectList)
    # recorremos todos los objetos y subimos
    i = 0
    for objectReference in objectList:
        if i == 1:
            break
        # if (objectReference.name == "enwiki-latest-abstract10.xml"): #"enwiki-latest-pages-articles-multistream10.xml-p4045403p5399366"):
        #    continue
        print(objectReference.name)
        if not os.path.exists(f"multistreams/{objectReference.name}"):
            xmlReference = object_storage.get_object(namespace, bucket_name, objectReference.name).data
            
            xmlFile = open(f"multistreams/{objectReference.name}", 'wb')
            xmlFile.write(xmlReference.content)
            xmlFile.close()
            print("written")
    #   print(type(xmlFile))

        xmlDump = mwxml.Dump.from_file(open(f"multistreams/{objectReference.name}", 'rb'))
        siteInfo = xmlDump.site_info
        print("siteInfo:", siteInfo.name, siteInfo.dbname, siteInfo)
        j=0

        print("opening...")
        abstract = open("abstracts/enwiki-latest-abstract3.xml", 'rb')
        print("Opened")

        cursorSQL = connectionSQL.cursor()
        cursorSQL.execute("""
            INSERT INTO siteInfos (siteInfoName, siteInfoDBName) VALUES (:siteInfoName, :siteInfoDBName)""", [siteInfo.name, siteInfo.dbname])
        connectionSQL.commit()

        print("INSERTED SITE")
        input()
        #guardar el primer id y el page
        for page in xmlDump.pages:
            try:
                if not j:
                    firstPageId = page.id
                    firstPageTitle = page.title
                print(page.id)
                print(page.title)
                print(page.namespace)
                print(page.redirect)
                print(page.restrictions)
                pageHasRedirect = 1 if page.redirect else 0
                lastPageId = page.id
                lastPageTitle = page.title
            except Exception as e:
                continue
            for revision in page:
                print(revision.id, revision.timestamp, revision.user)
                print("bytes: ", revision.bytes, "text: ", revision.text)
            cursorSQL.execute("""
                INSERT INTO pages (pageId, pageTitle, pageNamespace, pageRedirect, pageHasRedirect, pageLastModified, pageLastModifiedUser, pageBytes, pageText,
                    pageWikipediaLink, pageWikipediaGenerated,
                    pageNumberLinks, siteInfoId) VALUES
                    (:pageId, :pageTitle, :pageNamespace, :pageRedirect, :pageHasRedirect, :pageLastModified, :pageLastModifiedUser, :pageBytes, :pageText,
                    :pageWikipediaLink, :pageWikipediaGenerated,
                    :pageNumberLinks, :siteInfoId)""",
                    [page.id, page.title, page.namespace, page.redirect, pageHasRedirect, None, None, 100, "Hello", None, None, None, 1])

            if j == 1:
                print("break")
                break
            j += 1
        i += 1

        # recorrer abstracts nuevos para iterar y buscar page titles y links
        # for abstract in abstractList
        for item in Parser(abstract).iter_from(Doc):
            if item.title[11:] == firstPageTitle:
                print("Found first")
                url = item.url
                links = item.sublinks
                print(url, links)
                break
            elif item.title[11:] == lastPageTitle:
                print("Found Last")
                url = item.url
                links = item.sublinks
                print(url, links)
        # borrar el archivo

