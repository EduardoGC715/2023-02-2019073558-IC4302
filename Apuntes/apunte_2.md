# Apuntes Clase 19/09/23
## José Eduardo Gutiérrez Conejo - 2019073558

## Fix del error out of shape
En Oracle Cloud se van a Shape y copian VM.Standard3.Flex y se van al vm.tl-pi (workspace) y lo copian en la línea donde está el VM. Standard.A1.Flex, cambiándolo. Abajo en Shape_confi pueden cambiarle el número de memory _in_gbs ya sea por 4 o el que ustedes gusten para manejar el tamaño. 
Esto va a causar inmediatamente se que ustedes puedan crear una máquina, tomando como ejemplo la pagina ORACLE cloud en donde ustedes pueden rebajar $36 de los $300 que se tenían disponibles, teniendo el crédito gratis. 
Una vez hayan recolectado la información van y terminan esa instancia que crearon para obtener los valores correctos. Una vez hecho esto ya van a tener sus máquinas creadas cuando tiene el problema de que no hay capacidad cuando están creando las máquinas. 
Otra cosa que tener presente es que en el código que el profesor les paso a ustedes (Docker/helloflask), ahí se van a encontrar que la imagen que estamos utilizando (arm64v8) lo que quiere decir es que cuando nosotros venimos y seleccionamos el shape de la imagen de la instancia, este tipo de instancia llamada AMPERE va a hacer es utilizar una arm64v8, ya que esa es la arquitectura que utiliza. 
Ahora, cuando va a la página AMPERE y seleccionan Browse all shapes, la sección Intel y AMD, ambas no utilizan esa arquitectura, entonces en este caso específico, al hacer una maquina basada n INTEL o AMD, este código que el profesor les brindó lo deben de ajustar para que funcione con la arquitectura que se seleccionó. 
En este caso deben de irse a Docker Hub, ingresando y buscando Python seleccionando al final de la página Supported Arquitecture, encontrando la arquitectura arm64v8 (la que usa con INTEL y AMD), cambiando igualmente la imagen base a como viene por ahí. 
Esto quiere decir que en Dockerfile se le debe de quitar el arm64v8, dejando solo pyhon.3.11.5-slim-bullseye, asegurándose que esta versión se encuentre disponible en la sección Simple Tags de la página de Python, causando como consecuencia que inmediatamente que cuándo copilemos el código Python, el código pueda correr correctamente en la arquitectura seleccionada. 
Cabe destacar que esto se hará solo si no hay arquitectura Ampere disponible (gratis), intentando crear primeramente maquinas AMP ($26) y sino Intel ($36). Igual ustedes tienen un crédito hasta final de semestre para gastarlo. 

### Preguntas generales del proyecto 

El profesor menciona que se descarguen los archivos que vienen con multistream. Mulistream index y p*p*, el cual da un rango de páginas. Con esto del rango de paginas se deben de asegurar que el archivo que bajan es contenga al menos una porción de las páginas. 
En el caso de Latest-abstract puedenen descargar el primero (latest-abstract vml.gr), en este caso, este archivo no es necesario si utilizan la relación de multistream*xml -p*p*
De igual manera, cuando ustedes creen su infraestructura, van a encontrarse con un Bucket que va a tener un nombre que ustedes le asignen (este se crea en storage_object .tf) y ahí es donde ustedes van a subir los archivos de Wikipedia. 
No deben de ir a Create Autonoumous database y crear uno nuevo, porque sino deben de leerse toda la documentación, para eso el profesor ya les brindó uno para que trabajen. 
Para correr el código brindado tienen que ejecutar el código de la sección requirements. Txt dentro de la máquina de Oracle y correrlo dentro de la máquina de Oracle, en caso de correrlo dentro de la maquina local deben de tener habilitado el edit Access control list y darle click a add my IP adress. 

### Retomando la clase
MISPM (o era Mysol) y poscres son muy similares, con algunas diferencias, más que todo en el tema de nomenclatura. MISPM nos da la opción de tener una base da datos más que todo en memoria. 

QL server 
Copia muchas de las formas de replicación y alta disponibilidad de otros all proveider. 

Vamos a tener mecanismos:  

1.	Always on hability group: permite tener una copia que siempre va a ser primaria (no puede haber uno multiprimer) teniendo varias replicas que pueden ser hot o warm replicas. Esta cantidad de replicas está determinado por la clasificación de modo estándar (2 réplicas conocidos como basic) y enterprice (9 réplicas comportándose como hot replicas) 
*warm replicas: solo reciben los datos y los aplican y no sirven para hacer lecturas. 
*Hot replicas: si hacen lecturas. 
En este caso, uno escoge cual usar dependiendo si se tiene consistencia eventual, que es cuando el sistema puede soportar que en algún momento un cliente quiere información diferente de la que está viendo el cliente. 
Volviendo al Always on hability group, este funciona de dos formas: una Sync (envió las transaccionesde una instancia a otra y se espera que se confirme que existió un comit, esto quiere decir que se debe de hacer un rite en la réplica para confirmar al servidor que la transacción fue recibida si y solo si la transacción que escrita en disco (log), ya que esto nos confirma que si todo lo demás se cae, la información sigue estando guardada) y Asyc (envió la transacción y digo que fue enviada sin tener seguridad de que fue escrita en el log).  
Ambos Sync o Asyc funcionan a nivel de bases de datos, por lo que si uno pierde un servidor y está conectada se va a perder las bases de datos. 
Va a tener un fairlover automático o puro y manual. 
Otra ventaja de Always on hability group es que se puede desplegar en varias data center, loque quiere decir es que los servidores van a estar lejos en términos geográficos implicando que se deben de mover sobre una red, por lo que el modelo de envío de transacciones y sincronización se va a complicar un poco; ya que cuando uno se muevo sobre una red no local puede tener un retraso, conocido como el tiempo round robin que tarda la información desde salir de una máquina, llegar y recibir contestación de eso. 
En este caso, cuando manejamos el envío de transacciones de forma síncrona (Sync), esto puede causar retrasos a nivel de aplicación, es importante mencionar que normalmente este tipo de configuraciones no se hace.  Al manejar esto en la nube hace que mejore, ya que el tiempo disminuya. 

### Pacemaker  
Hace que se refieran a una pieza de software que se comunica con los servidores, haciendo que pregunte a los servidores si están bien. Cuando se detecta que algo no está bien, entonces se toman acciones, que quiere decir que se notifica a alguien se hace el switch automático. 
No se es bueno ponerlo dentro de servidores de bases datos. 

### Business continuity 

Como yo voy a planear la arquitectura de las bases de datos para maximizar la alta disponibilidad, esto es por una estrategia de recuperación de desastres. 

Sacle Read replicas 
Lo que se ve en servidores SQL. 

2.	Always on fairlover cluster: va a utilizar una tecnológica de Microsoft llamada Windows hey fairlover cluster, para definir un servidor (Windows server)
Un Windows server se puede instalar un Wsfc, instalando algún tipo de proceso que va a permitir hacer sincronizaciones (sincronización de archivos, talover) a nivel de servidores. 
También se van a implementar los servicios de peace maker y virtual IPs y sincronización de configuración. Esto quiere decir que si instalo un servidor SQL, esto se va a replicar en el otro servidor, permitiendo que ambos servidores sean un espejo el uno del otro, en todo nivel. 
Por lo que el fair lover cluster va a replicar toda la instalación del SQL server y o solo a nivel de bases de datos. 
También se tiene el job agent que dentro del mundo de SQL server es una forma de hacer tareas programas y orquestar tarea, quiere decir que uno puede decirle al SQL server que ejecutar con horarios y fechas programadas (calerandiza tareas y da un flujo de ejecución). 
Linked servers que lo que va a hacer es que yo voy a agarrar dos instalaciones del SQL server, por lo que se puede hacer un link entre los dos servidores y permitir replicar alguna información de eso sin entrar en un Cluster o alguna cuestión así. 
Fairlover manual, es levantar un servidor, por lo que cuando un servidor este corriendo el otro toma un archivo del shared storage, entonces si alguien levanta uno va a haber un conflicto porque ambos van a pelear con el shared sotrage, por eso siempre debe de hacer uno detenido y otro en primario para que no haya conflictos. Por lo que si uno se cae, siempre va a tener el otro en espera para poder probarlo y ver si funciona todo bien. 

Log shipping: mandamos transacciones de un servidor a otro. 
El que se encarga de correrlo es el SQL 
Siempre se debe de hacer un cambio de un primary a un stand by o al revés. 
