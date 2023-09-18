### José Eduardo Gutiérrez Conejo - 2019073558 
### Bases de Datos II
### Lectura 4: Bigtable: A Distributed Storage System for Structured Data

1. ¿Cómo se diferencia el modelo de datos de Big Tables de una base de datos SQL?

    Bigtable difiere de una base de datos SQL al proporcionar un modelo de datos más flexible y no relacional. Permite a los clientes controlar dinámicamente la disposición y el formato de los datos, sin la necesidad de un esquema fijo. Los datos se organizan utilizando nombres de fila y columna, y se tratan como cadenas no interpretadas, aunque los clientes a menudo pueden serializar datos estructurados en estas cadenas. Por otro lado, una base de datos SQL se basa en un modelo de datos relacional con tablas y un esquema fijo que define la estructura de los datos. Esta diferencia en el modelo de datos tiene un impacto significativo en la forma en que se almacenan y acceden a los datos en ambos sistemas

2. ¿Cuáles decisiones de diseño en Big Table aumenta el rendimiento del sistema? Explique.

    Para aumentar el rendimiento en Bigtable, es crucial implementar agrupaciones eficientes en forma de "Grupos de Localidad". Esto permite a los clientes organizar múltiples familias de columnas, generando un SSTable distinto para cada grupo en cada tableta. Esta segregación facilita lecturas más eficaces, ya que se evita el acceso a columnas que no se consultan conjuntamente. Además, la posibilidad de establecer parámetros de ajuste específicos para cada grupo de localidad, como la opción de declarar un grupo como "en memoria", representa una mejora significativa. Esto posibilita la carga perezosa de SSTables en la memoria del servidor de tabletas, lo que, una vez completado, permite la lectura de columnas pertenecientes a este grupo sin necesidad de acceder al disco. Este enfoque es especialmente beneficioso para pequeños conjuntos de datos que se acceden con frecuencia, como la familia de columnas de ubicación en la tabla METADATA.

3. ¿Considera que Big Table podría cumplir el papel de Prometheus en un sistema de Observabilidad? En caso de responder No, explique detalladamente, en caso de responder si, ¿utilizarían versiones de timestamps para cada métrica y recolectarían cada métrica como un row separado?

4. Explique en detalle la organización de tablets en Big Table

5. Comente los tipos de fallas de sistemas distribuidos en bases de datos que se mencionan en la lectura.

### Referencias
