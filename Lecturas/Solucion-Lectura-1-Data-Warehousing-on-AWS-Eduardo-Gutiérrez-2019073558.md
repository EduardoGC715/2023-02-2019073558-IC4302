### José Eduardo Gutiérrez Conejo - 2019073558 
### Bases de Datos II
### Lectura 1: Data Warehousing on AWS

1. ¿En qué consisten datos estructurados, semiestructurados y no estructurados? Comente ejemplos de estos tipos de datos.

   * Los datos estructurados corresponden a datos que tienen un formato estandarizado que permite tanto al software como a las personas acceder a estos de forma eficaz. Por lo general, se trata de datos tabulares con filas y columnas que definen claramente sus atributos. Los semiestructurados corresponden a datos que no pueden considerarse totalmente estructurados porque carecen de un modelo de datos relacional o tabular específico. No obstante, incluyen metadatos que se pueden analizar, como etiquetas y otros marcadores. Y los no estructurados corresponden a información sin un modelo de datos establecido o datos que no están ordenados de una manera predefinida.
  
&nbsp;

2. ¿En qué consisten datos de series de tiempo? ¿Se consideran logs, datos de series de tiempo?
 
    *  Los datos de series de tiempo son una secuencia de data points, que típicamente consisten en sucesivas métricas hechas desde una fuente de datos sobre un determinado periodo de tiempo. Los logs no son considerados datos de series de tiempo ya que estos suelen ser mucho más ricos que las series temporales. Pueden ser tanto estructurado como no estructurado, generalmente empleando tecnologías de búsqueda de texto completo. Esto significa índices invertidos, lenguajes de consulta enriquecidos y grandes gastos generales de almacenamiento de datos. Y además, la tolerancia a la pérdida de datos es muy baja.

&nbsp;

3. ¿Comente diferencias entre Lake house, Data warehouse y Data mart?
   
    * El Lake house es un patrón de arquitectura que combina los mejores elementos de Data warehouse y Data lakes, este modelo permite un percepción más profunda de sobre los datos. Por otro lado, con un Data warehouse se pueden correr análisis rápidos en grandes volumenes de datos y descubrir patrones escondidos en los datos aprovechando herramientas de BI. Finalmente un Data mart es una simplificación de un Data warehouse cuya función esta definida de forma específica a un área funcional o tema.

&nbsp;

4. ¿En qué consiste Row-oriented Column-oriented databases? Suponiendo que existe una tabla en una base de datos relacional con 10 columnas cuyos nombres son column1, column2, …., column10, ¿Una consulta como “SELECT column1, colum2 FROM tabla” se vería mas beneficiada por Row-oriented o Column-oriented? Explique.

    * Row-oriented consiste en una base de datos cuyos datos son guardados en filas completas en un bloque físico, mientras que un column-oriented consiste en que cada columna con sus datos es su propio bloque físico. Dado el ejemplo la base de datos se vería más beneficiada si se utiliza column-oriented, ya que al realizar la consulta solo se estan consultando 2 columnas de la tabla; lo que en una row-oriented generaría tener que buscar todos las filas y además las columnas especificada, en un column-oriented solo tendria que consultar las dos columnas especificadas.

Referencias:  

Amazon (s.f.). ¿Cuáles son las diferencias entre los datos estructurados y los no estructurados? AWS. Recuperado el 5 de agosto de 2023 de https://aws.amazon.com/es/what-is/structured-data/#:~:text=Los%20datos%20estructurados%20tienen%20un,que%20definen%20claramente%20sus%20atributos.   

Droogenbroeck, I. V. (15 de Julio de 2022). Introducción a Datos de Series Temporales ¿Qué son? Y ¿Con qué se comen? CDUser. Recuperado el 5 de agosto de 2023 de https://cduser.com/introduccion-a-datos-de-series-temporales/  

O'Toole, P. (23 de agosto de2020). Logs and Time Series are not the Same. Vallified. Recuperado el 5 de agosto de 2023 de https://www.philipotoole.com/logs-and-time-series-are-not-the-same/