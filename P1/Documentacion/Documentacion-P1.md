# Proyecto 1:  WikiSearc 
# Bases de Datos II

## Documentación

### Instrucciones para ejecutar el proyecto

Instrucciones de cómo acceder a la máquina virtual
Para acceder a la máquina virtual, primero es necesario acceder al directorio donde se encuentran los archivos del proyecto. Este contiene la llave ssh para conectarse a la máquina virtual. Luego, podemos ejecutar el siguiente comando para conectarnos:
```
ssh -i ssh/db2 ubuntu@{IP pública de la máquina virtual}
```
Ejemplo:
```
ssh -i ssh/db2 ubuntu@207.211.179.27
```
Luego, para poder correr comandos de Docker, debemos elevar el usuario a nivel de root con:
```
sudo -i
```
Ya con esto, podemos ejecutar comandos de Docker para verificar que los 3 componentes están corriendo:
```
docker ps
```
![vmdocker](src/vm.png)

Cuando ya se logra entrar a la máquina virtual, se obtiene la siguiente página principal.
![login](src/login.png)
Uno puede ingresar los datos para ingresar al programa. Estos se validarán con los datos ingresados en Firebase. Si se desea registrar, hay que presionar en el botón de Sign Up. Esto llevará el usuario a la siguiente página.
![register](src/register.png)
Aquí, es necesario que la contraseña tenga al menos 6 caracteres y que el número de teléfono tenga el código de area. Por ejemplo, +50612345678. Luego de que se presione el botón de registrar, si el usuario se pudo registrar, se muestra este mensaje de éxito.
![usercreated](src/usercreated.png)
Si no se pudo registrar:
![userfailed](src/userfailed.png)
Luego de ingresar al sistema, se llegará a la siguiente pantalla.
![emptysearch](src/emptysearch.png)
Esta es la página para buscar los documentos. Aquí podemos notar que tanto los facets como los documents están vacíos. Esto es porque se llenan dinámicamente con base en lo que uno buscó. En los botones de arriba uno puede seleccionar de cuál base de datos se buscan los documentos. Para esto, se ingresa el valor que se quiere buscar y se presiona en la lupa.
![fullsearch](src/fullsearch.png)
Esta es la página que aparece cuando uno busca algo. En este ejemplo, buscamos potato y estos fueron los facets que se generaron y los documentos que se encontraron. Uno puede seleccionar los facets con los que se quiere buscar y luego volver a presionar en el botón de search para buscar con ese facet. 
![facetsearch](src/facetsearch.png)
Por ejemplo, estos son los resultados cuando se busca potato con el facet de Chris the speller.
Se pueden presionar en los links del documento, al texto azul subrayado, para ir a una página donde se muestra el documento completo.
![documentpage](src/documentpage.png)
### Pruebas realizadas y pasos para reproducirlas
Para probar los endpoints del API, utilizamos Thunder Client. Esta es una extensión en Visual Studio Code que envía requests HTTP a un endpoint que uno le indique. Uno puede configurar los headers y el cuerpo, el cual puede ser un JSON, XML, Text, Form, Form-encoded, GraphQL y Binary. Por ejemplo, en el caso del login y register, los datos se envían por medio de JSON. 

Para probar el loader, se creó un unit test que revisa las funciones de transformación para insertar en las tablas auxiliares de Autonomous Database. Para correrla, simplemente hay que correr el archivo test_loader.py. Este también se debería cada vez que se crea un contenedor de Docker con el loader.

### Resultados de las pruebas unitarias
![unittestlogin](src/unittestlogin.png)
Resultado de la prueba del loader:
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK

### Mongo Atlas y Mongo Atlas Search
#### Base de datos
La base de datos tiene el nombre de bibliotec, en esta se encuentra una colección donde se van a guardar la información obtenida de los Dumps de Wikipedia. Los documentos tienen los siguientes campos:
- **_id**: El cual es el identificador único para cada documento. Este es un encriptado del nombre de la página de wikipedia. Es de tipo string.
- **PageBytes**: Este representa la cantidad de bytes que posee la página. Es de tipo int.
- **PageHasRedirect**: Indica si la página tiene links de redireccionamiento. Es de tipo string, ya que los valores booleanos no se les puede generar facets ni ser buscados mediante la busqueda de texto completo.
- **PageId**: Es un identificador único para la página de wikipedia. Es de tipo int.
- **PageLastModified**: Esta es la fecha de la última modificación realizada en la página de wikipedia. Es de tipo date.
- **PageLastModifiedUser**: Este es el último usuario que realizó una modificación sobre la página de Wikipedia. Es de tipo string.
- **PageNamespace**: Este indica el namespace donde se encuentra la página de Wikipedia. Es de tipo string, aunque si valor es numérico, ya que se desea realizar un busqueda textual sobre este campo.
- **PageRedirect**: En este campo se guarda la redirección que posee la página. Es de tipo string.
- **PageRestrictions**: Es un array con las restricciones que posee la página. Es de tipo array de strings.
- **PageText**: En este campo se encuentra el texto de la página. Es de tipo string.
- **PageTitle**: Representa el título de la página. Es de tipo string.
- **SiteInfoDBName**: Representa el nombre de la base de datos del sitio. Es de tipo string.
- **SiteInfoName**: Representa el nombre del sitio donde se encuentra la información. Es de tipo string.
- **SiteLanguage**:  Representa el lenguaje en el que se encuentran los documentos. Es de tipo string.
- **pageWikipediaGenerated**: Representa el link generado de forma automática. Es de tip string.
- **PageLinks**: Es un arreglo con los links asociados a la página. Es de tipo array de strings.
- **PageNumberLinks**: Representa la contidad de links que posee a página. Es de tipo int.
- **PageWikipediaLink**: Es el link donde se encuentra la página. Es de tipo string.

#### Search Index
La base de datos de bibliotec posee un índice de búsqueda el cual hace posible la búsqueda de texto completo sobre los campos que son de tipo string. Este índice posee el siguiente mapping:
```
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "PageBytes": [
        {
          "indexDoubles": false,
          "representation": "int64",
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "representation": "int64",
          "type": "numberFacet"
        }
      ],
      "PageHasRedirect": [
        {
          "type": "string"
        },
        {
          "type": "stringFacet"
        }
      ],
      "PageId": [
        {
          "representation": "int64",
          "type": "number"
        },
        {
          "type": "string"
        }
      ],
      "PageLastModified": [
        {
          "type": "string"
        },
        {
          "type": "date"
        },
        {
          "type": "dateFacet"
        }
      ],
      "PageLastModifiedUser": [
        {
          "type": "string"
        },
        {
          "type": "stringFacet"
        }
      ],
      "PageLinks": {
        "type": "string"
      },
      "PageNamespace": [
        {
          "type": "string"
        },
        {
          "type": "stringFacet"
        }
      ],
      "PageNumberLinks": [
        {
          "representation": "int64",
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "representation": "int64",
          "type": "numberFacet"
        }
      ],
      "PageRedirect": {
        "type": "string"
      },
      "PageRestrictions": [
        {
          "type": "string"
        },
        {
          "type": "stringFacet"
        }
      ],
      "PageText": {
        "type": "string"
      },
      "PageTitle": {
        "type": "string"
      },
      "PageWikipediaLink": {
        "type": "string"
      },
      "SiteInfoDBName": [
        {
          "type": "string"
        },
        {
          "type": "stringFacet"
        }
      ],
      "SiteInfoName": [
        {
          "type": "string"
        },
        {
          "type": "stringFacet"
        }
      ],
      "SiteLanguage": [
        {
          "type": "string"
        },
        {
          "type": "stringFacet"
        }
      ],
      "pageWikipediaGenerated": {
        "type": "string"
      }
    }
  }
}
```
En este índice se definen los tipos de los campos que van a ser utilizados para las búsquedas de texto y los campos que deben de generar facets con buckets para realizar filtros, estos facets pueden ser de tipo string, numéricos, y de fechas. Por ejemplo el campo llamado “SiteLanguage” posee dos tipos, uno de tipo string para realizar las búsquedas,  y otro de tipo facet que genera las categorías donde los documentos que retorna la búsqueda puedan ser clasificados.

### Diagramas del Proyecto
#### Arquitectura
![diagram](src/diagram.png)
#### Oracle Autonomous Database
![autonomousdiagram](src/autonomousdiagram.png)


