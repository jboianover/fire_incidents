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
### Sobre las tablas y la solución
- Se crean dimensiones basadas en default_dimensions.txt y compound_dimensions.txt:
    - default_dimensions: extrae el atributo del source (por ejemplo City) y genera un Id respectivo.
    - compound_dimensions: extrae de más de un atributo del source cuando estos corresponden al mismo concepto (por ejemplo, el concepto action_taken es el mismo para los campos "action_taken_other", "action_taken_secondary", "action_taken_primary").
    - en caso de modificarse las reglas de negocio y querer agregar/eliminar una dimensión, se modifican los txt correspondientes que están en forma de dictionary y el proceso lo tomará dinámicamente en la próxima ejecución y el modelo se refrescará acorde a los cambios.
    - los campos que en el source eran atributos convertidos a dimensión se los reemplaza por sus respectivos Id's subrogados.
---
### Algunos reportes generados desde la base de datos:
#### Average Incidents Resolution Time by each Battalion
![alt text](https://github.com/jboianover/fire_incidents/blob/main/avg_resolution_time_by_battalion.PNG)

---
#### Fire Incidents per day by Neighborhood District
![alt text](https://github.com/jboianover/fire_incidents/blob/main/fire_incidents_per_day_by_neighborhood.PNG)

---
## *Instrucciones de instalación*

### **Para montar un servidor MySQL se asume que se cuenta con docker instalado en la máquina donde se probará la solución**

### Levantar una instancia mysql

> docker run --name mysql1 -e MYSQL_ROOT_PASSWORD=root -d mysql:latest
 
Aparentemente por temas de seguridad no se puede acceder a la misma desde fuera de la imagen de docker

- Para poder acceder desde nuestra máquina local:
> docker logs mysql1 2>&1 | grep GENERATED
- Se solicitará ejecutar la sentencia ALTER USER con valores root/root
- Ejecutar:
> update mysql.user set host = '%' where user='root';
- Ejecutar:
> docker restart mysql1
- Ahora estaremos en condiciones de poder acceder a la base de datas desde MySQL Workbench - descargarlo y comenzar a utilizarlo.

## Librerias de Python a instalar
- pandas
- sodapy
- mysql.connector
- sqlalchemy
- numpy
- ast
- numpy
- logging
- os
- pathlib
- configparser