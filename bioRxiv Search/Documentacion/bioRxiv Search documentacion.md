# BioRxiv Search documentación

## Descripcion

BioRxiv Search es un motor de busqueda de articulos cientificos de Covid19 utilizando la base de datos Elasticsearch y el repositorio de descripciones de articulos cientificos BioRxiv.

## Diagramas

A continuacion, se presenta el diagrama de flujo y el diagrama de rquitectura de BioRxiv Search.

### Diagrama de Flujo

El siguiente diagrama describe el proceso realizado por el BioRxiv Search.

![Diagrama Flujo](src/DiagramaFlujo.jpg)

### Diagrama de Arquitectura

El siguiente diagrama muestra la implementacion e interaccion de los componentes del BioRxiv Search. Asi como el flujo de datos dentro del sistema.

![Diagrama Arquitectura](src/DiagramaArquitectura.jpg)

## Pre-instalación

Como pre-instalación del proyecto sern necesarias las siguientes aplicaciones:

- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Helm](https://helm.sh/docs/intro/install/)

[Kubernetes](https://docs.docker.com/desktop/kubernetes/) será implemetado mediante la habilitación del cluster de docker.

## Instalación

blablbal

## Descripción de Componentes

### Elasticsearch
[Elasticsearch](https://www.elastic.co/elasticsearch/) es un motor de búsqueda y análisis de datos. Está diseñado para almacenar, indexar y buscar grandes volúmenes de datos en tiempo real. Utiliza una estructura basada en JSON.

#### Implementación Elasticsearch

blahblahblah

### Kibana

[Kibana](https://www.elastic.co/kibana), por otro lado, es una plataforma de visualización y análisis de datos, esta permite crear visualizaciones interactivas y paneles de control para explorar y analizar los datos almacenados en Elasticsearch.

#### Implementación Kibana

blahblahblah

### RabbitMQ
[RabbitMQ](https://www.rabbitmq.com) es un software de intermediación de mensajes que se utiliza para gestionar colas de mensajes entre diferentes aplicaciones o componentes de software. 

#### Implemantación RabbitMQ

blahblahblah

### Spacy Entity Extractor

El Spacy Entity Extractor tiene la funcionalidad de leer los mensajes publicados por el componente API Crawler en una cola de RabbitMQ. Posteriormente, realiza un Named Entity Recognition, donde estas entidades se almacenaran en un nuevo campo de tipo Array llamado entities, en un indice llamado augmented.

#### Implemantación Spacy Entity Extractor

 A continuacion, se muestra al implementacion del componente Spacy Entity Extractor.

![Spacy Code Section 1](src/SpacyCode1.PNG)

![Spacy Code Section 2](src/SpacyCode2.PNG)

![Spacy Code Section 3](src/SpacyCode3.PNG)

### Controller

Este componente cumple con la funcion de revisar continuamente el indice, en el momento que detecta este documento, hace un llamado al API de bioRxiv, capturando el valor llamado messages.total. Con esto el controller genera varios splits, los mismos son una porcion de los articulos que se deben descargar. Y por cada split publica un mensaje en RabbitMQ.

#### Implemantación Controller

 A continuacion, se muestra al implementacion del componente Controller.

![Controller Code Section 1](src/ControllerCode1.PNG)

En la figura anterior se encuenta la implementacion del metodo get_biorxiv_data. El cual se encarga de hacer un request al API de bioRxiv y retornando el response en caso de recibir un response status code igual 200.

![Controller Code Section 2](src/ControllerCode2.PNG)

Posteriormente, se define las variables de entorno necesarios para establecer las conexiones tanto de elasticsearch como de rabbitMQ. Ademas, se inicializa la connecion al elasticsearch.

![Controller Code Section 3](src/ControllerCode3.PNG)

En esta seccion se crea el indice de jobs para el cliente de elasticsearch, tal como se indica en el codigo.

![Controller Code Section 4](src/ControllerCode4.PNG)

Finalmente, un ciclo donde se va a procesar el valor de messages.total y se generan lo splits para publicarlos en la cola de RabbitMQ.

### API Crawler

El API Crawler es el componente encargado de leer los mensajes publicados en el RabbitMQ provenientes del Controller. Ademas, este se encarga de descargar los archivos de API bioRxiv y los almacena en un indice de ElasticSearch llamado raw. Y al finalizar publica un mensaje en una cola de RabbitMQ.

#### Implemantación API Crawler

 A continuacion, se muestra al implementacion del componente API Crawler.

![Crawler Code Section 1](src/CrawlerCode1.PNG)

En la figura anterior se encuenta la implementacion del metodo get_biorxiv_data. El cual se encarga de hacer un request al API de bioRxiv y retornando el response en caso de recibir un response status code igual a 200.

![Crawler Code Section 2](src/CrawlerCode2.PNG)

Posteriormente, en esta figura semuestra la implementacion del metodo callback. El cual se encarga de leer los mensajes de RabbitMQ provenientes del Controller, hace un request al API de bioRxiv para obtener los articulos y los prepara para publicarlos en la cola SPACY_QUEUE.

![Crawler Code Section 3](src/CrawlerCode3.PNG)

Finalmente se definen las variables de entorno para la configuracion de la conexion con rabbitMQ y elasticsearch.

### SparkSQL

SparkSQl es el componente encargado de leer el indice augmented que se ejecutara de forma manual y aplicara ciertas transformaciones a los datos. Una vez transformados, este lo publicaraen un indice llamado documents.

#### Implemantación SparkSQL

Este componente no fue implementado.

## Ejecución

## Pruebas Realizadas

## Resultados Pruebas Unitarias

Respecto a las pruebas unitarias, debido al poco codigo generado durante el desarrollo del proyecto, unicamente se logran identificar 2 componentes a los cuales se les puede realizar un unit test. Los cuales seran mencionados mas adelante. Esto bajo la premisa de probar unicamente codigo generado para la implementacion dell "motor de busqueda" de articulos cientificos, omitiendo las funciones que generen conexiones con los distintos componentes del sistema.

### Controller

Referente al controller, este cuenta unicamente con un metodo, get_biorxiv_data. El cual se encarga de hacer un request al API de bioRxiv y retornar un response. El response retornado por get_biorxiv_data puede ser null o bien un json, esto depende del response status code proveneiente del API. Debido a que no podemos controlar el comportamiento del API de bioRxiv, no se puede generar casos de prueba sobre los posibles errores y se procede unicamente a validar el resultado proveniente del metodo anteriormente mencionado.

A continuacion, se muestra el codigo del unit test generado para el metodo del controller.

![Unit test Controller](src/TestController.PNG)

El resultado de esta prueba es positivo ya que funciona correctamente al ejecutar el sistema. En caso de rebir un status code diferente a 200 este indica el error.

### Crawler

Caso similar al controller, el crawler unicamente cuenta con 2 metodos, de los cuales solo el metodo get_biorxiv_data es sujeto para un unit test. Este se encarga de hacer un request al APi de bioRxiv y recibir un response con los articulos cientificos. El unit test para el mismo se presenta en la sigueinte figura.

![Unit test Crawler](src/TestCrawler.PNG)

El resultado de esta prueba es positivo ya que funciona correctamente al ejecutar el sistema. En caso de rebir un status code diferente a 200 este indica el error.

## Recomendaciones y Conclusiones

A continuacion, se presentan una serie de recomendaciones con el fin de un desarrollo mas eficiente de los componentes que forman parte de este sistema. Adicionalmente, se muestran una serie de conclusiones al momento de finalizar el proyecto.

### Recomendaciones

1. Mejorar el trabajo en equipo.
2. Una buena distribucion del trabajo.
3. Estudiar a profundidad cada una de las tecnologias a trabajar.
4. Invertir tiempo en aprender Kubernetes.
5. Establecer consultas periodicas con el profesor a cargo.
6. Establecer entregas periodicas.
7. Buena comunicacion de equipo.
8. Adecuada organizacion del GIT(repositorio).
9. Mejorar las practicas de programacion.
10. Realizar reuniones grupales periodicas donde todos los integrantes participen.

### Conclusiones

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. 

## Referencias

1. UnitTest — Unit Testing framework. (s. f.). Python documentation. https://docs.python.org/3/library/unittest.html
2. UnitTest — Unit Testing framework. (s. f.-b). Python documentation. https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertEqual
