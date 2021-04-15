# **Fire_Incidents**

## *Overview de la solución*

### Entorno
- Se crea un config.ini con diferentes parámetros a ser utilizados (conexiones a socrata, mysql, etc.)
---
### Base de Datos
- Servidor MySQL local montado con docker, se refresca todo el ambiente. 
- Se crea una base de datos fire_incidents y diseña un modelo estrella con una fact_table y 27 dimensiones alrededor de ella. 
- El proceso está preparado para recrear el modelo en cada ejecución.
---
### Fuente de Datos:
- Respecto a la extracción desde el source, se creó una librería que recibe las peticiones de extracción y basados en config.ini utiliza dichos parametros en su conexión y request (por ejempo limit_size)
- Disclaimer sobre la calidad de los datos:
    - Se renombraron algunas columnas que decían "Sytem" en lugar de "System" y se le limpiaron los espacios a las mismas.
    - Se detectaron muchos valores de atributos que deberían ser el mismo pero el data cleanse quedó fuera del scope del ejercicio.
---
### Sobre las tablas
- Se crean dimensiones basadas en default_dimensions.txt y compound_dimensions.txt:
    - default_dimensions: extrae el atributo del source (por ejemplo City) y genera un Id respectivo.
    - compound_dimensions: extrae de más de un atributo del source cuando estos corresponden al mismo concepto (por ejemplo, el concepto action_taken es el mismo para los campos "action_taken_other", "action_taken_secondary", "action_taken_primary").
    - en caso de modificarse las reglas de negocio y querer agregar/eliminar una dimensión, se modifican los txt correspondientes que están en forma de dictionary y el proceso lo tomará dinámicamente en la próxima ejecución y el modelo se refrescará acorde a los cambios.
    - los campos que en el source eran atributos convertidos a dimensión se los reemplaza por sus respectivos Id's subrogados.
---
### Algunos reportes generados desde la base de datos:
#### Average Incidents Resolution Time by each Battalion
![alt text](https://github.com/jboianover/fire_incidents/blob/master/avg_resolution_time_by_battalion.PNG)
---
#### Fire Incidents per day by Neighborhood District
!]alt text](https://github.com/jboianover/fire_incidents/blob/master/fire_incidents_per_day_by_neighborhood.PNG)


