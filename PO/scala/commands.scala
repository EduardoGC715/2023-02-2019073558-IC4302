import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.SparkSession._
import org.elasticsearch.spark.sql
import org.elasticsearch.spark.sql._
import org.elasticsearch.spark._ 
// kubectl port-forward service/ic4302-es-http 9200:9200
//https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html
//https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz
//https://artifacts.elastic.co/downloads/elasticsearch-hadoop/elasticsearch-hadoop-8.6.2.zip
// copy elasticsearch-hadoop-8.6.2.jar into spark-2.4.8-bin-hadoop2.7/jars/
sc.stop()
spark.stop()

val conf = new SparkConf()
conf.set("es.index.auto.create", "true")
conf.set("es.nodes", "http://localhost:9200/")
conf.set("es.net.http.auth.user", "elastic")
conf.set("es.net.http.auth.pass", "6608EzMQ7X7zy004KQi7WHmM")
conf.set("es.port", "9200")
conf.set("es.nodes.wan.only", "true")


val sc = new SparkContext(conf)

val spark = SparkSession.builder.config(sc.getConf).getOrCreate()

val sqlcontext = new org.apache.spark.sql.SQLContext(sc)
val options = Map("es.read.field.as.array.include" -> "data")
val df = sqlcontext.read.options(options).format("org.elasticsearch.spark.sql").load("messages")
df.createOrReplaceTempView("es")
spark.sql("SELECT col.hostname as hostname, col.msg as msg FROM (SELECT EXPLODE(data) FROM es)").show
spark.sql("SELECT col.hostname as hostname, col.msg as msg FROM (SELECT EXPLODE(data) FROM es)").saveToEs("datos")