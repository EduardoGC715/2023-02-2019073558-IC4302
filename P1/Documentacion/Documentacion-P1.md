# Proyecto 1:  WikiSearc 
# Bases de Datos II

## Documentación

### Mongo Atlas y Mongo Atlas Search
#### Base de datos
La base de datos tiene el nombre de bibliotec, en esta se encuentra una colección donde se van a guardar la información obtenida de los Dumps de Wikidepedia. Los documentos tienen los siguientes campos:
- **_id**: El cual es el identificador único para cada documento. Este es un encriptado del nombre de la página de wikipedia. Es de tipo string.
- **PageBytes**: Este representa la cantidad de bytes que posee la página. Es de tipo int.
- **PageHasRedirect**: Indica si la página tiene links de redireccionamiento. Es de tipo string, ya que los valores booleanos no se les puede generar facets ni ser buscados mediante la busqueda de texto completo.
- **PageId**: Es un identificador único para la página de wikipedia. Es de tipo int.
- **PageLastModified**: Esta es la fecha de la última modificación realizada en la página de wikipedia. Es de tipo date.
- **PageLastModifiedUser**: Este es el último usuario que realizó una modificación sobre la página de Wikipedia. Es de tipo string.
- **PageNamespace**: Este indica el namespace donde se encuentra la página de Wikipedia. Es de tipo string, aunque si valor es numérico, ya que se desea realizar un busqueda textual sobre este campo.
- **PageRedirect**: En este campo se guarda la redireccón que posee la página. Es de tipo string.
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
La base de datos de bibliotec posee un índice de búsqueda el cual hace ... . Este índice posee el siguiente mapping: 
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
Este mapping representa que ... .

### Oracle Autonomous Database

### Oracle NoSQL Database Cloud

### Firebase Real Time Database

### Object Storage

### Diagramas del Proyecto

### Componentes

#### Loader
##### Unit Tests

#### API
##### Unit Tests

#### UI
##### Unit Tests

### Ejecución del Proyecto y pruebas realizadas

### Recomendaciones y Conclusiones (10 c/u)

### Referencias (si hay)