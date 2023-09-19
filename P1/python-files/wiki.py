import mwxml
dump = mwxml.Dump.from_file(open("enwiki-latest-pages-articles-multistream1.xml-p1p41242"))
print(dump.site_info.name, dump.site_info.dbname)
for page in dump:
    print("###################################################################")
    print(page.title)
    print(page.redirect)
    print(page.id)
    print(page.namespace)
    print(page.restrictions)
    print("___________")
#    for revision in page:
#        print(revision.text)
#    print("####################################################################")
#    break
