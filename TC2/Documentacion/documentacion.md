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

A continuación, se presenta un manual de instalación para distintos motores de bases de datos junto con respectivos códigos para implementar backups y restaurar datos a través de una cuenta AWS.

#### Paso 1. Selección del Motor de Bases de datos a probar

Dentro de la carpeta para la TC2 se incluyen varios motores de bases de datos, la lista de todos estos es:

- MariaDB
- PostgreSQL
- Elasticsearch
- MongoDB
- Neo4J
- CouchDB

Una vez se haya seleccionado la base de datos para la que se desea probar backups y restauración se hace lo siguiente:

Se ingresa al path `TC2\helm\databases\values.yaml` donde se va a cambiar ciertos parámetros para hacer backups solo en la base deseada e iniciar solo la base deseada. Por cada base de datos saldrá el siguiente parámetro:

![Alt text](imgs/InicioTutorial.png)

enabled hace referencia a si se quiere inicializar o no ese motor de base de datos, la recomendación es no correr más de uno al mismo tiempo.

En caso de querer correr ese motor cambiar `enabled: true` por la versión actual, y al resto de motores ingresar `enabled: false` para apagarlos

Una vez hecho esto se debe ingresar a  `TC2\helm\backups\values.yaml`, y hacer lo mismo con las bases de datos que aparecen. 

IMPORTANTE: En caso de querer ejecutar backups a través de elastic **NO es necesario** ingresar a `TC2\helm\backups\values.yaml` a habilitar la base también. Sin embargo, sí es necesario acceder al archivo de values.yaml en el folder de `TC2\helm\bootstrap\values.yaml` y poner enabled: true en _elasticsearch_. Esto habilita el *elastic operator* en la instalación del helm chart de _bootstrap_. Este es importante para correr elasticsearch.

Finalmente, antes de ejecutar el código, se debe decidir si se desea realizar un backup o un restore en la base de datos. Esto se escoge en el archivo `TC2\helm\backups\values.yaml`, en el campo de *config.type*. Si queremos hacer un backup, simplemente ponemos `type: backup` y si queremos hacer un restore, ponemos `type: restore`. Cabe destacar que cuando queremos hacer un restore, debemos especificar el nombre del backup que queremos restaurar de los que están en aws. Esto se especifica en el campo *name*.
![Backup o Restore](imgs/inicioBackupRestore.png)

#### Paso 2. Ejecución del Código

Una vez se haya escogido la base, el siguiente paso es ejecutar los comandos para levantarla con sus respectivos parámetros, para esto ingresamos a cualquier terminal desde la cuál se puedan ejecutar comandos Linux. Una vez aquí abriremos la carpeta desde la terminal:

![Alt text](imgs/image.png)

Una vez en la carpeta donde hayamos descargado el proyecto se insertarán los siguientes comandos:

`cd TC2`
`cd helm`

Una vez aquí la terminal se encuentra en la carpeta donde se pueden ejecutar los archivos para la instalación y desinstalación de las bases de datos.

##### Para Instalar la base deseada con los parámetros especificados

En la terminal, primero se recomienda ejecutar:

`dos2unix install.sh`

Seguido de esto ejecutamos el comando: `./install.sh`

Una vez hecho esto la terminal comenzará a instalar todos los helm charts necesarios para la ejecución correcta del programa:

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

Este código va a instalar un pod en la red de Kubernetes donde se pueden ejecutar comandos para verificar si el bucket tiene archivos en la dirección que se quiere revisar. Al finalizar se podrá ver lo siguiente:

![Alt text](imgs/BackupElastic/debugpod.png)

Aquí se pueden ingresar comandos para revisar el contenido de los buckets en aws. El que lista los archivos que están en una dirección dada es:
`aws s3 ls s3://tec-ic4302-02-2023/[ruta]`
En nuestro caso, nuestros backups se están almacenando a partir de la ruta /2019073558, por lo que la instrucción que usaríamos comenzaría con:
`aws s3 ls s3://tec-ic4302-02-2023/2019073558/`

#### Elasticsearch con Kibana

A continuación, se muestra una guía para hacer backups y restores en la base Elasticsearch a través de su interfaz Kibana. Para este paso se asume que ya se habilitó la base y se ejecutó el script de instalación desde la terminal.

Lo primero que se debe hacer es tener instalada una aplicación para poder visualizar el kubernetes deployment y fácilmente obtener la información importante de los pods.

Para esta funcionalidad se recomienda hacer uso de **LENS**, el resto de esta guía se basará en el uso de esta aplicación para conectar los pods.

Desde Lens lo primero que haremos será entrar el cluster de Docker Desktop y nos iremos a la sección de **`PODS`**, una vez aquí entraremos al siguiente pod:

![Alt text](imgs/BackupElastic/PortElastic.png)

Al abrir el pod se debe buscar la sección señalada a la derecha, esta contiene un link que nos permitirá acceder de forma local a la interfaz Kibana para interactuar con la base de datos elasticsearch.

Una vez se haya hecho forward del port y se haya ingresado al sitio aparecerá lo siguiente:

![Alt text](imgs/BackupElastic/loginelastic.png)

Se solicita un usuario y una contraseña para poder ingresar al servicio Kibana, para obtener estos datos volvemos a **LENS** y buscamos la sección:

`Config/Secrets`, una vez aquí abrimos el siguiente secret:

![Alt text](imgs/BackupElastic/LensUbicacion.png)

Una vez aquí buscamos los siguientes datos:

![Alt text](imgs/BackupElastic/passwordES.png)

Estos corresponden a mi usuario y contraseña de elasticsearch. Por lo tanto, copio estas credenciales y las pongo en la interfaz. El usuario será elastic y la contraseña el otro valor. Hay que hacer click sobre el ojo para desencriptar la contraseña.

Despúes de ingresar las credenciales correctamente saldrá una imagen similar a esta:

![Alt text](imgs/BackupElastic/MainScreen.png)


En esta pantalla buscaremos la opcion stack management e ingresaremos
![Alt text](imgs/BackupElastic/OpcionManagement.png)


Una vez en esta interfaz, se busca la sección con el nombre **Snapshot and Restore**, en elastic los backups son llamados de esta forma.

Para restaurar o guardar backups lo primero es definir la dirección donde se van a guardar/obtener. Para esto se va a agregar el repositorio donde vamos a manejar nuestros backups de elastic, este hace referencia a la dirección del bucket de AWS y el cliente que vamos a usar para guardar los datos correspondientes a los snapshots. 

![Alt text](imgs/BackupElastic/addrepository.png)

Una vez aquí se selecciona `Register a repository`  para crearlo. Una vez adentro:

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


En esta sección no es necesario cambiar nada, es cuestión de dejarlo con sus configuraciones por default, se pasa a la siguiente página:

![Alt text](imgs/BackupElastic/eliminardespuesCiertoTIempo.png)

Esta es la sección final para crear un policy, aquí se puede definir **Si se quieren borrar los backups después de cierto tiempo, y si se quieren definir un mínimo a mantener**. A través de esta sección se puede configurar los puntos extra de la tarea, indicando la cantidad de días tras los que se quiere borrar los backups.
Finalmente, le damos next y se va a crear el policy en esta sección:

![Alt text](imgs/BackupElastic/CreatePolicy.png)


Confirmamos que los datos están correctos y se le da crear,como resultado, si se hizo bien debe de aparecer lo siguiente:

![Alt text](imgs/BackupElastic/ResultadoPolicy.png)


Despues de crear el policy y repositorio se van a crear backups automáticamente cada cierto tiempo dependiendo de lo definido al crear el policy.

![Alt text](imgs/BackupElastic/ExisteSnapshot.png)


Al revisar el repo tambien se podra observar que hay un snapshot disponible

![Alt text](imgs/BackupElastic/HayunSnapshot.png)


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



Consultando al índice se obtienen los datos:


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


---

#### PostgreSQL
Para realizar la instalación de PostgreSQL, se utilizó la versión del [helm chart preparada por Bitnami](https://bitnami.com/stack/postgresql/helm). Se utilizó la versión de la [imagen 14.9.0](https://bitnami.com/stack/postgresql/containers) debido a que la versión que está incluida en el [repositorio de extras de Amazon Linux es PostgreSQL 14](https://devopscube.com/install-configure-postgresql-amazon-linux/).
Para realizar la instalación, se habilita en el `databases/values.yaml` y en `backups/values.yaml` en el folder de `helm`.
En el archivo de `databases/values.yaml`, se especifica la base de datos que se crea en el servidor y adicionalmente el usuario y contraseña que se va a crear. El contenedor está configurado para correr con 1 CPU y 4GB de RAM.

![Configuración de bases de datos PostgreSQL](imgs/BackupPostgreSQL/postgreDBConfig.png)

Si se desea realizar un backup, en el archivo de backups/values.yaml` se pone `type: backup` en el campo de _postgresql.config.type_. Adicionalmente, se especifica la base de datos que se desea respaldar y un usuario registrado con su contraseña que es el que ingresará a realizar el backup. Los backups de PostgreSQL se van a guardar en `s3://tec-ic4302-02-2023/2019073558/postgresql/`. El campo de schedule debe contener un horario válido para un [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/). En nuestra configuración, está configurado para correr dos veces al día, 1 vez a medio día y otra vez a media noche.

![Configuración de backup PostgreSQL](imgs/BackupPostgreSQL/postgreConfig.png)

Luego se puede correr el script de `install.sh` en helm para correr el backup.
Cuando se instala en modo “backup”, se crean dos objetos principales de Kubernetes: un CronJob que se va a ejecutar dos veces al día cada 12 horas, y un Job que se ejecuta de una vez y realiza el respaldo a la base de datos. Estos jobs van a ejecutar el script `TC2/helm/backups/scripts/postgresqlBackup.sh`. Este script utiliza la herramienta de [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html) para realizar el backup. Se usan las opciones de –h, -U y –p para señalar la información de conexión a la base de datos. -h indica el host, el cual es el nombre del servicio de la base de datos de PostgreSQL. En el values.yaml del helm chart, se especifica como el FQDN de este servicio. El –U representa el usuario, el cual es *admin* en la configuración. No se especifica la contraseña directamente en el comando. Sin embargo, este usa una variable de entorno que se llama PGPASSWORD donde la almacena. Por lo tanto, en el template de `backup.yaml` del helm chart, se especifica la variable de entorno PGPASSWORD y se recibe como el campo de `postgresql.config.password`. Aquí se establece la contraseña para el uso. Finalmente, -p se usa para indicar el puerto de la base de datos, que en PostgreSQL usualmente es 5432. Luego, las otras opciones de –w es para que no solicite un prompt para ingresar la contraseña. -c es para indicar que se incluyan instruciones de “DROP” para la creación de objetos. Esto vuelve a crear todos los objetos dentro de la base de datos. Sin embargo, la base de datos debe existir en el servidor de la base de datos.
Finalmente, se utiliza la siguiente instrucción para subir el backup al bucket S3 de aws:
`aws s3 cp /pgdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive`
Este script crea backups con el nombre DBNAME-DATE.sql

![postgreBackup.sh](imgs/BackupPostgreSQl/postgreBackup.png)

El restore de PostgreSQL funciona muy similarmente. Para activarlo, hay que cambiar el type en el values.yaml a restore y especificar el nombre del backup que queremos restaurar en el campo de name:

![postgreBackup.sh](imgs/BackupPostgreSQl/pgRestoreConfig.png)

El script que ejecuta el restore utiliza la herramienta de [psql](https://www.postgresql.org/docs/current/app-psql.html#:~:text=psql%20is%20a%20terminal%2Dbased,or%20from%20command%20line%20arguments.), el cual es una terminal interactiva para Postgres. En el script, la configuración de opciones es muy igual a la del script de backups. Se conecta con el host, el usuario, y el puerto y restaura la base de datos dada al final. El backup lo recibe como entrada. Este backup es descargado del bucket de AWS a partir del path y el name dado en la configuración en el values.yaml. 

![postgreBackup.sh](imgs/BackupPostgreSQl/postgreRestore.png)

##### Ejemplo de Backup y Restore:
Para tener más control, podemos instalar los helm charts por separado. Primero, hay que installar bootstrap. Ubicándonos en el folder de helm, hacemos:
`helm install bootstrap bootstrap`
Luego, tras asegurarnos de que PostgreSQL está habilitado en el values.yaml de databases, hacemos:
`helm install databases databases`
Esto crea el pod de la base de datos.

![Pod](imgs/BackupPostgreSQl/pgPod.png)

Para insertar registros en la base de datos, podemos hacer un portforward del servicio de la base de datos. Para esto, en Lens, vamos a Network, Services, databases-postgresql, lo abrimos y bajamos hasta que aparezca el puerto. Aquí podemos abrir el portforward. Esto nos va a abrir una ventana del navegador con el puerto que se está exponiendo en la máquina local.

![Port Forward](imgs/BackupPostgreSQl/pgPort.png)

Luego, podemos abrir una herramienta de Postgres como [pgAdmin](https://www.pgadmin.org/) y conectarnos al servidor de PostgreSQL en el puerto abierto por el portforward. Ahí, al registrar el servidor, podemos ponerle un nombre y podemos ingresar con el usuario definido en el helm chart.

![Conexión](imgs/BackupPostgreSQl/pgConnection.png)

Aquí podemos correr consultas, como crear una tabla e insertar un registro:

![Conexión](imgs/BackupPostgreSQl/pgCreateTable.png)

Ya con información en la base de datos, podemos instalar el helm chart de backups para que el Job realice el respaldo:
`helm install backups backups`
Podemos ir a Lens y la sección de Jobs. Aquí podemos abrir la consola del pod y ver el progreso del script. Si sale un error de que no encuentra el script, hay que hacer la instrucción en la consola de y reinstalar el helm chart de backups:
`dos2unix backups/scripts/postgresqlBackup.sh`

![Backup Pod](imgs/BackupPostgreSQl/pgPodBackup.png)

Al final, podemos usar el debug-pod de /utils para consultar si se subió correctamente el archivo con el comando:
` aws s3 ls s3://tec-ic4302-02-2023/2019073558/postgresql/`

![AWS ls](imgs/BackupPostgreSQl/pgAWSls.png)

Aquí podemos ver que el backup creado es Pokemon-202310212135.sql. Ahora vamos a restaurar este.
Para probarlo, podemos eliminar el registro insertado anteriormente, para ver cómo se restaura:

![Delete record](imgs/BackupPostgreSQl/pgDelete.png)

Ahora, escribimos el nombre del backup Pokemon-202310212135.sql en el campo de name en el values.yaml de backups y cambiamos el type a restore. Tras hacer esto, podemos reinstalar el helm chart con:
`
helm uninstall backups
helm install backups backups
`
Cuando está en modo restore, no crea un CronJob, solo ejecuta un Job. Por lo tanto, podemos ver el progreso del Job en la pestaña de Jobs en Lens:

![PostgreSQL Restore Job](imgs/BackupPostgreSQl/pgRestoreJob.png)

Al final, podemos saber que el Job terminó cuando la columna de Completions salga en 1/1.
Ahora, podemos verificar que el restore se realizó en pgAdmin haciendo un select de la tabla:

![PostgreSQL Restore Job](imgs/BackupPostgreSQl/pgRestoreSelect.png)

#### MongoDB
Para realizar la instalación de MongoDB, se utilizó la versión del [helm chart preparada por Bitnami]( https://bitnami.com/stack/mongodb/helm). 
Para realizar la instalación, se habilita en el `databases/values.yaml` y en `backups/values.yaml` en el folder de `helm` la opciones de enabled para realizar la instalación de la base de datos deseada.
En el archivo de `databases/values.yaml`, como no se está indicando algún valor además del enabled, la instalación se va a realizar de manera default, es decir se va a realizar una instalación con los parámetros predefinidos por el helmchart.
```
mongodb:
  enabled: true
```
Si se desea realizar un backup, en el archivo de backups/values.yaml` se pone `type: backup` en el campo de _mongo.config.type. En este setup, el job que realiza esta toma los datos del secret de mongo para obtener el acceso a la base de datos y realizar el backup. Los backups de Mongo se van a guardar en `s3://tec-ic4302-02-2023/2019073558/mongo/`. El campo de schedule debe contener un horario válido para un [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/). En nuestra configuración, está configurado para correr dos veces al día, 1 vez a medio día y otra vez a media noche.
```
mongo:
  enabled: false
  config:
    namespace: default
    connectionString: databases-mongodb.default.svc.cluster.local:27017
    bucketName: tec-ic4302-02-2023
    path: 2019073558/mongodb
    maxBackups: 3
    secret: databases-mongodb
    name:  "202310202250"
    schedule: "0 */12 * * *"
    diskSize: 1
    storageClass: hostpath
    provider: aws
    type: restore
```

Luego se puede correr el script de `install.sh` en helm para correr el backup.
Cuando se instala en modo “backup”, se crean dos objetos principales de Kubernetes: un CronJob que se va a ejecutar dos veces al día cada 12 horas, y un Job que se ejecuta de una vez y realiza el respaldo a la base de datos. Estos jobs van a ejecutar el script `TC2/helm/backups/scripts/mongodbBackup.sh`. Este script utiliza la herramienta de [mongodump]( https://www.mongodb.com/docs/database-tools/mongodump/) para realizar el backup. Se usan las opciones de --host, -U y –p para señalar la información de conexión a la base de datos. --host indica el host, el cual es el nombre del servicio de la base de datos de PostgreSQL. En el values.yaml del helm chart, se especifica como el FQDN de este servicio. El –U representa el usuario, el cual es *root* en la configuración. No se especifica la contraseña directamente en el comando. Sin embargo, este usa una variable de entorno que se llama MONGO_PASSWORD donde la almacena. Por lo tanto, en el template de `backup.yaml` del helm chart, se especifica la variable de entorno MONGO_PASSWORD y se recibe como el campo de `mongo.config.password`. Aquí se establece la contraseña para el uso.
Finalmente, se utiliza la siguiente instrucción para subir el backup al bucket S3 de aws:
`aws s3 cp /mongodump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/$DATE --recursive`
Este script crea backups dentro del S3 dentro de una carpeta con la fecha, un archivo llamado archive donde se tiene la información del backup realizado.
El restore de Mongo funciona muy similarmente. Para activarlo, hay que cambiar el type en el values.yaml a restore y especificar el nombre del backup que queremos restaurar en el campo de name:
El script que ejecuta el restore utiliza la herramienta de mongodumps igual que el backup, por lo que la instalación es la misma. En el script, la configuración de opciones es muy igual a la del script de backups. Se conecta con el host, el usuario, y restaura la base de datos dada al final. El backup lo recibe como entrada. Este backup es descargado del bucket de AWS a partir del path y el name dado en la configuración en el values.yaml en el valor de _name_.
##### Ejemplo de Backup y Restore:
Para tener más control, podemos instalar los helm charts por separado. Primero, hay que installar bootstrap. Ubicándonos en el folder de helm, hacemos:
`helm install bootstrap bootstrap`
Luego, tras asegurarnos de que Mongo está habilitado en el values.yaml de databases, hacemos:
`helm install databases databases`
Esto crea el pod de la base de datos.
Para insertar registros en la base de datos, podemos hacer una terminal interactiva con el pod con el comando:
```
kubectl exec -i -t -n default databases-mongodb-59dbc55f8c-2fndw -c mongodb -- sh -c "clear; (bash || ash || sh)"
```
Dentro de esta terminal interactiva se pueden realizar todas las operaciones para probar crear una colección y agregar un registro a la base de datos y luego hacer el backup mediante el job, y finalmente borrar los registros que hay en la base de datos para después realizar el restore y observar que se recupera la información que ha sido borrada.
En el documento dentro de la carpeta de dbscripts, dentro de la carpeta de MongoDB, se encuentran los scrips tanto de creación como los de borrado para probar esta funcionalidad. 

_Datos antes del borrado_

![Mongo datos](imgs/BackupMongo/Mongo1.png)

Ya con información en la base de datos, podemos instalar el helm chart de backups para que el Job realice el respaldo:
`helm install backups backups`
Podemos ir a Lens y la sección de Jobs. Aquí podemos abrir la consola del pod y ver el progreso del script. Si sale un error de que no encuentra el script, hay que hacer la instrucción en la consola de y reinstalar el helm chart de backups:
`dos2unix backups/scripts/postgresqlBackup.sh`
Al final, podemos usar el debug-pod de /utils para consultar si se subió correctamente el archivo con el comando:
` aws s3 ls s3://tec-ic4302-02-2023/2019073558/mongodb/`
Aquí podemos ver que el backup que se ha generado.
Ahora se procede a realizar el borrado de los datos de mongo:

_Datos después del borrado_

![Mongo datos](imgs/BackupMongo/Mongo2.png)

Para realizar el restore, se escribe el nombre del backup generado, este se puede consultar utilizando el mismo comando de  ` aws s3 ls s3://tec-ic4302-02-2023/2019073558/mongodb/` , este dato se agrega en el campo de name en el values.yaml de backups y cambiamos el type a restore. Tras hacer esto, podemos reinstalar el helm chart con:
`
helm uninstall backups
helm install backups backups
`
Cuando está en modo restore, no crea un CronJob, solo ejecuta un Job. Por lo tanto, podemos ver el progreso del Job en la pestaña de Jobs en Lens:
Al final, podemos saber que el Job terminó cuando la columna de Completions salga en 1/1.
Ahora mediante un find en la terminal interactiva se puede observar que el restore ha sido exitoso.

_Datos despues del restore_

![Mongo datos](imgs/BackupMongo/Mongo3.png)

#### MariaDB
Para realizar la instalación de MongoDB, se utilizó la versión del [helm chart preparada por Bitnami]( https://bitnami.com/stack/mariadb/helm). 
Para realizar la instalación, se habilita en el `databases/values.yaml` y en `backups/values.yaml` en el folder de `helm` la opción de enabled para realizar la instalación de la base de datos deseada.
En el archivo de `databases/values.yaml`, como no se está indicando algún valor además del enabled, la instalación se va a realizar de manera default, es decir se va a realizar una instalación con los parámetros predefinidos por el helmchart.
```
moariadb:
  enabled: true
```
Si se desea realizar un backup, en el archivo de backups/values.yaml` se pone `type: backup` en el campo de _maria.config.type. En este setup, el job que realiza esta toma los datos del secret de mariadb para obtener el acceso a la base de datos y realizar el backup. Los backups de MariaDB se van a guardar en `s3://tec-ic4302-02-2023/2019073558/mariadb/`. El campo de schedule debe contener un horario válido para un [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/). En nuestra configuración, está configurado para correr dos veces al día, 1 vez a medio día y otra vez a media noche.
```
maria:
  enabled: false
  config:
    namespace: default
    connectionString: databases-mariadb
    bucketName: tec-ic4302-02-2023
    path: 2019073558/mariadb
    maxBackups: 3
    secret: databases-mariadb
    name:  pokemon_db-202310210452.sql
    schedule: "0 */12 * * *"
    diskSize: 1
    storageClass: hostpath
    provider: aws
    type: restore
```

Luego se puede correr el script de `install.sh` en helm para correr el backup.
Cuando se instala en modo “backup”, se crean dos objetos principales de Kubernetes: un CronJob que se va a ejecutar dos veces al día cada 12 horas, y un Job que se ejecuta de una vez y realiza el respaldo a la base de datos. Estos jobs van a ejecutar el script `TC2/helm/backups/scripts/mariadbBackup.sh`. Este script utiliza la herramienta de [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) para realizar el backup. Se usan las opciones de -h, -U y –p para señalar la información de conexión a la base de datos. -h indica el host, el cual es el nombre del servicio de la base de datos de PostgreSQL. En el values.yaml del helm chart, se especifica como el FQDN de este servicio. El –U representa el usuario, el cual es *root* en la configuración. No se especifica la contraseña directamente en el comando. Sin embargo, este usa una variable de entorno que se llama MARIA_PASSWORD donde la almacena. Por lo tanto, en el template de `backup.yaml` del helm chart, se especifica la variable de entorno MARIA_PASSWORD y se recibe como el campo de `maria.config.password`. Aquí se establece la contraseña para el uso.
Finalmente, se utiliza la siguiente instrucción para subir el backup al bucket S3 de aws:
`aws s3 cp /mariadbdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive`
Este script crea backups dentro del S3 dentro de un archivo con la fecha de cuando se realizó el backup.
El restore de MariaDB funciona muy similar. Para activarlo, hay que cambiar el type en el values.yaml a restore y especificar el nombre del backup que queremos restaurar en el campo de name:
El script que ejecuta el restore utiliza la herramienta de mysqldump igual que el backup, por lo que la instalación es la misma. En el script, la configuración de opciones es muy igual a la del script de backups. Se conecta con el host, el usuario, y restaura la base de datos dada al final. El backup lo recibe como entrada. Este backup es descargado del bucket de AWS a partir del path y el name dado en la configuración en el values.yaml en el valor de _name_.
##### Ejemplo de Backup y Restore:
Para tener más control, podemos instalar los helm charts por separado. Primero, hay que installar bootstrap. Ubicándonos en el folder de helm, hacemos:
`helm install bootstrap bootstrap`
Luego, tras asegurarnos de que Mongo está habilitado en el values.yaml de databases, hacemos:
`helm install databases databases`
Esto crea el pod de la base de datos.
Para insertar registros en la base de datos, podemos hacer una terminal interactiva con el pod con el comando:
```
PS C:\Users\joseg> kubectl exec -i -t -n default databases-mariadb-0 -c mariadb -- sh -c "clear; (bash || ash || sh)"
```
Dentro de esta terminal interactiva se pueden realizar todas las operaciones para probar crear una base datos, tablas y agregar un registro a la base de datos y luego hacer el backup mediante el job, y finalmente borrar los registros que hay en la base de datos para después realizar el restore y observar que se recupera la información que ha sido borrada.
En el documento dentro de la carpeta de dbscripts, dentro de la carpeta de MariaDB, se encuentran los scrips tanto de creación como los de borrado para probar esta funcionalidad. 

_Datos antes del borrado_

![Maria datos](imgs/BackupMaria/Maria1.png)

Ya con información en la base de datos, podemos instalar el helm chart de backups para que el Job realice el respaldo:
`helm install backups backups`
Podemos ir a Lens y la sección de Jobs. Aquí podemos abrir la consola del pod y ver el progreso del script. Si sale un error de que no encuentra el script, hay que hacer la instrucción en la consola de y reinstalar el helm chart de backups:
`dos2unix backups/scripts/postgresqlBackup.sh`
Al final, podemos usar el debug-pod de /utils para consultar si se subió correctamente el archivo con el comando:
` aws s3 ls s3://tec-ic4302-02-2023/2019073558/mariadb/`
Aquí podemos ver que el backup que se ha generado.
Ahora se procede a realizar el borrado de los datos de MariaDB:

_Datos después del borrado_

![Maria datos](imgs/BackupMaria/Maria2.png)

Para realizar el restore, se escribe el nombre del backup generado, este se puede consultar utilizando el mismo comando de  ` aws s3 ls s3://tec-ic4302-02-2023/2019073558/mariadb/` , este dato se agrega en el campo de name en el values.yaml de backups y cambiamos el type a restore. Tras hacer esto, podemos reinstalar el helm chart con:
`
helm uninstall backups
helm install backups backups
`
Cuando está en modo restore, no crea un CronJob, solo ejecuta un Job. Por lo tanto, podemos ver el progreso del Job en la pestaña de Jobs en Lens:
Al final, podemos saber que el Job terminó cuando la columna de Completions salga en 1/1.
Ahora mediante un select *  en la terminal interactiva se puede observar que el restore ha sido exitoso.

_Datos despues del restore_

![Maria datos](imgs/BackupMaria/Maria3.png)


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
Si se desea realizar un backup, en el archivo de backups/values.yaml se pone `type: backup` en el campo de couchdb.config.type. Los backups de CouchDB se van a guardar en `s3://tec-ic4302-02-2023/2019073558/couchdb/`. El campo de schedule debe contener un horario válido para un [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/). En nuestra configuración, está configurado para correr dos veces al día, 1 vez a medio día y otra vez a media noche. El host va a tener la dirección de la base de datos de CouchDB dentro del cluster para que así pueda localizarlo y hacer el backup, la base de datos va a ser la base de datos ya definida de la cual se va a hacer el backup, el port va a ser el predefinido por el helm chart de CouchDB por el cual vamos a tener acceso al API. Y tenemos el user y password que van a ser los mismos que definimos previamente, por ultimo para el caso del restore se le indica un name, que va a ser el nombre del archivo en el cual se está guardando el backup que se quiera restaurar.  
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
Cuando se instala en modo “backup”, se crean dos objetos principales de Kubernetes: un CronJob que se va a ejecutar dos veces al día cada 12 horas, y un Job que se ejecuta de una vez y realiza el respaldo a la base de datos. Estos jobs van a ejecutar el script `TC2/helm/backups/scripts/couchdbB.sh`. Debido a que CouchDB no tiene definido ningún método para realizar los backups, hacemos uso del [API de CouchDB](https://docs.couchdb.org/en/latest/api/) para así extraer los documentos que contenga la base de datos y poder crear un respaldo de estos. Para realizar el backup utilizamos el siguiente método: 
``` 
URL="http://$COUCHDB_USER:$COUCHDB_PSW@$COUCHDB_HOST:$COUCHDB_PORT/$COUCHDB_DB/_all_docs?include_docs=true" 
curl -X GET "$URL" -H "Accept: application/json" | jq '{ docs: [.rows[] | .doc] }' > /couchdump/$DATE/couchdb-$DATE.json 
``` 
En donde de primero definimos el path que vamos a utilizar para hacer la llamada al API, en este caso utilizamos unas variables de entorno definidas con los datos del values.yaml, el endpoint que utilizamos es **db/_all_docs?include_docs=true**, el cual nos va a retornar todos los documentos de la base de datos que indiquemos para asi poder almacenarlos en un archivo .json, ya teniendo el path para el llamado utilizamos el método **curl** para hacer el llamado, en este indicamos que es un GET, y le definimos el url, e indicamos el tipo de dato que esperamos de vuelta, al mismo tiempo estamos utilizando el método **jq** para así cambiarle el formato al archivo de respuesta para así tenerlo en un formato que luego pueda ser utilizado para el recovery , y por ultimo le indicamos el path en el cual queremos que se almacene y el nombre del archivo que queremos que tenga.  
Finalmente, se utiliza la siguiente instrucción para subir el backup al bucket S3 de aws: 
`aws s3 cp /couchdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive` 
Este script crea backups dentro del S3 dentro de un archivo con la fecha de cuando se realizó el backup. 
En el caso del restore, es bastante similar al backup pero tiene ciertas diferencias, entre estas esta que se utiliza el endpoint del API **_bulk_docs** al cual se le da el archivo .json extraído del path y con el nombre indicado e inserta en la base de datos todos los documentos dentro de este archivo.  

##### Ejemplo de Backup y Restore: 
Para tener más control, podemos instalar los helm charts por separado. Primero, hay que instalar bootstrap. Ubicándonos en el folder de helm, hacemos: 
`helm install bootstrap bootstrap` 
Luego, tras asegurarnos de que Couchdb está habilitado en el values.yaml de databases, hacemos: 
`helm install databases databases` 
Esto crea el pod de la base de datos. 
Una vez creado hacemos un port foward dentro de Lens del puerto de CouchDB para asi poder hacer uso del API en herramientas como Postman o Thunderclient.  
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
Donde el rev es autogenerado por CouchDB por cada registro, podemos ver cuál es el rev de nuestro registro con el llamado: 
` GET http://127.0.0.1:50209/pokemon/_all_docs?include_docs=true ` 
Para realizar el restore, se escribe el nombre del backup generado, este lo recibimos cuando se ejecute el backup en el pod logs, este dato se agrega en el campo de name en el values.yaml de backups y cambiamos el type a restore. Tras hacer esto, podemos reinstalar el helm chart con: 
` helm uninstall backups `
` helm install backups backups `
Cuando está en modo restore, no crea un CronJob, solo ejecuta un Job. Por lo tanto, podemos ver el progreso del Job en la pestaña de Jobs en Lens: 
Al final, podemos saber que el Job terminó cuando la columna de Completions salga en 1/1. 
Ahora mediante el mismo llamado en Postman: 
` GET http://127.0.0.1:50209/pokemon/_all_docs?include_docs=true `  
Y con el response se puede observar que el restore ha sido exitoso.

 
#### Neo4j
Para instalar Neo4j, se utilizó el Helm Chart oficial de Neo4j. Este se puede acceder de https://helm.neo4j.com/neo4j. Para añadir el repositorio, hay que hacer 
```
helm repo add neo4j https://helm.neo4j.com/neo4j
```
 Los Helm Charts disponibles de Neo4j son los siguientes.
```
neo4j/neo4j                       5.13.0  5.13.0  Neo4j is the world's leading graph database
neo4j/neo4j-admin                 5.13.0  5.13.0  Neo4j is the world's leading graph database
neo4j/neo4j-headless-service      5.13.0  -       Neo4j is the world's leading graph database
neo4j/neo4j-persistent-volume     5.13.0  -       Sets up persistent disks suitable for a Neo4j H...
neo4j/neo4j-reverse-proxy         5.13.0  5.13.0  Sets up an http server and a reverse proxy for ...
```

Para instalar la base de datos en sí, se tiene que añadir la dependencia al Chart.yaml del chart de databases. 
```
- name: neo4j
    version: "5.12.0"
    repository: https://helm.neo4j.com/neo4j
    condition: neo4j.enabled
```
En los values.yaml, hay que poner los siguientes valores.
```
neo4j:
  enabled: true
  neo4j:
    name: my-standalone
    resources:
      cpu: "0.5"
      memory: "2Gi"
    password: "neo4j-password"
    edition: "enterprise"
    acceptLicenseAgreement: "yes"
  config:
    server.directories.plugins: "/var/lib/neo4j/labs"
    dbms.security.procedures.unrestricted: "apoc.export.*,apoc.import.*,apoc.*,apoc.export"
    server.config.strict_validation.enabled: "false"
    dbms.security.procedures.allowlist: "apoc.export.*,apoc.import.*"
  apoc_config:
    apoc.trigger.enabled: "true"
    apoc.jdbc.neo4j.url: "jdbc:foo:bar"
    apoc.import.file.enabled: "true"
    apoc.export.file.enabled: "true"
  env:
    NEO4J_PLUGINS: '["apoc"]'
  volumes:
    data:
      mode: defaultStorageClass
      defaultStorageClass:
        requests:
          storage: 2Gi
```
Aquí hay varios parámetros importantes. La base de datos siempre debe tener un nombre, el parámetro de name. En este caso es my-standalone. El password es la contraseña del usuario neo4j, que es el usuario predeterminado. Si este campo se omite, la contraseña se genera automáticamente. Los resources definen el tamaño de la instancia de Neo4j. El mínimo es de 0.5 CPU y 2 Gb de memoria. El volumes.data asigna el volumen del contendor que va a contener los datos. Este puede persistir aun cuando la base de datos no está instalada. 

La sección de config se utiliza para instalar plugins, que son como métodos, funciones y procedimientos adicionales a los que ya tiene Neo4j. En este caso, estamos intentando de instalar el plugin de APOC Core. Este permite exportar e importar una base de datos con un archivo del dump. Se incluyen estos procedimientos y la configuración del plugin.
Finalmente, está el parámetro más importante para nuestro caso de backup: el edition. Esto es debido a que los backups solo están disponibles en el Enterprise Edition de Neo4j.

![Alt text](imgs/BackupNeo4j/enterprise1.png)
 
![Alt text](imgs/BackupNeo4j/enterprise2.png)

 
 

Para levantar el pod de Neo4j, simplemente hay que hacer 
```
helm install databases databases
```

##### Backup
Hay varias formas de hacer un backup en Neo4j. La primera es la que se utilizó para esta tarea.
Para hacer un backup desde un job y luego subir el backup al bucket de AWS, se necesita buscar una forma instalar Neo4j en Amazon Linux. Esto es porque el pod del job usa una imagen del Amazon CLI. Para hacer esto, se utilizan las siguientes instrucciones:
```
rpm --import https://debian.neo4j.com/neotechnology.gpg.key
cat << EOF >  /etc/yum.repos.d/neo4j.repo
[neo4j]
name=Neo4j RPM Repository
baseurl=https://yum.neo4j.com/stable/5
enabled=1
gpgcheck=1
EOF
NEO4J_ACCEPT_LICENSE_AGREEMENT=yes yum install neo4j-enterprise-5.13.0 -y
```
Es importante recalcar que hay que instalar la versión de Enterprise. La Community Edition de Neo4j no tiene la instrucción específica para hacer el backup. 
La instalación de Neo4j en Amazon Linux contiene las herramientas para interactuar con esta: neo4j y neo-admin. Se utiliza neo4j-admin para hacer el backup. La instrucción es la siguiente:
```
neo4j-admin database backup --from=$NEO4J_SERVICE:$NEO4J_PORT --type=full --to-path=/neo4j/$DATE
```
Este comando tiene varias opciones. Se explicarán a continuación las que se utilizaron en esta tarea:
-	--from=<host:port> : Esta opción se utiliza para especificar la dirección de la base de datos de Neo4j. En nuestro caso, se necesita acceder al servicio del admin del pod de Neo4j. Esto se hace poniendo el nombre del pod-admin.default.svc.cluster.local. El puerto es el que se usa para los backups. En este caso es el 6362.
-	--type=full : Se utiliza para especificar el tipo de backup que se necesita. Hay tres tipos: full, diff y auto. Un backup full contiene toda la base de datos. Un diferencial (diff) contiene una bitácora de las transacciones que se aplicaron a la base de datos desde el último full backup. Auto determina cuál backup hacer automáticamente.
-	--to-path= : Especifica el directorio donde se va a almacenar el backup. Este puede ser en la misma base de datos, pero en este caso es utilizó el camino absoluto al directorio del pod del job para que se almacene el backup localmente en este.
Luego de ejecutar la instrucción, es obtiene el siguiente resultado.

![Alt text](imgs/BackupNeo4j/backupcomplete.png)

 
Las variables de $NEO4J_SERVICE y $NEO4J_PORT se envían por el values.yaml del job. Para la sección de Neo4j, los valores son los siguientes:
```
neo4j:
  enabled: true
  config:
    namespace: default
    host: databases-admin.default.svc.cluster.local
    port: "6362"
    bucketName: tec-ic4302-02-2023
    path: 2019073558/neo4j
    maxBackups: 3
    name: neo4j-2023-10-23T20-53-22.backup
    schedule: "0 */12 * * *"
    diskSize: 2
    storageClass: hostpath
    provider: aws
    type: backup
```
Aquí podemos ver cómo se envían el host (la dirección de la base de datos), el puerto (6362) y la información del path para subir el backup a AWS. Las instrucciones para subirlo a AWS son las mismas para las otras bases de datos:
```
aws s3 cp /neo4j/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
```
Luego de correr el backup y subirlo a AWS, podemos revisar si se subió correctamente:

![Alt text](imgs/BackupNeo4j/backupinbucket.png)
 

La segunda opción para hacer el backup es utilizar el Helm Chart del neo4j-admin para subir el backup directamente a Neo4j. Para hacer esto, es necesario crear un nuevo values.yaml file específico para este. Este archivo tiene parámetros diferentes:
```
neo4j:
  image: "neo4j/helm-charts-backup"
  imageTag: "5.12.0"
  jobSchedule: "0 17 * * *"
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  backoffLimit: 3


backup:
  bucketName: "tec-ic4302-02-2023"
  databaseAdminServiceName:  "databases-admin"
  database: "neo4j"
  cloudProvider: "aws"
  secretName: "aws-credential"
  secretKeyName: "credentials"
consistencyCheck:
  enabled: true
```
Las credenciales de AWS están en un secret de Kubernetes. Este se establece en el helm chart de Bootstrap. La imagen que se va a usar para el pod es la de neo4j/helm-charts-backup. Esta contiene las instrucciones para hacer el backup y subirlo al bucket. Se pone el horario del cronjob que se crea, los límites de intentos, la información del bucket de AWS, las bases de datos que se van a respaldar y el consistency check. Este se asegura de que los datos sean consistentes antes de hacer el backup.

Luego, hay que instalar el Helm Chart de neo4j-admin. Esto se puede hacer con
```
helm install backup-name neo4j/neo4j-admin -f /dreccion-del-archivo/backup-values.yaml
```
Esto crea un cronjob con la configuración especifica en el values.yaml. Uno puede manualmente correr el cronjob. Es importante que la base de datos de Neo4j se del Enterprise Edition, porque si no, no va a estar abierto el puerto 6362, que es el de los backups, por lo que el job falla.

![Alt text](imgs/BackupNeo4j/portfailure.png)
 
Si el job no falla, ocurre lo siguiente:

![Alt text](imgs/BackupNeo4j/manualjob.png)

 
![Alt text](imgs/BackupNeo4j/bucketsuccess.png)

 
![Alt text](imgs/BackupNeo4j/backupinbucket.png)

 
Aquí podemos observar que el backup sí se subió correctamente, pero no se subió al directorio de nuestro grupo. No obstante, cuando intenté cambiar la dirección del bucket, daba error de que no encontraba el bucket.

![Alt text](imgs/BackupNeo4j/bucketfailure.png)

 
Por lo tanto, usamos la primera forma para que sí se subiera al bucket y dirección correcta. 

La tercera forma de hacer un backup es de la forma que no es en línea, con un dump. Es muy similar a la primera forma, pero la base de datos tiene que estar detenida. Esto se puede hacer con la herramienta de Neo4j. El comando es neo4j stop. El problema con esto es que para detenerla, uno tiene que estar directamente con en el pod de la base de datos, con kubectl exec –it nombre del pod. Por lo tanto, esta forma no nos sirve para esta tarea. No obstante, el procedimiento es el siguiente.
Cuando uno ya está en el pod, hay que hacer
```
neo4j stop
neo4j-admin database dump neo4j
```
El resultado es el siguiente.

![Alt text](imgs/BackupNeo4j/databasedump.png)

 
Para encontrar el dump, hay que entrar al directorio data/dumps/

![Alt text](imgs/BackupNeo4j/dumplocation.png)

 

La última forma de hacer un backup es por medio del plugin APOC. Este significa Awesome Procedures on Cypher. Este tiene unos procedimientos que son export e import. Hay varias versiones de export. Uno puede exportar a un archivo GraphML, Cypher, CSV, Excel, JSON, etc. 
Este comando se puede correr desde el browser de Neo4j. 

![Alt text](imgs/BackupNeo4j/apocresult.png)

 El resultado de esta instrucción se debería guardar en el directorio de imports del pod.

Para correr esta instrucción desde el pod del job, se puede utilizar el API de Neo4j. Se puede instalar curl y realizar un post al endpoint. Se utiliza el servicio y el puerto, como al igual que en la primera forma del backup. La instrucción para hacer esto es el siguiente. Se utiliza un > para guiar el resultado del query a un archivo del pod.
```
curl --verbose POST http://databases-admin.default.svc.cluster.local:7474/db/neo4j/tx/commit -H "Content-Type:application/json" -d "{\"statements\":[{\"statement\":\"CALL apoc.export.cypher.all('backup.cypher', {useTypes: TRUE, storeNodeIds: FALSE})\"}]}" -H "Authorization: Basic bmVvNGo6bmVvNGotcGFzc3dvcmQ=" > /neo4j/$DATE/backup.cypher
``` 
Sin embargo, como se ve en el resultado del query más arriba, el resultado no es el archivo en sí, es como un mensaje de éxito. Esta respuesta es lo que se guarda en el archivo, no el archivo del backup. Por lo tanto, esta opción no sirve para esta tarea.

##### Restore
Para hacer un restore, es muy similar a la primera forma de hacer el backup. Los values.yaml para el job son muy similares:
```
neo4j:
  enabled: true
  config:
    namespace: default
    host: databases-admin.default.svc.cluster.local
    port: "6362"
    bucketName: tec-ic4302-02-2023
    path: 2019073558/neo4j
    maxBackups: 3
    name: neo4j-2023-10-23T20-53-22.backup
    schedule: "0 */12 * * *"
    diskSize: 2
    storageClass: hostpath
    provider: aws
    type: restore
```
Cuando uno le pone el type restore, eso indica que el job que se tiene que crear es el de restore y no el backup.
Hay que instalar Neo4j Enterprise en el pod.
Primero, hay que copiar el archivo del backup del bucket al pod. Esto se hace con la siguiente instrucción:
```
aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/$RESTORE_FILE $DIRECTORY
```
Luego, se realiza la instrucción propia del restore. Este es muy similar al backup
```
neo4j-admin database restore --from-path=$DIRECTORY/$RESTORE_FILE --to-path-data=$NEO4J_SERVICE:$NEO4J_PORT --verbose
```
Se envía el servicio de Neo4j y el puerto y ahí se realiza el restore.

![Alt text](imgs/BackupNeo4j/restoresuccess.png)

 

Así se debería ver la base de datos luego del restore.

![Alt text](imgs/BackupNeo4j/graph.png)

 

## Conclusiones

1.	El uso de almacenamiento en la nube con AWS S3 facilita la escalabilidad y accesibilidad de los backups, pero requiere tomar en cuenta consideraciones adicionales de seguridad a la hora de hacer el código y mantener su control de versiones, como asegurarse que las credenciales de AWS estén siempre seguras y privadas.

2. Si bien Elasticsearch requiere una configuración inicial más elaborada y el proceso para habilitar snapshots es más manual, una vez que se tienen los componentes configurados adecuadamente, la automatización de snapshots y restores resulta bastante sencilla y más fácil de entender desde una perspectiva de usuario.

3.	El uso de scripts de Linux resulta extremadamente útil para ejecutar automáticamente tareas más complejas en jobs o en un contenedor.

4.	Las operaciones de backup y restore se pueden realizar de forma más fácil si la base de datos tiene herramientas de línea comandos para esto y que además se pueden conectar a otro servidor por medio de parámetros de conexión. Por esta razón, los jobs de PostgreSQL, MariaDB y MongoDB resultaron más sencillas.

5.	Los backups y restores son fundamentales para la recuperación de accidentes o fallas, como cuando se borra un registro por accidente o cuando se inicia un nuevo servidor y se quiere restaurarlo para que esté igual a otra base de datos. Para esto, son especialmente útiles los backups completos.

6.	El cronjob es una herramienta útil para realizar los procesos de backup de una manera automática y segura.

7. 	Kubernetes es una herramienta esencial que permite realizar una amplia cantidad de pruebas e instalaciones de bases de datos.

8. 	Los helm charts continúan siendo una herramienta necesaria para la automatización del despliegue de las bases de datos.

9.	El servicio ClusterIP que levantan las bases de datos resulta fundamental y extremadamente útil para conectarse a la base de datos desde otro pod en el cluster de Kubernetes.

10.	El API de CouchDB nos facilita el manejo de los datos, al momento de hacer pruebas con herramientas como Postman o de hacer los backups de los documentos de manera eficiente. 

## Recomendaciones

1.	Para implementar los backups desarrollados en este proyecto en un escenario real, se podrían implementar junto con herramientas de monitoreo como Prometheus y Grafana. Contar con dashboards personalizados en Grafana facilitaría identificar tendencias, bottlenecks y problemas en los procesos de backup.

2.	Para establecer backups en Elasticsearch, se recomienda hacer uso de la interfaz interactiva de Kibana para crear políticas de snapshots. Esto en lugar de ejecutar comandos manuales sobre la base Elasticsearch para hacer cada backup de forma individual, ya que provee una experiencia más amigable e intuitiva para los usuarios.

3.	En lugar de tener las credenciales de acceso a la nube y el bucket hardcoded en los scripts de backup, se recomienda almacenar estas credenciales como secrets de Kubernetes. De esta manera se centraliza la gestión de credenciales sensibles y se evita exponerlas en el código. 

4.	Es crítico que el repositorio de código donde se almacena la tarea de backup se mantenga privado y con acceso restringido. De esta manera se evita que personas no deseadas puedan ver el código fuente y obtener las credenciales que dan acceso a la cuenta de AWS u otra plataforma en la nube.

5.	Para optimizar el uso de almacenamiento en AWS, se recomienda hacer uso de una política de retención de backups automatizada. En lugar de retener todos los backups por tiempo indefinido, se recomienda usar una política que conserve los backups más recientes y necesarios, y elimine versiones antiguas que ya no son relevantes.

6.	Es crítico validar periódicamente que al implementar backups, estos sean funcionales y permitan restaurar los datos correctamente. Por eso, al implementar componentes de backups se recomienda realizar pruebas regulares de restore a partir de los mismos para confirmar su correcto funcionamiento y capacidad de recuperación de información.

7.	En una tarea de este tipo, dividir el trabajo es importante, pero también es importante que cada persona del equipo entienda su tarea. Se recomienda mantener una buena comunicación durante el desarrollo del proyecto y nunca quedarse con dudas.

8.	A la hora de probar los backups generados, se recomienda hacer uso de un pod de depuración como el incluido en la solución de esta tarea. Dicho pod proporciona una terminal con conectividad directa al bucket de almacenamiento en AWS. Esto permite validar de forma efectiva que los respaldos se estén ejecutando correctamente y subiendo a la nube según lo esperado.

9.	Cuando se quiera hacer pruebas sobre las bases de datos con API’s se recomienda el uso de aplicaciones como Postman o Thunder Client ya que estos nos ayudan a hacer request HTTP de forma sencilla.  

10.	A la hora de preparar el pod con el aws-cli, se recomienda buscar cómo instalar las herramientas necesarias para hacer el backup específicamente para la plataforma de Amazon Linux. Incluso, puede ser que Amazon tenga una implementación en el repositorio de extras para Amazon Linux, como ocurrió con PostgreSQL

### Referencias
Accessing Neo4J - Operations Manual. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/docs/operations-manual/current/kubernetes/accessing-neo4j/ 

Awesome Procedures on Cypher (APOC) - Neo4J Labs. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/labs/apoc/#:~:text=APOC%20(Awesome%20Procedures%20on%20Cypher,a%20lot%20of%20useful%20functionality. 

Back up an offline database - operations manual. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/docs/operations-manual/current/backup-restore/offline-backup/ 

Back up an online database - operations manual. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/docs/operations-manual/current/backup-restore/online-backup/ 

Back up and restore (online) - Operations manual. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/docs/operations-manual/current/kubernetes/operations/backup-restore/ 

Create a Helm Deployment Values.yaMl file - Operations Manual. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/docs/operations-manual/current/kubernetes/quickstart-standalone/create-value-file/ 

Dump and Load Databases (offline) - Operations Manual. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/docs/operations-manual/current/kubernetes/operations/dump-load/ 

Export - APOC extended documentation. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/labs/apoc/4.1/export/ 

Red Hat, CentOS, Fedora, and Amazon Linux (.RPM) - Operations Manual. (s. f.). Neo4j Graph Data Platform. https://neo4j.com/docs/operations-manual/current/installation/linux/rpm/



