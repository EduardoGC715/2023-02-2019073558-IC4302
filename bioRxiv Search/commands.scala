
// kubectl port-forward service/ic4302-es-http 9200:9200
//https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html
//https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz
//https://artifacts.elastic.co/downloads/elasticsearch-hadoop/elasticsearch-hadoop-8.6.2.zip
// copy elasticsearch-hadoop-8.6.2.jar into spark-2.4.8-bin-hadoop2.7/jars/

// se hacen todos los imports
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
import org.apache.spark.sql.types.StringType
import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.DataFrame

// Se detiene el contexto y la session actuales para definirlos manualmente.
sc.stop()
spark.stop()

// Se establece la configuración para conectar con Elasticsearch
val conf = new SparkConf()
conf.set("es.index.auto.create", "true")
conf.set("es.nodes", "http://localhost:9200/")
conf.set("es.net.http.auth.user", "elastic")
conf.set("es.net.http.auth.pass", "54h5i778GJVYi61n2xvExq9h")
conf.set("es.port", "9200")
conf.set("es.nodes.wan.only", "true")

// Se crea el nuevo contexto y session
val sc = new SparkContext(conf) // El contexto es el punto de entrada al cluster de Spark, lo cual permite manejar recursos y coordinar tareas.

// Un session es un nivel de abstracción que permite trabajar con data frames y datasets.
val spark = SparkSession.builder.config(sc.getConf).getOrCreate()

// Permite tener una interfaz para trabajar con datos estructurados mediante el uso de SparkSQL.
val sqlcontext = new org.apache.spark.sql.SQLContext(sc)

// Crea un data frame con lo que obtiene del índice de augmented.
val augmentedDF = spark.read.format("org.elasticsearch.spark.sql").option("es.read.field.as.array.include","articles,articles.rel_authors,articles.entities").load("augmented")
augmentedDF.printSchema()
augmentedDF.show(false)

// Crea funciones que transforman los datos.
val categoryTransform: String => String = category =>category.toLowerCase.capitalize

val categoryUDF: UserDefinedFunction = udf(categoryTransform)

val dateTransform: String => String = date => {
  val originalFormat = new java.text.SimpleDateFormat("yyyy-MM-dd")
  val targetFormat = new java.text.SimpleDateFormat("dd/MM/yyyy")
  targetFormat.format(originalFormat.parse(date))
}

val dateUDF: UserDefinedFunction = udf(dateTransform)

val nameTransform: String => String = fullName => {
  val parts = fullName.split(" ")
  if (parts.length >= 2) {
    val lastName = parts.last
    val firstName = parts.dropRight(1).mkString(" ")
    s"$lastName, $firstName"
  } else {
    fullName
  }
}


val nameUDF: UserDefinedFunction = udf(nameTransform)

augmentedDF.createOrReplaceTempView("temp_view")
val result = spark.sql("""
  SELECT
    article.rel_title AS title,
    article.category AS category,
    article.rel_date AS rel_date,
    author.author_name AS author_name,
    author.author_inst AS author_inst
  FROM
    temp_view
  LATERAL VIEW explode(articles) AS article
  LATERAL VIEW explode(article.rel_authors) AS author
""")
result.show(50)

val transformedDF = result.withColumn("title", col("title")).withColumn("category", categoryUDF(col("category"))).withColumn("rel_date", dateUDF(col("rel_date"))).withColumn("author_name", nameUDF(col("author_name")))

transformedDF.show(50)

val indexName = "documents"

val groupedDF = transformedDF.groupBy("title").agg(first("category").alias("category"),first("rel_date").alias("rel_date"),collect_list(struct("author_name", "author_inst")).alias("authors"))

groupedDF.saveToEs("documents", Map("es.mapping.id" -> "title"))


/*
val transformedDF = result.withColumn("articles.category", categoryUDF(categoriesDF.select(col("categories")))).withColumn("articles.rel_date", dateUDF(datesDF.select(col("rel_date")))).groupBy("splitId").agg(collect_list("articles").as("articles"))


transformedDF.show()
transformedDF.saveToEs("documents")

////////////////

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
    authorName
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
*/
transformedDF.show()
transformedDF.saveToEs("documents")

df.createOrReplaceTempView("es")
spark.sql("SELECT col.hostname as hostname, col.msg as msg FROM (SELECT EXPLODE(data) FROM es)").show
spark.sql("SELECT col.hostname as hostname, col.msg as msg FROM (SELECT EXPLODE(data) FROM es)").saveToEs("documents")