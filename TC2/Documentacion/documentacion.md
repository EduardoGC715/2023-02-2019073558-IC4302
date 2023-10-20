# Bases de Datos II
# Tarea Corta 2  
#### Equipo de trabajo:
Granados Retana, Diego - 2022158363
Granados Retana, Daniel - 2022104692
Mora Montes, Diego - 2022104866
Gutierrez Conejo, Eduardo - 2019073558
José Ricardo Cardona Quesada - 2021022613



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

#### Elastic

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















![Alt text](imgs/BackupElastic/ResultadoPolicy.png)

Paso 1 create policy

![Alt text](imgs/BackupElastic/creacionPolicy.png)

![Alt text](imgs/BackupElastic/dejarigual.png)

![Alt text](imgs/BackupElastic/eliminardespuesCiertoTIempo.png)


Una vez creado el policy

![Alt text](imgs/BackupElastic/CreatePolicy.png)


Despues de crear el policy y repositorio si se crea un backup saldra lo siguiente

![Alt text](imgs/BackupElastic/ExisteSnapshot.png)

Al revisar el repo tambien se podra observar que hay un snapshot disponible

![Alt text](imgs/BackupElastic/HayunSnapshot.png)


Verificar si se subieron al AWS Bucket los backups
![Alt text](imgs/BackupElastic/Ev1Bups.png)

