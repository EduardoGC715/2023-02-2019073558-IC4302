### José Eduardo Gutiérrez Conejo - 2019073558 
### Bases de Datos II
### Lectura 3: 7 NoSQL Considerations

1. ¿Es posible utilizar una base de datos SQL como una base de datos key-value?, ¿Cómo la implementaría? Comente las implicaciones de rendimiento

   Sí es posible, pero esta implementación trae varias consecuencias. Para implementarlo se puede diseñar una tabla con columnas para clave y valor, lo que podría facilita la inserción y recuperación de datos, pero este enfoque carece de restricciones de integridad referencial y puede tener un rendimiento menos eficiente en comparación con las consultas en tablas relacionales. Además, a medida que la cantidad de datos crece, la eficiencia puede disminuir.

2. ¿En qué consisten los datos polimórficos? Explique la razón por la cual estos son un buen caso de uso en bases de datos documentales.

    Los datos polimórficos se refieren a la capacidad de un elemento o campo para contener diferentes tipos de datos o estructuras de datos en función del contexto. Esto significa que un mismo elemento o campo puede representar diferentes tipos de información según la situación.

    En bases de datos no SQL utilizarl este concepto es bueno ya que trae los siguiente beneficios:

    - Flexibilidad en la Estructura de Datos: Permiten que un campo o documento pueda contener diferentes tipos de datos sin necesidad de una estructura fija.

    - Manejo de Datos Variados: Los datos polimórficos pueden facilitar el almacenamiento y recuperación de información sin requerir una estructura de tabla rígida.

    - Reducción de la Complejidad: Al permitir que los campos sean polimórficos, se reduce la complejidad de diseñar y mantener una estructura de base de datos fija y extensa.

    - Adaptabilidad: Los datos polimórficos son útiles cuando se trata de datos que evolucionan con el tiempo o cuando se necesita una rápida adaptación a nuevas necesidades.

    - Facilita Consultas Expresivas: En una base de datos documental, los datos polimórficos permiten consultas expresivas que pueden adaptarse a la variabilidad de los datos, lo que facilita la extracción de información de manera más natural.

3. Presente 5 ejemplos de sistemas/casos de uso que podrían soportar consistencia eventual, Explique
Sistemas de Redes Sociales:

    En redes sociales, donde la prioridad es la disponibilidad de los contenidos para los usuarios. Los 'me gusta', comentarios y publicaciones pueden propagarse asincrónicamente y eventualmente llegar a un estado consistente.

    Plataformas que permiten a los usuarios comentar en blogs o artículos pueden usar consistencia eventual. Los comentarios pueden enviarse a través de nodos distribuidos.

    En sistemas de procesamiento de big data, como Hadoop o Spark, donde se manejan grandes volúmenes de datos, la consistencia eventual puede ser aceptable en algunos casos, siempre y cuando los resultados finales sean precisos.

    En juegos multijugador en línea, la prioridad es mantener la experiencia del juego fluida y sin retrasos. Los eventos del juego pueden propagarse asincrónicamente y converger hacia un estado consistente en el tiempo.

    En sistemas de registro y auditoría, donde se mantienen registros de eventos o transacciones, la consistencia eventual puede ser aceptable siempre y cuando los registros eventualmente se sincronicen

4. ¿Por qué es importante que nativamente una base de datos NoSQL implemente un REST API?


5. ¿Por qué la geo localización de la bases de datos NoSQL pueden ayudar a mantener leyes de Data sovereignty?


### Referencias

Whiteside, J. (Junio 12 del 2023). Inheritance and polymorphism: Where the cracks in SQL begin to show. Vaticle. Recuperado el 9 de Agosto del 2023, de https://blog.vaticle.com/inheritance-and-polymorphism-where-the-cracks-in-sql-begin-to-show-a795701af90e