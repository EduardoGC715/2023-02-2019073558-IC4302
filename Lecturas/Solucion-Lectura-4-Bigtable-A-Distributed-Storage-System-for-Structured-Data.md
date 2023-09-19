### José Eduardo Gutiérrez Conejo - 2019073558 
### Bases de Datos II
### Lectura 4: Bigtable: A Distributed Storage System for Structured Data

1. ¿Cómo se diferencia el modelo de datos de Big Tables de una base de datos SQL?

    Bigtable difiere de una base de datos SQL al proporcionar un modelo de datos más flexible y no relacional. Permite a los clientes controlar dinámicamente la disposición y el formato de los datos, sin la necesidad de un esquema fijo. Los datos se organizan utilizando nombres de fila y columna, y se tratan como cadenas no interpretadas, aunque los clientes a menudo pueden serializar datos estructurados en estas cadenas. Por otro lado, una base de datos SQL se basa en un modelo de datos relacional con tablas y un esquema fijo que define la estructura de los datos. Esta diferencia en el modelo de datos tiene un impacto significativo en la forma en que se almacenan y acceden a los datos en ambos sistemas

2. ¿Cuáles decisiones de diseño en Big Table aumenta el rendimiento del sistema? Explique.

    Las desiciones que le permiten al Big Table ser eficiente son:
    - Grupos de Localidad: Los grupos de localidad en Bigtable permiten a los usuarios especificar qué datos deben estar físicamente cerca unos de otros en los servidores. Esto es crucial para reducir la latencia de acceso a los datos. Por ejemplo, si se sabe que ciertos datos se acceden juntos con frecuencia, se pueden asignar a la misma localidad para minimizar los tiempos de acceso.

    - Caching: Bigtable tiene la capacidad de usar cachés para almacenar datos en memoria para acceso rápido. Utilizar correctamente la caché puede acelerar las operaciones de lectura, ya que se pueden recuperar datos directamente desde la memoria en lugar de acceder al almacenamiento subyacente.

    - Aceleración de la recuperación de tabletas: La recuperación de tabletas se refiere al proceso de volver a cargar datos después de una falla. Optimizar este proceso es crucial para minimizar la interrupción del servicio. Estrategias eficientes de recuperación de tabletas pueden reducir el tiempo de inactividad y mejorar la disponibilidad del sistema.

    - Filtros Bloom: Los filtros Bloom son estructuras de datos probabilísticas utilizadas para determinar si un elemento pertenece a un conjunto. En Bigtable, se utilizan para reducir la necesidad de acceder a datos en disco durante las operaciones de lectura, lo que puede mejorar la eficiencia y el rendimiento.

    - Compresión: La compresión de datos reduce el tamaño de los datos almacenados, lo que puede disminuir los tiempos de lectura y escritura. Al comprimir los datos antes de almacenarlos, se reduce la cantidad de datos que deben transferirse entre el almacenamiento y los nodos de procesamiento, lo que puede mejorar significativamente el rendimiento.

    - Implementación de Commit-log: La forma en que se implementa el registro de confirmación (commit-log) puede afectar el rendimiento. Una implementación eficiente puede reducir la latencia en operaciones de escritura, lo que es esencial para mantener un alto rendimiento en entornos de alta concurrencia.

    - Explotar Inmutabilidad: Bigtable está diseñado para funcionar bien con conjuntos de datos inmutables, es decir, conjuntos de datos que no se modifican con frecuencia. Al aprovechar esta característica, se pueden realizar optimizaciones específicas que aprovechen la naturaleza inmutable de los datos, lo que puede mejorar el rendimiento general del sistema.
  
3. ¿Considera que Big Table podría cumplir el papel de Prometheus en un sistema de Observabilidad? En caso de responder No, explique detalladamente, en caso de responder si, ¿utilizarían versiones de timestamps para cada métrica y recolectarían cada métrica como un row separado?

    No se considera que Big Table sea una solución directa para reemplazar a Prometheus en un sistema de observabilidad.

    Prometheus está diseñado específicamente para la recopilación, almacenamiento y consulta de métricas de sistemas y aplicaciones y ofrece una serie de características orientadas a la observabilidad, mientras que Bigtable es un sistema de almacenamiento de datos distribuido altamente escalable, que se enfoca en proporcionar una infraestructura para almacenar grandes cantidades de datos estructurados y realizar consultas de baja latencia en ellos. No está optimizado para la recopilación y procesamiento en tiempo real de métricas de sistemas.

    Con respecto a la organización de datos en Big Table para almacenar métricas, sería posible usar versiones de timestamps para mantener un historial temporal de las métricas. Cada métrica podría ser almacenada como una fila, donde las versiones de columna representarían los diferentes puntos temporales de la métrica. Esto permitiría consultas históricas y análisis de tendencias, pero es importante tener en cuenta que este enfoque puede no ser tan eficiente como una solución diseñada específicamente para este propósito.

4. Explique en detalle la organización de tablets en Big Table
   
    Cuando se crea una tabla en Big Table, el sistema divide el rango de claves de fila en partes más pequeñas llamadas tablets. Esto se hace para permitir una distribución eficiente de los datos y facilitar la escalabilidad.

    Los tablets se distribuyen entre los servidores que forman parte del clúster de Big Table. Esto asegura que la carga de trabajo se distribuya equitativamente y previene la congestión en puntos específicos.

    El master de Big Table es responsable de asignar tablets a los servidores de tablets. Esto implica determinar qué servidor manejará cada tablet y supervisar cualquier cambio en esta asignación, como la adición o eliminación de servidores de tablets.

    Cada servidor de tablets es responsable de gestionar un conjunto de tablets. Estos servidores manejan tanto las solicitudes de lectura como de escritura para los tablets que tienen cargados. Además, se encargan de dividir tablets que hayan crecido demasiado en tamaño.

5. Comente los tipos de fallas de sistemas distribuidos en bases de datos que se mencionan en la lectura.
   
    - Corrupción de memoria y red: Esto implica la alteración o daño de la integridad de los datos en la memoria o durante la transmisión a través de la red.
  
    - Google File System: Indica que se han enfrentado problemas relacionados con la superación de los límites de almacenamiento establecidos en el sistema de archivos utilizado.

    - Clock Skew: Refiere a una discrepancia significativa en la medición del tiempo entre diferentes relojes en el sistema. Esto puede afectar la sincronización de eventos y la consistencia temporal en un sistema distribuido.
    
    - Hung Machines: Sucede cuando una máquina en el sistema se bloquea o deja de responder, lo que puede resultar en interrupciones en el funcionamiento del sistema.
    
    - Errores en sistemas como Chubby: Se refiere a problemas causados por fallos en otros sistemas que están siendo utilizados como parte del entorno de Big Table.

    - Divisiones de red extendidas y asimétricas: Estas divisiones ocurren cuando los nodos en un sistema distribuido pierden la capacidad de comunicarse entre sí. Si estas divisiones afectan solo a un subconjunto de nodos, se consideran asimétricas.

    - Mantenimiento de hardware: Tanto el mantenimiento de hardware planificado como el no planificado es fuente de problemas y desafíos en la operación y el rendimiento.