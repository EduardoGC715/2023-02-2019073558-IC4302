### José Eduardo Gutiérrez Conejo - 2019073558 
### Bases de Datos II
### Lectura 3: 7 NoSQL Considerations

1. ¿Es posible utilizar una base de datos SQL como una base de datos key-value?, ¿Cómo la implementaría? Comente las implicaciones de rendimiento

   Sí es posible, pero esta implementación trae varias consecuencias. Para implementarlo se puede diseñar una tabla con columnas para clave y valor, lo que podría facilita la inserción y recuperación de datos, pero este enfoque carece de restricciones de integridad referencial y puede tener un rendimiento menos eficiente en comparación con las consultas en tablas relacionales. Además, a medida que la cantidad de datos crece, la eficiencia puede disminuir.

2. ¿En qué consisten los datos polimórficos? Explique la razón por la cual estos son un buen caso de uso en bases de datos documentales.

    Los datos polimórficos se refieren a la capacidad de un elemento o campo para contener diferentes tipos de datos o estructuras de datos en función del contexto. Esto significa que un mismo elemento o campo puede representar diferentes tipos de información según la situación.

    En bases de datos no SQL utilizar este concepto es bueno ya que trae los siguiente beneficios:

    - Flexibilidad en la Estructura de Datos: Permiten que un campo o documento pueda contener diferentes tipos de datos sin necesidad de una estructura fija.

    - Manejo de Datos Variados: Los datos polimórficos pueden facilitar el almacenamiento y recuperación de información sin requerir una estructura de tabla rígida.

    - Reducción de la Complejidad: Al permitir que los campos sean polimórficos, se reduce la complejidad de diseñar y mantener una estructura de base de datos fija.

    - Adaptabilidad: Los datos polimórficos son útiles cuando se trata de datos que evolucionan con el tiempo o cuando se necesita una rápida adaptación a nuevas necesidades.

3. Presente 5 ejemplos de sistemas/casos de uso que podrían soportar consistencia eventual, Explique
Sistemas de Redes Sociales:

    - En redes sociales donde la principal prioridad es obtener el contenido de los usuarios. Las interacciones de los usuarios con el sistema pueden ser propagados al sistema de uan forma evetual hasta llegar a un estado consistente.

    - En plataformas de tipos blog o foros se puede utilizar consistencia eventual ya que los comentarios o posts pueden propagarse de forma eventual sin mayor riesgo.

    - En sistemas de procesamiento de big data, como Hadoop o Spark, donde se manejan grandes volúmenes de datos, la consistencia eventual puede ser aceptable en algunos casos, siempre y cuando los resultados finales sean precisos.

    - En juegos multijugador en línea donde la prioridad es mantener la experiencia del juego fluida y sin retrasos. Los eventos del juego pueden propagarse de forma asincrónica y lleagr a un estado consistente con el paso del tiempo.

    - En sistemas de registro y auditoría la consistencia eventual es aceptable siempre y cuando los registros eventualmente se sincronicen.

4. ¿Por qué es importante que nativamente una base de datos NoSQL implemente un REST API?

    Cuando se desarrolla un servicio backend construyendo un API, se puede asegurar que cualquier sistema o cliente se pueda conectar a dicho backend. El API lo que reliza es devolver datos, que están desacoplados a cualquier modo de visualización. Si se está desarrollando una página web, el API se consume desde cualquiera de los frameworks o librerías Javascript y también se podrán consumir los servicios del API desde aplicaciones desarrolladas en Java, Swift, C entre otros. Este REST simplifica mucho el funcionamiento, dado que se elimina todo lo relacionado al estado de la aplicación.

5. ¿Por qué la geo localización de la bases de datos NoSQL pueden ayudar a mantener leyes de Data sovereignty?
   
    La localización puede ayudar a mantener leyes de Data sovereignity de las siguientes maneras:

    - Cumplimientos Legale y Regulatorios: Ciertas jurisdicciones requieren que los datos de sus ciudadanos se almacenen en su país, lo que al utilizar bases de datos NoSQL con capacidades de geolocalización, se puede asegurar que los datos estén almacenados en el país o región correspondiente.

    - Protección de Privacidad y Seguridad: Al mantener los datos dentro de una jurisdicción específica, se reduce el riesgo de acceso no autorizado o violaciones de privacidad.

    - Reducción de la Latencia: Al tener los datos almacenados cerca de los usuarios, se reduce la latencia en la recuperación y procesamiento de la información.

    - Protección contra riesgos de transmisión internacional: Cuando los datos cruzan fronteras existe un riesgo de exposición o interceptación no autorizada durante la transmisión.

### Referencias

Whiteside, J. (Junio 12 del 2023). Inheritance and polymorphism: Where the cracks in SQL begin to show. Vaticle. Recuperado el 9 de setiembre de 2023, de https://blog.vaticle.com/inheritance-and-polymorphism-where-the-cracks-in-sql-begin-to-show-a795701af90e

IONOS (s.f.). Data Sovereignty. Digital Guide IONOS. Recuperado el 9 de setiembre de 2023, de https://www.ionos.es/digitalguide/servidores/seguridad/data-sovereignty/

Arsys (Agosto 31 de 2016). API REST: La mejor manera de proyectar un backend. Programación y BBDD. Recuperado el 9 de setiembre de 2023, de https://www.arsys.es/blog/proyectar-un-backend-hoy