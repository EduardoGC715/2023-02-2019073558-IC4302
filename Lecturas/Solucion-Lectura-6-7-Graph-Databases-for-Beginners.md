### José Eduardo Gutiérrez Conejo - 2019073558 
### Bases de Datos II
### Lectura 6/7: Graph Databases for Beginners

1. ¿De qué forma se diferencia el BASE consistency model del ACID?

    ACID (Atomicidad, Consistencia, Aislamiento y Durabilidad) es un modelo de consistencia que se centra en garantizar la fiabilidad y la integridad de los datos en situaciones de fallos.

    - **Atomicidad:** Todas las operaciones de una transacción se realizan de forma completa o ninguna se realiza. No hay un estado intermedio.

    - **Consistencia:** La base de datos siempre pasa de un estado válido a otro estado válido después de una transacción.

    - **Aislamiento:** Las transacciones pueden ejecutarse de manera simultánea sin interferirse mutuamente. Los resultados de una transacción no son visibles para otras transacciones hasta que se complete.

    - **Durabilidad:** Una vez que una transacción se completa con éxito, los cambios persisten incluso en caso de fallo del sistema.

    BASE (Basic Availability, Soft State, Eventual Consistency) en cambio, es un modelo que se enfoca en la disponibilidad y la escalabilidad, incluso a expensas de la consistencia inmediata de los datos.

    - **Disponibilidad Básica:** La base de datos siempre está disponible, incluso si no puede garantizar la consistencia inmediata.

    - **Estado Suave:** El estado de la base de datos puede cambiar a lo largo del tiempo, incluso sin entradas de nuevos datos.

    - **Consistencia Eventual:** Después de un tiempo, todos los nodos de la base de datos llegarán a un estado consistente.

2. ¿Explique porque no es recomendable modelar una base de datos orientada a grafos mediante una base de datos relacional?

    No es recomendable modelar una base de datos orientada a grafos con una base de datos relacional porque los paradigmas subyacentes son fundamentalmente diferentes. Una base de datos relacional organiza los datos en tablas con relaciones entre ellas, mientras que una base de datos orientada a grafos utiliza nodos y relaciones directas entre ellos.

    Los grafos son ideales para representar relaciones complejas entre entidades, como redes sociales, rutas de navegación, sistemas de recomendación, etc. Intentar modelar esto en una base de datos relacional requeriría una cantidad significativa de tablas y relaciones complejas, lo que podría llevar a consultas ineficientes y dificultades para mantener la coherencia de los datos.

3. ¿Qué es una base de datos orientada a grafos? Explique casos de uso.

    Una base de datos orientada a grafos es un tipo de sistema de gestión de bases de datos diseñado específicamente para trabajar con estructuras de datos de grafos. En un grafo, los datos se representan como nodos y relaciones que conectan estos nodos.

    Casos de uso:
    - **Redes Sociales:** Las plataformas de redes sociales pueden representarse de manera natural como grafos, donde los usuarios son nodos y las relaciones de amistad o seguimiento son aristas.

    - **Rutas y Sistemas de Navegación:** En aplicaciones de mapas y navegación, los nodos pueden representar ubicaciones y las aristas las conexiones entre ellas (caminos, carreteras, etc.).

    - **Gestión de Conocimiento y Sistemas de Recomendación de Contenido:** Para organizar y relacionar contenido, como artículos, videos y otros recursos.

### Referencias
Oracle. (s.f.). Definición de base de datos orientada a grafos. Recuperado el 1 de octubre del 2023, de https://www.oracle.com/pe/autonomous-database/what-is-graph-database/