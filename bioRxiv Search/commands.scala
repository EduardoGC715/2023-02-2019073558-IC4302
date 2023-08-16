
// kubectl port-forward service/ic4302-es-http 9200:9200
//https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html
//https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz
//https://artifacts.elastic.co/downloads/elasticsearch-hadoop/elasticsearch-hadoop-8.6.2.zip
// copy elasticsearch-hadoop-8.6.2.jar into spark-2.4.8-bin-hadoop2.7/jars/
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.SparkSession._
import org.elasticsearch.spark.sql
import org.elasticsearch.spark.sql._
import org.elasticsearch.spark._ 
import org.apache.spark.sql.functions
import org.apache.spark.sql.functions._
sc.stop()
spark.stop()

val conf = new SparkConf()
conf.set("es.index.auto.create", "true")
conf.set("es.nodes", "http://localhost:9200/")
conf.set("es.net.http.auth.user", "elastic")
conf.set("es.net.http.auth.pass", "59cr05jqo3eZsAD3jT5zj859")
conf.set("es.port", "9200")
conf.set("es.nodes.wan.only", "true")


val sc = new SparkContext(conf)

val spark = SparkSession.builder.config(sc.getConf).getOrCreate()

val sqlcontext = new org.apache.spark.sql.SQLContext(sc)

val includedFields = "author_inst,author_name,category,rel_date" // List of fields to include
val esOptions = Map("es.read.field.include" -> includedFields)
val daf = spark.read.format("org.elasticsearch.spark.sql").options(esOptions).load("augmented") 

val explodedDF: Dataframe = daf.select(EXPLODE(col("articles")).alias("article"))

val resultDF: DataFrame = explodedDF.select(col("article.rel_author").alias("rel_author"),col("article.category").alias("category"),col("article.rel_date").alias("rel_date"))
resultDF.show()
val splitAuthorInst = functions.udf((authorInst: String) => {authorInst.split(", ").map(_.trim) })

val transformAuthorName = functions.udf((authorName: String) => {
    val parts = authorName.split(" ")
    if (parts.length == 2) {
    val lastName = parts(1)
    val firstName = parts(0)
    s"$lastName, $firstName"
    } else {
    authorName // Return original value if not in the expected format
    }
})

val transformCategory = functions.udf((category: String) => {
    val cleanedCategory = category.replaceAll("\\s+", "") 
    if (cleanedCategory.nonEmpty) {
        cleanedCategory.charAt(0).toUpper + cleanedCategory.substring(1).toLowerCase
    } else {
        cleanedCategory
    }
})

val transformRelDate = functions.udf((relDate: String) => {java.time.LocalDate.parse(relDate).format(java.time.format.DateTimeFormatter.ofPattern("dd/MM/yyyy"))})


val transformedDF = df.withColumn("author_inst", splitAuthorInst(df("author_inst"))).withColumn("author_name", transformAuthorName(df("author_name"))).withColumn("category", transformCategory(df("category"))).withColumn("rel_date", transformRelDate(df("rel_date")))

transformedDF.show()
transformedDF.saveToEs("documents")

df.createOrReplaceTempView("es")
spark.sql("SELECT col.hostname as hostname, col.msg as msg FROM (SELECT EXPLODE(data) FROM es)").show
spark.sql("SELECT col.hostname as hostname, col.msg as msg FROM (SELECT EXPLODE(data) FROM es)").saveToEs("documents")