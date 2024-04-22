# Chatbot de incidentes de IT - Sistemas Basados en Conocimiento
## Estudiantes

* Alexander Garro
* Sergio Oviedo
* Luis Felipe Soto

## Requerimientos
Para la ejecución de esta solucion necesita instalar Python 3.9 y Node 20.11.0.
* [Python 3.9](https://www.python.org/downloads/release/python-390/)
* [Node 20.11.0](https://nodejs.org/en/blog/release/v20.11.0)

## Ejecución del Modelo de entrenamiento
Se brinda el modelo ya entrenado como parte del repositorio. Sin embargo, si desea ejecutarlo deberá instalar **pandas** y **scikit-learn**



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
cd ..
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
Inicie una conversación con el Chatbot y luego envíe un mensaje. Puede saludarlo o preguntarle por un problema de IT.   

Ejemplo:   
> You: Hello   
> Chatbot: Greetings! What can I do for you today?

> You: Network switch has failed   
> Chatbot: I see what you mean, it would be a good idea to inspect the switch and replace if necessary.

## Sistemas operativos soportados   
Esta solución ha sido probada con los siguientes Sistemas Operativos y sus versiones:   
- Windows 11 Pro 23H2
- Mac OS Sonoma 14.2.1