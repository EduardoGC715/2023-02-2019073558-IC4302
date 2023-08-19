### José Eduardo Gutiérrez Conejo - 2019073558 
### Bases de Datos II
### Lectura 2: Prometheus & Grafana

1. ¿En qué consisten los datos timeseries?

    Estos datos son una colección de observaciones obtenidas a través de mediciones repetidas a lo largo del tiempo. Las métricas de los datos timeseries se refieren a una pieza de datos que se rastrea en un incremento en el tiempo. Por ejemplo, una métrica podría referirse a cuánto inventario se vendió en una tienda de un día para otro.

1. ¿Qué son métricas?
   
   Son una medida numérica, estas son importantes para entender por qué una aplicacion trabaja decierta manera. Por ejemplo en una base de datos explica el porqué esta puede volverse lenta si el número de consultas es alto, este caso se llama el request count metric, y con esta información se puede detecatar el problema y aumentar la cantidad de servidores para aumentar la capacidad.

2. ¿Explique en que consiste la Observabilidad?

    La observabilidad se refiere en TI y computación en la nube, a la capacidad de medir el estado actual de un sistema en función de los datos que genera, como registros, métricas y seguimientos.

    La observabilidad se basa en la telemetría derivada de la instrumentación que proviene de los puntos finales y los servicios en sus entornos informáticos de múltiples nubes.

3. ¿Explique el concepto de dimensiones en datos timeseries?

    Este concepto hace referencia a categorías de datos. Los valores de dimensión son nombres, descripciones u otras características de una categoría. Por ejemplo: 
    - Dimensión de intervalo de fechas: Se utiliza como base para limitar el rango de fechas del gráfico. Por ejemplo, esta es la dimensión utilizada si establece una propiedad de intervalo de fechas para el gráfico o si un lector del informe utiliza un control de intervalo de fechas para limitar el período de tiempo.
    - Dimensión de tiempo: Determina la granularidad de la serie temporal. Por ejemplo, para visualizar datos diarios, utilice el tipo de datos Fecha con año, mes y día completos.
    - Dimensión de desglose: Esta opción muestra los datos de la métrica desglosados ​​según la dimensión seleccionada. Por ejemplo, un gráfico que muestre datos de ventas anuales podría desglosarse por una dimensión de región de ventas para mostrar las ventas por región.
&nbsp;

1. ¿Por qué los tags en métricas permiten generar mejores gráficos en Grafana?

    Los tags en métricas mejoran la generación de gráficos en Grafana al permitir la segmentación, filtrado y agrupación de datos según atributos como fuente, ubicación o dispositivo. Esto posibilita una organización más efectiva de los datos, la creación de gráficos específicos para diferentes categorías, comparaciones y análisis detallados. Además, los tags añaden contexto y flexibilidad, mejorando la interpretación de los gráficos y la toma de decisiones.

2. Suponiendo que se están recolectando datos IoT (Internet of Things) de miles de dispositivos, los mismos generan una métrica cada 15 segundos con el consumo de energía y temperatura, explique:
   - ¿Porque una base de datos relacional no es una buena opción para almacenar esta información?

    Una base de datos relacional no es ideal para almacenar datos de IoT debido a su rigidez de esquema, falta de escalabilidad para grandes volúmenes de datos de series temporales generados por dispositivos, almacenamiento ineficiente, dificultades en consultas complejas, problemas de latencia y rendimiento en alta concurrencia, y costos asociados. En su lugar, bases de datos especializadas en series temporales, como las NoSQL, son más apropiadas para manejar eficientemente la recopilación y análisis de datos de IoT.

   - Dada la naturaleza de datos timeseries, ¿De qué forma la localidad puede ayudarnos a ahorrar dinero?
  
        La localidad puede ayudarnos a ahorrar dinero si se necesita procesar volúmenes masivos de datos, la localización de datos mejora los tiempos de procesamiento y ejecución y reducir el tráfico de red; para esto se mueve el sistema cerca de donde residen los datos reales en el nodo, en lugar de mover grandes cantidades de datos. Esto significa una toma de decisiones más rápida, un mejor servicio al cliente, menor carga de red y un uso mucho más eficiente del ancho de banda limitado lo que ayuda a reducir costos y aumentar el rendimiento general de la red y del sistema.

### Referencias
Influx Data (s.f.). What is time series data? Recuperado el 18 de agosto de 2023, de https://www.influxdata.com/what-is-time-series-data/

Livens, J. (26 de enero de 2023). What is observability? Not just logs, metrics and traces. Recuperado el 18 de agosto de 2023, de https://www.dynatrace.com/news/blog/what-is-observability-2/#:~:text=In%20IT%20and%20cloud%20computing,in%20your%20multicloud%20computing%20environments.

Pattinson, T. (9 de noviembre de 2022). Relational vs. Non-Relational Databases. Pluralsight. Recuperado el 18 de agosto de 2023, de https://www.pluralsight.com/blog/software-development/relational-vs-non-relational-databases#:~:text=The%20non-relational%20database%2C%20or,type%20of%20data%20being%20stored.

Decoder (s.f). Data Locality. Thoughtworks. Recuperado el 18 de agosto de 2023, de https://www.thoughtworks.com/insights/decoder/d/data-locality#whatsinitforyou