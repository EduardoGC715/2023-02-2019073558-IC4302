# BioRxiv Search documentación

## Pre-instalación
Como pre-instalación del proyecto sern necesarias las siguientes aplicaciones:
- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Helm](https://helm.sh/docs/intro/install/)
- [Lens](https://k8slens.dev)

[Kubernetes](https://docs.docker.com/desktop/kubernetes/) será implemetado mediante la habilitación del cluster de docker.

## Instalación
Para la instalación del cluster de kubernetes es necesario ejecutar los siguientes comandos en el Git Bash: 

- `helm repo add elastic https://helm.elastic.com`
- `helm repo add bitnami https://charts.bitnami.com`
- `helm repo update`
- `cd bootstrap`
- `rm -rf Char.lock`
- `helm dependency build --skip-refresh`
- `cd ../stateful`
- `rm -rf Char.lock`
- `helm dependency build --skip-refresh`
- `cd ..`

Estas lineas de comando lo que realizan es importar los repositorios de bitnami y elastic search que son necesario para la instalacion de sus debidos componentes e instalar las dependencias de cada Helm chart. En seguida se continuará con la instalación de los componentes, empezando con el bootstrap el cual instala el elastic operator:

- `helm upgrade --install bootstrap bootstrap`

Una vez se instala el bootstrap ejecutar el siguiente comando para instalar el stateful, el cual consiste en kibana, elasticsearch y rabbitMQ:
- `helm upgrade --install stateful stateful`

Una vez se finaliza de instalar el stateful (se puede verificar con `kubectl get pods` y verificando que todos los pods esten listos, o se puede verificar mendiante la aplicación de Lens) se procede a instalar el stateless el cual corresponde a el controller, API crawler y el Spacy.

- `helm upgrade --install stateless stateless`

Una vez finalizada la instalación se pueden realizar las pruebas de funcionamiento definidas en la sección de Ejecución y Pruebas Realizadas.

## Descripción de Componentes

### Elasticsearch
[Elasticsearch](https://www.elastic.co/elasticsearch/) es un motor de búsqueda y análisis de datos. Está diseñado para almacenar, indexar y buscar grandes volúmenes de datos en tiempo real. Utiliza una estructura basada en JSON. Este es la base de datos principal donde se guardarán los datos extraidos del API de BioRxiv.

#### Implementación Elasticsearch
Elasticsearch fue implementado mediante el uso de helm charts, en la dirección: [template elasticsearch](/bioRxiv%20Search/charts/stateful/templates), se encuentra el template de creación de Elasticsearch, y fuera de esta carpeta se encuentra el archivo de [Values.yaml](/bioRxiv%20Search/charts/stateful/values.yaml) donde se especifica los valores que debe tomar el template. Es importante notar que dentro del [elastic.yaml](/bioRxiv%20Search/charts/stateful/templates/elastic.yaml) se encuentra definido el stateful set de elasticsearch y el servicio tipo nodeport que expone el puerto del pod (9200) a la maquina (localhost) en el puerto 30090.

### Kibana

[Kibana](https://www.elastic.co/kibana), por otro lado, es una plataforma de visualización y análisis de datos, esta permite crear visualizaciones interactivas y paneles de control para explorar y analizar los datos almacenados en Elasticsearch. Este será utilizado para la interacción con Elasticsearch por parte de los usuarios.

#### Implementación Kibana
Elasticsearch fue implementado mediante el uso helm charts, en la dirección: [template kibana](/bioRxiv%20Search/charts/stateful/templates), se encuentra el template de creación de Kibana, y tambien se encuentra el archivo de [Values.yaml](/bioRxiv%20Search/charts/stateful/values.yaml) donde se especifica los valores que debe tomar el template. Es importante notar que dentro del [kibana.yaml](/bioRxiv%20Search/charts/stateful/templates/kibana.yaml) se encuentra definido el replica set de kibana y el servicio tipo nodeport que expone el puerto del pod (5601) a la maquina (localhost) en el puerto 30091, por lo que para acceder a kibana es necesario ingresar a localhost:30091.

### RabbitMQ
[RabbitMQ](https://www.rabbitmq.com) es un software de intermediación de mensajes que se utiliza para gestionar colas de mensajes entre diferentes aplicaciones o componentes de software. Este será utilizado para enviar mensajes entre los componentes para que realicen sus tareas definidas.

#### Implemantación RabbitMQ
RabbitMQ fue implementado como una dependencia en el archivo de [Charts.yaml](/bioRxiv%20Search/charts/stateful/Chart.yaml), la instalación de este es de manera "default" ya que no se especifican valores para sus parametros. Este pod permanece activo durante la ejecucion y son los diferentes componentes los que crean y consumen las colas (esto se verá mas a fondo en la descripción de cada componente).

### Spacy Entity Extractor

#### Implemantación Spacy Entity Extractor
blahblahblah

### Controller

#### Implemantación Controller
blahblahblah

### API Crawler

#### Implemantación API Crawler
blahblahblah

### SparkSQL

#### Implemantación SparkSQL
blahblahblah

## Ejecución y Pruebas Realizadas
Para iniciar con las pruebas debe de haber sido necesario realizar el proceso de pre-instalación e instalación para el cluster de kubernetes. Una vez se tiene todo listo se puede iniciar.

El primer paso es acceder a kibana mediante el NodePort: [Kibana](https://localhost:30091) e ingresar las credenciales, el usuario predeterminado es **elastic** y la contraseña se puede accesar por medio de Lens en el apartado de *Config* en el apartado de *Secrets* bajo el nombre de **ic4302-es-elastic-user**.

Una vez se ingresa a Kibana se abre el menú y se abre el apartado de *Management* bajo el nombre de *Dev Tools* para acceder a la consola de Kibana.

kibana image 1

En la consola se ejecutará el siguiente comando el cual en el índice de jobs ingresa un nuevo job con el formato especificado:

kibana image 2

Una vez se ingrese el nuevo job, el controller verificará este indice de *jobs* y se dará cuenta que debe de enviar los splits con el mensaje a una cola de RabbitMQ. El crawler entonces empieza a consumir estos mensajes y empieza a extrar la información cruda del BioRxiv API y la guarda en un índice llamado raw, esto se puede verificar con el siguiente comando:

kibana image 3

Una vez que se van extrayendo los datos, el crawler va publicando mensajes en otra cola para que el Spacy los detecte y empiece con el Named Entity Recognition y guarde las nuevas entidades en un índice que se llama *augmented*, esto se puede verificar con el siguiente comando:

kibana imaage 4

Finalmente como ultimo proceso de verificación se ejecutará el código de SparkSQL con Scala.TODO

## Resultados Pruebas Unitarias

## Recomendaciones y Conclusiones (10)

## Referencias
