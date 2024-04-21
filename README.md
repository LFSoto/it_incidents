# Chatbot de incidentes de IT - Sistemas Basados en Conocimiento
## Estudiantes

* Alexander Garro
* Sergio Oviedo
* Luis Felipe Soto

## Requerimientos
Para la ejecución de esta solucion necesita instalar Python 3.10 y Node 20.11.0.
* [Python 3.10](https://www.python.org/downloads/release/python-3100/)
* [Node 20.11.0](https://nodejs.org/en/blog/release/v20.11.0)


## Modelo
```
pip install pandas
pip install scikit-learn
``` 

## Instrucciones para configurar el backend
En este paso, desde una consola de comandos, entraremos al folder backend para configurar y levantar el ambiente virtual de Python donde se instalarán las dependencias. 
```
cd backend
python -m venv venv
venv/bin/activate
pip install -r requirements.txt
```

Debido a unos errores de compatibilidad con la versión de Python instalada, se debe hacer un cambio en el código fuente de la librería kanren.

Buscar uso de la librería **collections** y cambiarlo por **collections.abc** para los archivos:
```backend\venv\lib\python_version\site-packages\kanren\util.py```  
```backend\venv\lib\python_version\site-packages\unification\core.py```



#### Ejemplo del cambio:

Para util.py:   
`from collections import Hashable`    
Cambiar a:   
`from collections.abc import Hashable`

Para core.py:   
`from collections import Iterator`   
Cambiar a:   
`from collections.abc import Iterator`


## Ejecutar la base de datos
Una vez hecho los cambios manuales en los paquetes instalados, deberá ir al folder **backend** y ejecutar el archivo **database.py** para crear la base de datos.
``` 
cd backend 
python database.py
```

## Ejecutar servicio del backend
Una vez se crea la base de datos, procederemos a ejecutar el servicio que habilita el API REST para la comunicación con el frontend. Dentro de la carpeta **backend** ejecutar el archivo **chat_service.py**.
```
cd backend 
python chat_service.py
```

## Ejecutar interfaz de usuario
Ahora cuando el servicio del API REST está en ejecución, deberá ejecutar el frontend. Para esto regresará a la carpeta raíz y dentro de la carpeta **frontend** ejecutar los comandos npm a continuación:
```
cd frontend
npm install
npm start
```

## Ejemplo de ejecución
Inicie una conversación con el Chatbot y luego envíe un mensaje.

## Sistemas operativos soportados

- Windows 11 Pro 23H2
- Mac OS Sonoma 14.2.1