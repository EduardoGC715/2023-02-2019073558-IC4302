import oracledb

cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-chicago-1.oraclecloud.com))(connect_data=(service_name=gcea482f4f1b83b_ic4302_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
connection=oracledb.connect(
     user="ADMIN",
     password="thisiswrongNereo08",
     dsn=cs)
