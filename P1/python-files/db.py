import oracledb

cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-chicago-1.oraclecloud.com))(connect_data=(service_name=gfc652926fee44e_ic4302_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
connection=oracledb.connect(
     user="ADMIN",
     password="thisiswrongNereo08",
     dsn=cs)
