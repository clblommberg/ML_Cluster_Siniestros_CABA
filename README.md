# Análisis de Siniestros Viales en la región de CABA en los periodos 2016 y 2021

## Descripción
Este proyecto tiene como objetivo analizar los datos de siniestros viales fatales (homicidios) en la Ciudad de Buenos Aires, Argentina. Los datos provienen de diferentes fuentes gubernamentales y contienen información sobre las víctimas, las ubicaciones geográficas, las características de los siniestros y los datos demográficos de las comunas de la ciudad.

## Contenido
- Datasets y Recursos de Análisis `/datasets`.
- Código fuente en Python para la descarga, preprocesamiento, análisis y visualización de datos `/notebooks`.
- Modelo sqlalchemy en el proyecto migrados a PosgreSQL `/server`.
- Dashboard del proyecto KPI 10% reducción Siniestros Viales Semestre Anterior y KPI 7% reducción Siniestros Viales tipo Moto :
<br>

**[Tableau Siniestros Fatales](https://public.tableau.com/app/profile/claudio.quispe/viz/sinistrosdb/SiniestrosViales?publish=yes)**



**Análisis Exploratorio de Datos (EDA)**<br>
- Se han realizado análisis descriptivos de cada tabla, destacando estadísticas como la moda, mediana y media para variables clave.<br>
- El análisis de correlación en el modelo de "Siniestros Fatales" revela patrones significativos. La correlación muy fuerte (0.98) entre "anio" e "id" indica una relación temporal positiva. La correlación moderada negativa (-0.68) entre "comuna_x" y "longitud" sugiere una posible relación inversa entre la comuna y la longitud geográfica.<br>

En términos del impacto en la población total ("total_pob"), las correlaciones positivas de 0.31 y 0.45 con "area" y "perimetro", respectivamente, sugieren que un mayor área y perímetro están asociados con una población total más grande.
**Detección de Valores Anómalos y Nulos**<br>
- Se han identificado y registrado valores faltantes en los DataFrames, y se ha generado un resumen de la presencia de valores `'SD', 'No especificado', 'sd' , '', 'Point (. .)']`.
- El análisis de valores faltantes revela que la columna "Altura" en el DataFrame "homicidios" tiene el mayor porcentaje de valores faltantes (81.47%). La columna "FECHA_FALLECIMIENTO" en "victima_h" no tiene valores nulos, pero tiene un 9.48% de valores raros. Otros porcentajes de valores faltantes oscilan entre 0.14% y 9.48%. Estos resultados señalan áreas críticas para la imputación o eliminación de datos.<br>

**Interpretación de Modelos Relacionales (DBML)**<br>
- Se ha proporcionado un modelo relacional en DBML para representar las relaciones entre las tablas homicidios_h, victimas_l, comunas_l, y censo_l.
- Cada tabla tiene sus columnas definidas con tipos de datos adecuados y relaciones clave para facilitar futuras consultas.

**Análisis de clústeres:**

En cuanto al análisis de clústeres, el código aplica dos enfoques principales:

 [![output-cluster.png](https://i.postimg.cc/05KrTTdt/output-cluster.png)](https://postimg.cc/23mzvXtv)

1. **Método del codo (Elbow Method) con K-Means:**
   - Se utiliza el método del codo para determinar el número óptimo de clústeres a utilizar en el algoritmo K-Means.
   - Se escalan los datos numéricos utilizando `StandardScaler` antes de aplicar el algoritmo K-Means.
   - Cluster 0 (Alto Riesgo): Este conjunto exhibe un riesgo elevado con un promedio de aproximadamente 315.76 víctimas, concentradas en comunas de baja latitud. Los siniestros fatales suelen acontecer en áreas densamente pobladas, con un promedio de población total de alrededor de 20.5 millones, y presentan una proporción significativa de varones, aproximadamente el 30.69%. Además, hay un leve sesgo hacia el uso de avenidas como tipo de calle, con un promedio del 29.05%. La edad promedio de las víctimas es relativamente joven, alrededor de 16 a 18 años.

   - Cluster 1 (Moderado Riesgo y Alta Cantidad de Víctimas): Este grupo presenta un riesgo moderado con una cantidad significativa de víctimas, con un promedio de aproximadamente 350.36. Estos siniestros ocurren principalmente en comunas con latitud y longitud moderadas. Asimismo, están asociados con áreas más pobladas, con un promedio de población total de aproximadamente 14.8 millones, y muestran un equilibrio relativo entre varones y mujeres, con un promedio del 50.28%. Se observa una mayor diversidad en los tipos de calles, indicando posibles incidentes en entornos diversos, con un promedio del 12.89%. La edad promedio de las víctimas es moderada, alrededor de 13 -71 años.

   - Cluster 2 (Bajo Riesgo y Cantidad Moderada de Víctimas): Este conjunto, con un promedio de aproximadamente 362.31 víctimas, se asocia con comunas de mayor latitud y longitud. Los siniestros tienden a ocurrir en áreas menos densamente pobladas, con un promedio de población total de alrededor de 14.5 millones, y muestran un equilibrio relativo entre varones y mujeres, con un promedio del 42.03%. La presencia de acusados relacionados con cargas y motos sugiere incidentes de tráfico menos complejos, con promedios de aproximadamente 0.22 y 5.17%, respectivamente. La edad promedio de las víctimas es moderada, alrededor de 11-26 años.

   - Cluster 3 (Moderado Riesgo con Alta Cantidad de Víctimas): Este grupo presenta un riesgo moderado con una cantidad alta de víctimas, con un promedio de aproximadamente 362.78. Los siniestros tienden a ocurrir en comunas con latitud y longitud moderadas y áreas densamente pobladas, con un promedio de población total de alrededor de 11.8 millones. Se observa una proporción relativamente equitativa de varones y mujeres, con un promedio del 32.17%. La presencia de acusados relacionados con cargas y motos sugiere una variedad de incidentes de tráfico, con promedios de aproximadamente 5.62% cada uno. La edad promedio de las víctimas es moderada, alrededor de 10 - 46 años.

   - Cluster 4 (Bajo Riesgo y Cantidad Baja de Víctimas): Este conjunto, con un promedio de aproximadamente 300.33 víctimas, se asocia con comunas de mayor latitud y longitud. Los siniestros tienden a ocurrir en áreas menos densamente pobladas, con un promedio de población total de alrededor de 15.3 millones, y presentan una proporción relativamente equitativa de varones y mujeres, con un promedio del 31.08%. La presencia de acusados relacionados con bicicletas y peatones sugiere incidentes de menor gravedad en entornos menos urbanos, con promedios de aproximadamente 31.25% y 16.67%, respectivamente. La edad promedio de las víctimas es relativamente joven, alrededor de 11 - 35 años.


2. **Análisis de Componentes Principales (PCA):**
   - Se aplica PCA para reducir la dimensionalidad de los datos y facilitar la visualización.
   - Se grafica un diagrama de dispersión con las dos principales componentes, coloreando los puntos según su clúster asignado por K-Means.
   - El Análisis  ha permitido reducir la dimensionalidad de los datos, proporcionando una visión más clara de las relaciones y patrones subyacentes en los siniestros fatales. Al observar las estadísticas del modelo PCA, podemos destacar que las dos componentes principales (pca1 y pca2) tienen una media cercana a cero y desviaciones estándar moderadas, lo que sugiere una distribución equilibrada y una variabilidad significativa en los datos proyectados.<br>

   - La media cercana a cero en ambos componentes sugiere una buena centralización de los datos. La desviación estándar indica una dispersión moderada alrededor de la media, con valores mínimo y máximo que abarcan un rango significativo.<br>

   - En el gráfico de dispersión resultante del PCA, se observa una separación clara entre los cinco clusters (representados por colores distintos). La dispersión y orientación de los puntos indican la varianza y la correlación entre las variables originales en el espacio reducido. Este enfoque permite visualizar la estructura inherente en los datos y puede facilitar la interpretación de patrones y relaciones entre observaciones.<br>


Estas técnicas de clusterización permiten identificar patrones y agrupar los datos en función de sus similitudes. Los resultados obtenidos pueden ser útiles para segmentar los siniestros viales, identificar factores comunes o realizar análisis más específicos para cada clúster.
Es importante destacar que el código también incluye visualizaciones adicionales, como mapas de calor, gráficos de barras y gráficos de líneas, que brindan una comprensión más profunda de los datos y las relaciones entre las variables.


## Requisitos
- Python 3.10.11
- Bibliotecas Python: requests, gzip, shutil, tqdm, BeautifulSoup, datetime, math, pathlib, pandas, numpy, re, unidecode, matplotlib, seaborn, plotly, IPython, geopandas, geojson, shapely, sklearn.
- PostgreSQL (PostgreSQL) 15.6
- Tableau Desktop 2024.1.0
## Modelo Relacional PostgreSQL
[![modelo-relacional.png](https://i.postimg.cc/wxtjhx8F/modelo-relacional.png)](https://postimg.cc/s1rzzr2Z)


Claro, puedo mejorar las referencias. Aquí tienes una versión mejorada:

### Referencias

- soyHenry/PI_ML_OPS at FT. (2024). GitHub Repository. [Link](https://github.com/soyHenry/PI_ML_OPS/tree/FT)
- Frogames. (2014). "Masterclass En Inteligencia Artificial: Con Proyectos Reales." Frogames Formación. [Enlace](https://cursos.frogamesformacion.com/courses/ia-moderna). Consultado el 22 de Marzo de 2024.


‌
