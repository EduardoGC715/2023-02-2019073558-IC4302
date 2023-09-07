
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
// cambiar contraseña cada vez que se ejecuta el cluster (secrets de Lens)
conf.set("es.net.http.auth.pass", "28T5XPW08xAGl8W10O2eS9JT")
conf.set("es.port", "9200")
conf.set("es.nodes.wan.only", "true")

// Se crea el nuevo contexto y session
val sc = new SparkContext(conf) // El contexto es el punto de entrada al cluster de Spark, lo cual permite manejar recursos y coordinar tareas.

// Un session es un nivel de abstracción que permite trabajar con data frames y datasets.
val spark = SparkSession.builder.config(sc.getConf).getOrCreate()

// Permite tener una interfaz para trabajar con datos estructurados mediante el uso de SparkSQL.
val sqlcontext = new org.apache.spark.sql.SQLContext(sc)

// Crea funciones que transforman los datos. 
// Código basado en
//https://www.geeksforgeeks.org/scala-string-tolowercase-method-with-example/
val categoryTransform: String => String = category =>category.toLowerCase.capitalize

val categoryUDF: UserDefinedFunction = udf(categoryTransform)

// Código basado en
// https://stackoverflow.com/questions/27620889/scala-simpledateformat
val dateTransform: String => String = date => {
  val originalFormat = new java.text.SimpleDateFormat("yyyy-MM-dd")
  val targetFormat = new java.text.SimpleDateFormat("dd/MM/yyyy")
  targetFormat.format(originalFormat.parse(date))
}

val dateUDF: UserDefinedFunction = udf(dateTransform)

val nameTransform: String => String = fullName => {
  if (fullName == null || fullName == ""){
    "No author"
  }
  val parts = fullName.split(" ") // Se separa el nombre entre las partes
  if (parts.length >= 2) { // Si el nombre no es solo de una parte
    val lastName = parts.last // el apellido lo toma como la última parte
    val firstName = parts.dropRight(1).mkString(" ") // el nombre es lo demás y elimina el espacio del final
    s"$lastName, $firstName" // retorna el string formateado.
  } else {
    fullName
  }
}

val nameUDF: UserDefinedFunction = udf(nameTransform)

val componentsTransform: String => String = component => {
  component.replace("\"","'") // se cambian los " por ' para que se formatee bien la string en Elasticsearch
}

val componentsUDF: UserDefinedFunction = udf(componentsTransform)

// Se lee el índice de augmented en Elasticsearch.
val augmentedDF = spark.read.format("org.elasticsearch.spark.sql").option("es.read.field.as.array.include","articles,articles.rel_authors,articles.entities").load("augmented")
augmentedDF.printSchema()
augmentedDF.show(false)

// Esta view temporal se utiliza para realizar queries en SQL
// y obtener las columnas.
augmentedDF.createOrReplaceTempView("temp_view")

// se obtienen las columnas que se necesitan.
val result = spark.sql("""
  SELECT
    article.rel_title AS title,
    article.category AS category,
    article.rel_date AS rel_date,
    author.author_name AS author_name,
    author.author_inst AS author_inst,
    author.institutions AS components
  FROM
    temp_view
  LATERAL VIEW explode(articles) AS article
  LATERAL VIEW explode(article.rel_authors) AS author
""")

result.show(50)

// Se transforman las columnas necesarias.
val transformedDF = result.withColumn("title", col("title")).withColumn("category", categoryUDF(col("category"))).withColumn("rel_date", dateUDF(col("rel_date"))).withColumn("author_name", nameUDF(col("author_name"))).withColumn("components", componentsUDF(col("components")))

transformedDF.show(50)
// Se agrupan los registros en los artículos.
val groupedDF = transformedDF.groupBy("title").agg(first("category").alias("category"),first("rel_date").alias("rel_date"),collect_list(struct("author_name", "author_inst","components")).alias("authors"))
groupedDF.show(50)

// Se guarda a Elasicsearch.
groupedDF.saveToEs("documents", Map("es.mapping.id" -> "title"))