# Bases de Datos II
# Tarea Corta 2  
#### Equipo de trabajo:
Granados Retana, Diego - 2022158363
Granados Retana, Daniel - 2022104692
Mora Montes, Diego - 2022104866
Gutierrez Conejo, Eduardo - 2019073558
Cardona Quesada, Jose Ricardo - 2021022613



---
## Manual de instalación

A continuacion se presenta un manual de instalacion para distintos motores de bases de datos junto con respectivos codigos para implementar backups y restaurar datos a través de una cuenta AWS.

#### Paso 1. Selección del Motor de Bases de datos a probar

Dentro de la carpeta para la TC2 se incluyen varios motores de bases de datos, la lista de todos estos es:


• MariaDB
• PostgreSQL
• Elasticsearch
• MongoDB
• Neo4J
• CouchDB

Una vez se haya seleccionado la base de datos para la que se desea probar backups y restauración se hace lo siguiente:

Se ingresa al path `TC2\helm\databases\values.yaml` donde se va a cambiar ciertos parámetros para hacer backups solo en la base deseada e iniciar solo la base deseada. Por cada base de datos saldrá el siguiente parámetro:

![Alt text](imgs/InicioTutorial.png)

Enabled hace referencia a si se quiere inicializar o no ese motor de base de datos, la recomendación es no correr más de uno al mismo tiempo.

En caso de querer correr ese motor cambiar `Enabled: True` por la versión actual, y al resto de motores ingresar `Enabled: False` para apagarlos

Una vez hecho esto se debe ingresar a  `TC2\helm\backups\values.yaml`, y hacer lo mismo con las bases de datos que aparecen. 

IMPORTANTE: En caso de querer ejecutar backups a través de elastic **NO es necesario** ingresar a `TC2\helm\backups\values.yaml` a habilitar la base también


# Aqui nose si falta algo para habilitar si se quieren backups o restores.


Finalmente, antes de ejecutar el código 


#### Paso 2. Ejecución del Código

Una vez se haya escogido la base, el siguiente paso es ejecutar los comandos para levantarla con sus respectivos parámetros, para esto ingresamos a cualquier terminal desde la cuál se puedan ejecutar comandos Linux. Una vez aqui abriremos la carpeta desde la terminal:

![Alt text](imgs/image.png)

Una vez en la carpeta donde hayamos descargado el proyecto se insertarán los siguientes comandos:

`cd TC2`
`cd helm`

Una vez aqui la terminal se encuentra en la carpeta donde se pueden ejecutar los archivos para la instalacion y desinstalación de las bases de datos.

##### Para Instalar la base deseada con los parámetros específicados

En la terminal primero se recomienda ejecutar:

`dos2unix install.sh`

Seguido de esto ejecutamos el comando: `./install.sh`

Una vez hecho esto la terminal comenzará a instalar todos los deployments necesarios para la ejecucuón correcta del programa:

![Alt text](imgs/install.png)

Una vez este código se verá lo siguiente:
![Alt text](imgs/terminalinstall.png)

Este código habilita la base deseada para las pruebas que se quieran ejecutar con ella. Cada una de las bases es distinta.

### Ejecución de Bases y pruebas

#### IMPORTANTE

Para poder verificar si los archivos correspondientes a una de las bases se encuentran en el bucket, se puede hacer lo siguiente:

En la terminal, con el proyecto abierto, nos aseguramos de volver a la carpeta TC2 y en caso de estar adentro de Helm, hay que regresar. Para esto, se ejecuta el comando `cd ..` hasta regresar a la dirección del TC2.

Una vez en esta dirección,se ejecutan los comandos:

`cd utils`

`dos2unix install.sh`

`./install.sh`

Este código va a instalar un pod en la red de kubernetes donde se pueden ejecutar comandos para verificar si el bucket tiene archivos en la dirección que se quiere revisar. Al finalizar se podrá ver lo siguiente:

![Alt text](imgs/BackupElastic/debugpod.png)

Aqui se pueden ingresar comandos para ver las distintas direcciones donde estan almacenados los backups, normalmente estas direcciones siguen el patrón:

**`2019073558 / [nombre base]`**

EJ:
**`
2019073558/elastic`**
**`
2019073558/postgresql`**

El comando para ver los archivos en esa dirección es:

**`aws s3 ls s3://tec-ic4302-02-2023/2019073558/[nombre Base]/`**

EJ:

**`aws s3 ls s3://tec-ic4302-02-2023/2019073558/postgresql/`**

**`aws s3 ls s3://tec-ic4302-02-2023/2019073558/elastic/`**

Al ejecutar estos comandos se puede ver lo siguiente:

![Alt text](imgs/BackupElastic/consultasAWS.png)


Claramente se despliegan los distintos backups que han sido creados hasta el momento para las respectivas bases.

#### Elastic Search con Kibana

A continuación se muestra una guía para hacer backups y restores en la base elasticsearch a través de su interfaz kibana. Para este paso se asume que ya se habilito la base y se ejecuto el script de instalación desde la terminal.

Lo primero que se debe hacer es tener instalada una aplicación para poder visualizar el kubernetes deployment y fácilmente obtener la informaión importante de los pods.

Para esta funcionalidad se recomienda hacer uso de **LENS**, el resto de esta guía se basará en el uso de esta aplicación para conectar los pods.

Desde Lens lo primero que haremos será entrar el deploymen de docker desktop y nos iremos a la sección de **`PODS`**, una vez aqui entraremos al siguiente pod:

![Alt text](imgs/BackupElastic/PortElastic.png)

Al abrir el pod se debe buscar la sección señalada a la derecha, esta contiene un link que nos permitirá acceder de forma local a la interfaz Kibana para interactuar con la base de datos elasticsearch.

Una vez se haya hecho forward del port y se haya ingresado al sitio aparecerá lo siguiente:

![Alt text](imgs/BackupElastic/loginelastic.png)

Se solicita un usuario y una contraseña para poder ingresar al servicio Kibana, para obtener estos datos volvemos a **LENS** y buscamos la sección:

`Config/Secrets`, una vez aqui abrimos el siguiente secret:

![Alt text](imgs/BackupElastic/LensUbicacion.png)

Una vez aqui buscamos los siguientes datos:

![Alt text](imgs/BackupElastic/passwordES.png)

Estos corresponden a mi usuario y contraseña de elastic search. Por lo tanto copio estas credenciales y las pongo en la interfaz. El usuario será elastic y la contraseña el otro valor.

Despúes de ingresar las credenciales correctamente saldra una imagen similar a esta:

![Alt text](imgs/BackupElastic/MainScreen.png)


En esta pantalla buscaremos la opcion stack management e ingresaremos
![Alt text](imgs/BackupElastic/OpcionManagement.png)


Una vez en esta interfaz, se busca la sección con el nombre **Snapshot and Restore**, en elastic los backups son llamados de esta forma.

Para restaurar o guardar backups lo primero es definir la dirección donde se van a guardar/obtener. Para esto se va a agregar el repositorio donde vamos a manejar nuestros backups de elastic, este hace referencia a la dirección del bucket de AWS y el cliente que vamos a usar para guardar los datos correspondientes a los snapshots. 

![Alt text](imgs/BackupElastic/addrepository.png)

Una vez aqui se selecciona `Register a repository`  para crearlo. Una vez adentro:

Seleccionamos el tipo de repositorio, en este caso debe de ser AWS S3 y se le pone el nombre que quiera al repositorio.

![Alt text](imgs/BackupElastic/AWS.png)

En la siguiente pantalla se solicitan los datos que le queremos poner al repositorio. En esta sección los únicos campos relevantes son:

![Alt text](imgs/BackupElastic/repoData.png)

En el campo Client ingresamos: `default`

En el campo bucket ingresamos: `tec-ic4302-02-2023`

En el campo Base path se debe ingresar: `2019073558/elastic` 

Es importante anotar este base path para posteriormente usarlo al definir la política para los backups.

El resto de campos para el repositorio se dejan por default y se finaliza la creación de este. El resultado de este proceso se verá similar a esto:

![Alt text](imgs/BackupElastic/repocreado.png)

---

#### Para hacer pruebas

Cabe aclarar que el repo será adonde guardemos los backups, pero aún no se ha creado ninguna política para crear backups o se han creado indices para los cuáles probar esto. Por lo tanto antes de seguir con el proceso de backups se van a insertar indices en la base elasticsearch manualmente, posteriormente se mostrará como hacer un backup con esta. Finalmente se borrarán los datos y se tratará de restauralos usando el snapshot.

Primero, para ingresar los datos a la base es necesario volver al menú principal de la interfaz de Kibana, una vez aqui buscamos la siguiente sección:

![Alt text](imgs/BackupElastic/Devtools.png)

Ingresamos a Dev Tools, y se presentará la siguiente interfaz:
![Alt text](imgs/BackupElastic/devInterface.png)

Aqui escribimos los siguientes comandos:

---
**PUT /indice-backup**

---
**POST /indice-backup/_doc
{
  "titulo": "Prueba Backups",
  "contenido": "Este documento es una prueba de backups",
  "integrantes": ["Granados Retana Diego", "Granados Retana Daniel","Mora Montes Diego","Gutierrez Conejo Eduardo","Cardona Quesada Jose Ricardo"]
}**

---
**GET /indice-backup/_search 
{
  "query": {
    "match": {
      "titulo": "Prueba Backups" 
    }
  }
}**

![Alt text](imgs/BackupElastic/insertData.png)

Una vez hecho esto se insertaron datos y un índice para el cuál podemos hacer backups


---

#### Snapshots

Para guardar snapshots de nuestra base completa o un índice en ella hay dos maneras, se puede hacer manualmente a través de comandos o automáticamente definiendo una política de guardado.

##### Método Manual
Para hacer un backup manualmente, desde la misma interfaz de Dev Tools se puede ingresar un comando como este:

**PUT /_snapshot/ [NOMBRE_REPOSITORIO] / [NOMBRE_SNAPSHOT]
{
  "indices": "[NOMBRE INDICE]",
  "ignore_unavailable": true,
  "include_global_state": false 
}**

Donde se reemplaza la dirección con el nombre del indice al que queremos tomar un snapshot. En este caso para el ejemplo se usara el siguiente:

**PUT /_snapshot/BackupsElastic/indice-backup_20231020
{
  "indices": "indice-backup",  
  "ignore_unavailable": true,
  "include_global_state": false 
}**

Para revisar que este snapshot se encuentra disponible en el repositorio y en AWS se puede revisar de dos maneras:

La primera opción es ingresar a la sección de Stack Management y Snapshot-Restore dentro de la interfaz de Kibana. Una vez aqui se verá lo siguiente:

![Alt text](imgs/BackupElastic/EjemploSnapshot.png)

Si se logro crear correctamente el snapshot, va a aparecer en esta sección. La segunda opción es a través de el debug-pod, como se menciona en la sección IMPORTANTE, previo a esta. Al utilizar el debug pod se puede observar el índice recién almacenado

![Alt text](imgs/BackupElastic/consultasAWS2.png)


#### Automático
El segundo método para hacer backups, es estableciendolos automáticamente a través de un policy, usando uno de estos, se pueden establecer la creación de backups cada cierto tiempo automáticamente, junto con un tiempo para el cúal cuando se pase sean eliminados automáticamente también.

Para esto en la misma sección de Snapshots and Restore dentro de la Interfaz de Kibana se accede a la sección de Snapshot and Restore y una vez ahi se entra a Policies/Create a Policy:

![Alt text](imgs/BackupElastic/restorePolicy.png)

Si se ingresa a esta Interfaz se le presenta al usuario con lo siguiente:


![Alt text](imgs/BackupElastic/creacionPolicy.png)

Aqui se solicitan los siguientes datos del usuario:

* **Policy Name:** Aqui se le pone un nombre a la política, este valor es a gusto del usuario
* **Snapshot Name:** En esta sección se le debe de poner un nombre a los snapshots que se van a almacenar, la plataforma automáticamente les agrega un identificador único al final
* **Repository:** Aqui se debe poner el nombre del repositorio previamente creado, si no se ingresa un repositorio válido no se creará la política
* **Schedule:** En esta parte se debe definir cada cuanto tiempo se quieren hacer backups de la plataforma, se puede definir si se quiere cada ciertas horas, dias, mes, etc.

Una vez se han ingresado los datos, se pasa a la siguiente página:

![Alt text](imgs/BackupElastic/dejarigual.png)

En esta sección no es necesario cambiar nada, es cuestión de dejarlo con sus configuraciones por default, esto va a guardar todos los indices de la base automáticamente, sin embargo, si se quiere guardar solo un índice

![Alt text](imgs/BackupElastic/backupsUnsoloIndex.png)

Se puede apagar esta configuración, aqui se pueden seleccionar los indices que si se quieran guardar, si tienen un check a la izquierda van a ser parte del snapshot, sino no se incluyen.

Se pasa a la siguiente página:

![Alt text](imgs/BackupElastic/eliminardespuesCiertoTIempo.png)

Esta es la sección final para crear un policy, aquí se puede definir **Si se quieren borrar los backups después de cierto tiempo, y si se quieren definir un mínimo a mantener**. A través de esta sección se puede configurar los puntos extra de la tarea, indicando la cantidad de días tras los que se quiere borrar los backups.

Finalmente, le damos next y se va a crear el policy en esta sección:

![Alt text](imgs/BackupElastic/CreatePolicy.png)

Confirmamos que los datos están correctos y se le da crear,como resultado, si se hizo bien debe de aparecer lo siguiente:

![Alt text](imgs/BackupElastic/ResultadoPolicy.png)

En este ejemplo solo se esta haciendo backup del index llamado: `indice-backup`

Despues de crear el policy y repositorio se van a crear backups automáticamente cada cierto tiempo dependiendo de lo definido al crear el policy.

![Alt text](imgs/BackupElastic/ExisteSnapshot.png)

Verificar si se subieron al AWS Bucket los backups
![Alt text](imgs/BackupElastic/Ev1Bups.png)

#### Restore

Para probar la restauración de datos usando Kibana, se deben haber hecho los pasos anteriores y al menos se debe tener:

* Un indice con datos
* Un Snapshot del Indice

Una vez se tienen esto, la forma más sencilla de probar es desde la sección DEV TOOLS de la interfaz de kibana, borrar el indice y tratar de restaurar sus datos usando el snapshot.

Si hacemos un GET del indice queda claro que si existe y sus datos son los siguientes:

![Alt text](imgs/BackupElastic/getindexP.png)

Ahora se procede a verificar que si existe un snapshot con ese index:

![Alt text](imgs/BackupElastic/RevisarSiexisteBackup.png)

Para esto se uso el comando: **`GET /_snapshot/BackupsElastic/_all`**

Una vez verificados ambos, se va a borrar el índice de la base de datos elasticSearch:
![Alt text](imgs/BackupElastic/deleteIndex.png)

Se utiliza el comando: **`DELETE /indice-backup`**

Revisando si todavía existen los datos usando GET, se obtiene:

![Alt text](imgs/BackupElastic/GetDEL.png)

##### Restauración

Una vez eliminado, hay dos maneras de restaurar el índice dentro de Kibana:

###### Comandos
La primera opción para restaurar el índice o la base es utilizando comandos y el nombre del snapshot que se quiere restaurar, el comando sería similar a esto:



**POST /_snapshot/[Nombre Repo]/[Nombre Snapshot]/_restore
{
  "indices": "[Indice a restaurar]",
  "include_global_state": false
}**

En el caso de nuestro ejemplo se ejecuta el siguiente comando:

**POST /_snapshot/BackupsElastic/indice-backup_20231020/_restore
{
  "indices": "indice-backup",
  "include_global_state": false
}**

![Alt text](imgs/BackupElastic/restore1.png)

Ahora si probamos el GET, deberían de volver a aparecer los datos del Index:

![Alt text](imgs/BackupElastic/Restore2.png)


###### Usando Interfaz Snapshot and Restore

La segunda opción para restaurar un índice eliminado es a través de la Sección Snapshot and Restore dentro de la Interfaz de Kibana en la sección de Stack Management. Una vez aqui buscamos lo siguiente:

![Alt text](imgs/BackupElastic/listaSnapS.png)


Aqui aparecerán todos los snapshots creados, ya sea que se crearon manualmente con comandos o a través de una política. Estos se encuentran en orden descendente del creado más reciente al más antiguo. Se recomienda usar snapshots más nuevos para regresar a un estado más reciente de la base de datos en caso de un fallo.

Se selecciona el snapshot que se quiera restaurar y se clickea para ver detalles de este. Una vez abierto podremos ver la opción de restaurar:

![Alt text](imgs/BackupElastic/restoreInterface.png)

Si seleccionamos esta opcíon se desplegará un menú interactivo de restauración donde se pueden seleccionar los indices del snapshot que se quieren restaurar, si se quieren mantener los mismos nombres para los indices o cambiarlos, etc. A continuación se presenta este menú:

![Alt text](imgs/BackupElastic/restoreInterface2.png)

Seleccionamos las configuraciones que se deseen aplicar al restore y se pasa a la siguiente página:

![Alt text](imgs/BackupElastic/restoreInterface3.png)

Se le da restore snapshot y listo, los datos de la base junto con los indices y configuraciones en el snapshot se restauraron a la base.

#### Pruebas Realizadas

Para las pruebas realizadas en elasticSearch, se crearon dos índices:

![Alt text](imgs/BackupElastic/Ejemplo1.png)

A continuación se presentan los comandos para crear los índices e insertar datos en cada uno:

---
#### pokemon-names

**PUT pokemon-names
{
  "mappings": {
    "properties": {
      "name": { "type": "keyword" }  
    }
  }
}** 

---
#####  >>>> Datos:

**POST pokemon-names/_doc
{
  "name": "Pikachu"
}**


**POST pokemon-names/_doc  
{
  "name": "Charmander"
}**


Consultando al indice se obtienen los datos:

![Alt text](imgs/BackupElastic/index1Backup.png)

El comando para consultar el índice es: **`GET pokemon-names/_search`**

---
#### pokemon-regions

**PUT pokemon-regions 
{
  "mappings": {
    "properties": {
      "region": { "type": "keyword" }
    }
  }
}**

---
#####  >>>> Datos:

**POST pokemon-regions/_doc
{
  "region": "Kanto" 
}**

**POST pokemon-regions/_doc
{
  "region": "Johto"
}**

Consultando al indice se obtienen los datos:

![Alt text](imgs/BackupElastic/index2Backup.png)


En base a estos índices se estableció una política que guarde los datos asociados a estos dos índices cada hora. La política es:

![Alt text](imgs/BackupElastic/snapshotspokemon.png)

Ahora se van a borrar los dos índices y tratar de restaurarlos a través de hacer 2 experimentos:

##### Se borran los índices:

**`DELETE pokemon-names`**

**`DELETE pokemon-regions`**

Probando obtener los datos:

![Alt text](imgs/BackupElastic/deletedregion.png)

![Alt text](imgs/BackupElastic/restoreI3.png)


##### Experimento #1 (Restaurar Un solo índice y el otro no)

![Alt text](imgs/BackupElastic/restoreEX1.png)

Se va a restaurar solamente el índice **pokemon-region** con el nombre **"pokemon-regions12"**

Haciendo el restore, se consultan ambos índices:

##### Consultando el índice pokemon-regions12

![Alt text](imgs/BackupElastic/restoreEX12.png)

##### Consultando el índice pokemon-regions

![Alt text](imgs/BackupElastic/res123.png)

Como se puede ver ahora se restauro el índice pokemon-regions con el nombre **pokemon-regions12.**

También se puede observar que al consultar el índice **pokemon-names**, ya no existe:


![Alt text](imgs/BackupElastic/restore43.png)

---

##### Experimento #2 (Restaurar ambos índices después de Experimento1)

Para este experimento se hace un restore normal del snapshot completo:

![Alt text](imgs/BackupElastic/restoreEX2.png)

Despúes de hacer esto, se puede observar en la sección de Restored dentro de la interfaz de Kibana lo siguiente:

![Alt text](imgs/BackupElastic/Evidencia_Restore.png)

Se muestran los archivos de los 3 índices restaurados, debido a que en el experimento 1 no se restauro el índice **`Pokemon-regions`** con el mismo nombre, se restauran 2 veces en vez de sobreescribir el índice restaurado previamente con la versión nueva del snapshot

Revisando **`Pokemon-regions`**
![Alt text](imgs/BackupElastic/restoreEX141.png)

**`Pokemon-regions12`**:

![Alt text](imgs/BackupElastic/restoreEX111.png)


Y si se trata de obtener **`Pokemon-names`**
![Alt text](imgs/BackupElastic/restoreEX122.png)

Como se puede ver, cuando se restaura un índice desde un snapshot, se está creando un índice nuevo a partir de una copia de seguridad. Si se restaura un índice con el mismo nombre que ya existía previamente, Elasticsearch sobreescribirá el índice existente con la versión restaurada desde el snapshot.

Sin embargo, si se restaura el índice con un nombre diferente al que tenía originalmente, Elasticsearch creará un nuevo índice con ese nuevo nombre, en lugar de sobreescribir.

#### CouchDB 

Para realizar la instalacion de CouchDB utilizamos la instalacion del [helm chart hecho por Apache](https://github.com/apache/couchdb-helm/tree/main/couchdb). 

Para realizar la instalación, se habilita en el `databases/values.yaml` y en `backups/values.yaml` en el folder de `helm` la opción de enabled para realizar la instalación de la base de datos deseada. 

En el archivo de `databases/values.yaml`, se indica la versión de la imagen que se va a utilizar en este caso la 3.3.2 , también se define el usuario y la contraseña que se van a utilizar para poder acceder a la base de datos y por último se va a generar un UUID (Universal Unique Identifier) necesario para la creación de la base de datos, este lo creamos aleatoriamente mediante el uso del link (https://www.uuidgenerator.net/api/version4). 

``` 
couchdb: 
  enabled: true 
  clusterSize: 1 
  adminUsername: "admin" 
  adminPassword: "admin" 
  image: 
    tag: 3.3.2 
  couchdbConfig: 
    couchdb: 
      uuid: $(shell curl -s https://www.uuidgenerator.net/api/version4 2>/dev/null | tr -d -) 
``` 

Si se desea realizar un backup, en el archivo de backups/values.yaml se pone `type: backup` en el campo de couchdb.config.type. Los backups de CouchDB se van a guardar en `s3://tec-ic4302-02-2023/2019073558/couchdb/`. El campo de schedule debe contener un horario válido para un [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/). En nuestra configuración, está configurado para correr dos veces al día, 1 vez a medio día y otra vez a media noche. El host va a tener la dirección de la base de datos de CouchDB dentro del cluster para que así pueda localizarlo y hacer el backup, la bd va a ser la base de datos ya definida de la cual se va a hacer el backup, el port va a ser el predefinido por el helm chart de CouchDB por el cual vamos a tener acceso al API. Y tenemos el user y password que van a ser los mismos que definimos previamente, por utlimo para el caso del restore se le indica un name, que va a ser el nombre del archivo en el cual se está guardando el backup que se quiera restaurar.  

``` 
couchdb: 
  enabled: true 
  config: 
    namespace: default 
    host: databases-couchdb.default.svc.cluster.local 
    db: "pokemon" 
    user: "admin" 
    password: "admin" 
    port: "5984" 
    bucketName: tec-ic4302-02-2023 
    path: 2019073558/couchdb 
    maxBackups: 3 
    name: couchdb-202310230113.json  
    schedule: "0 */12 * * *" 
    diskSize: 1 
    storageClass: hostpath 
    provider: aws 
    type: backup 
``` 
 
Luego se puede correr el script de `install.sh` en helm para correr el backup. 

Cuando se instala en modo “backup”, se crean dos objetos principales de Kubernetes: un CronJob que se va a ejecutar dos veces al día cada 12 horas, y un Job que se ejecuta de una vez y realiza el respaldo a la base de datos. Estos jobs van a ejecutar el script `TC2/helm/backups/scripts/couchdbB.sh`. Debido a que CouchDB no tiene definido ningún método para realizar los backups, hacemos uso del [API de CouchDB](https://docs.couchdb.org/en/latest/api/) para así extraer los documentos que contenga la base de datos y poder crear un respaldo de estos. Para realizar el backup utilizamos el siguiente metodo: 
``` 
URL="http://$COUCHDB_USER:$COUCHDB_PSW@$COUCHDB_HOST:$COUCHDB_PORT/$COUCHDB_DB/_all_docs?include_docs=true" 

curl -X GET "$URL" -H "Accept: application/json" | jq '{ docs: [.rows[] | .doc] }' > /couchdump/$DATE/couchdb-$DATE.json 
``` 

En donde de primero definimos el path que vamos a utilizar para hacer la llamada al API, en este caso utilizamos unas variables de entorno definidas con los datos del values.yaml, el endpoint que utilziamos es **db/_all_docs?include_docs=true**, el cual nos va a retornar todos los documentos de la base de datos que indiquemos para asi poder almacenarlos en un archivo .json, ya teniendo el path para el llamado utilizamos el metodo **curl** para hacer el llamado, en este indicamos que es un GET, y le definimos el url, e indicamos el tipo de dato que esperamos de vuelta, al mismo tiempo estamos utilizando el método **jq** para así cambiarle el formato al archivo de respuesta para así tenerlo en un formato que luego pueda ser utilizado para el recovery , y por ultimo le indicamos el path en el cual queremos que se almacene y el nombre del archivo que queremos que tenga.  

Finalmente, se utiliza la siguiente instrucción para subir el backup al bucket S3 de aws: 

`aws s3 cp /couchdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive` 

Este script crea backups dentro del S3 dentro de un archivo con la fecha de cuando se realizó el backup. 

En el caso del restore, es bastante similar al backup pero tiene ciertas diferencias, entre estas esta que se utiliza el endpoint del API **_bulk_docs** al cual se le da el archivo .json extraído del path y con el nombre indicado e inserta en la base de datos todos los documentos dentro de este archivo.  

##### Ejemplo de Backup y Restore: 

Para tener más control, podemos instalar los helm charts por separado. Primero, hay que installar bootstrap. Ubicándonos en el folder de helm, hacemos: 

`helm install bootstrap bootstrap` 

Luego, tras asegurarnos de que Couchdb está habilitado en el values.yaml de databases, hacemos: 

`helm install databases databases` 

Esto crea el pod de la base de datos. 

Una vez creado hacemos un port foward dentro de lens del puerto de couchdb para asi poder hacer uso del API en herramientas como Postman o Thunderclient.  

Con esto ya podemos hacer la creación de la base de datos y la inserción de los archivos mediante llamados al API, para este ejemplo los llamados utilizados son los siguientes.  

``` 
PUT http://127.0.0.1:50209/pokemon 

PUT http://127.0.0.1:50209/pokemon/001 

{"name": "Pikachu", "type": "Electric", "level": 25} 
``` 

Ya con información en la base de datos, podemos instalar el helm chart de backups para que el Job realice el respaldo: 

`helm install backups backups` 

Podemos ir a Lens y la sección de Jobs. Aquí podemos abrir la consola del pod y ver el progreso del script. Si sale un error de que no encuentra el script, hay que hacer la instrucción en la consola de y reinstalar el helm chart de backups: 

`dos2unix backups/scripts/postgresqlBackup.sh` 

Una vez creado el backup volvemos a Postman y eliminamos nuestros datos en este caso el llamado utilizado es: 

` DELETE http://127.0.0.1:50209/pokemon/001?rev=1-a11edc90c0d2388866469ce2f5235047` 

Donde el rev es autogenerado por CouchDB por cada registro, podemos ver cual es el rev de nuestro registro con el llamado: 

` GET http://127.0.0.1:50209/pokemon/_all_docs?include_docs=true ` 

Para realizar el restore, se escribe el nombre del backup generado, este lo recibimos cuando se ejecute el backup en el pod logs, este dato se agrega en el campo de name en el values.yaml de backups y cambiamos el type a restore. Tras hacer esto, podemos reinstalar el helm chart con: 

` helm uninstall backups `

` helm install backups backups `
 

Cuando está en modo restore, no crea un CronJob, solo ejecuta un Job. Por lo tanto, podemos ver el progreso del Job en la pestaña de Jobs en Lens: 

Al final, podemos saber que el Job terminó cuando la columna de Completions salga en 1/1. 

Ahora mediante el mismo llamado en Postman: 

` GET http://127.0.0.1:50209/pokemon/_all_docs?include_docs=true `  

Y con el response se puede observar que el restore ha sido exitoso. 

---

### Conclusiones y Recomendaciones

#### Conclusiones

* El uso de almacenamiento en la nube con AWS S3 facilita la escalabilidad y accesibilidad de los backups, pero requiere tomar en cuenta consideraciones adicionales de seguridad a la hora de hacer el código y mantener su versionamiento. 

* Si bien Elasticsearch requiere una configuración inicial más elaborada y el proceso para habilitar snapshots es más manual, una vez que se tienen los componentes configurados adecuadamente, la automatización de snapshots y restores resulta bastante sencilla y más fácil de entender desde una perspectiva de usuario 


#### Recomendaciones

* Para implementar los backups desarrollados en este proyecto en un escenario real, se podrían implementar junto con herramientas de monitoreo como Prometheus y Grafana. Contar con dashboards personalizados en Grafana facilitaría identificar tendencias, bottlenecks y problemas en los procesos de backup. 

* Para establecer backups en Elasticsearch, se recomienda hacer uso de la interfaz interactiva de Kibana para crear políticas de snapshots. Esto en lugar de ejecutar comandos manuales sobre la base ElasticSearch para hacer cada backup de forma individual, ya que provee una experiencia más amigable e intuitiva para los usuarios. 

* En lugar de tener las credenciales de acceso a la nube y el bucket hardcoded en los scripts de backup, se recomienda almacenar estas credenciales como secrets de Kubernetes . De esta manera se centraliza la gestión de credenciales sensibles y se evita exponerlas en el código. 

* Es crítico que el repositorio de código donde se almacena la tarea de backup se mantenga privado y con acceso restringido. De esta manera se evita que personas no deseadas puedan ver el código fuente y obtener las credenciales que dan acceso a la cuenta de AWS u otra plataforma en la nube. 

* Para optimizar el uso de almacenamiento en AWS, se recomienda hacer uso de una política de retención de backups automatizada. En lugar de retener todos los backups por tiempo indefinido, usar una política conserve los backups más recientes y necesarios, y elimine versiones antiguas que ya no son relevantes. 

* Es crítico validar periódicamente que al implementar backups, estos sean funcionales y permitan restaurar los datos correctamente. Por eso, al implementar componentes de backups se recomienda realizar pruebas regulares de restore a partir de los mismos para confirmar su correcto funcionamiento y capacidad de recuperación de información. 

* En una tarea de este tipo, dividir el trabajo es importante, pero también es importante que cada persona del equipo entienda su tarea. Se recomienda mantener una buena comunicación durante el desarrollo del proyecto y nunca quedarse con dudas. 

* A la hora de probar los backups generados, se recomienda hacer uso de un pod de depuración como el incluido en la solución de esta tarea. Dicho pod proporciona una terminal con conectividad directa al bucket de almacenamiento en AWS. Esto permite validar de forma efectiva que los respaldos se estén ejecutando correctamente y subiendo a la nube según lo esperado. 