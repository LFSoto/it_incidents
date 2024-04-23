# Chatbot de incidentes de IT - Sistemas Basados en Conocimiento
## Estudiantes

* Alexander Garro
* Sergio Oviedo
* Luis Felipe Soto

## Requerimientos
Para la ejecución de esta solucion necesita instalar Python 3.11.9 y Node 20.11.0.
* [Python 3.11.9](https://www.python.org/downloads/release/python-3119/)
* [Node 20.11.0](https://nodejs.org/en/blog/release/v20.11.0)

## Configurar el ambiente virtual y descargar las dependencias
Para configurar el ambiente virtual y descargar las dependencias de la solución deberá ejecutar los siguientes comandos en el root de la solución desde un powershell.   
```
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```    
Una vez instaladas las dependencias, debido a unos errores de compatibilidad con la versión de Python instalada, se debe hacer un cambio en el código fuente de la librería kanren y unification.

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

## Ejecución del modelo de entrenamiento
Se brinda el modelo ya entrenado como parte del repositorio. Sin embargo, si desea ejecutarlo deberá ejecutar los siguientes comandos:   
```
cd aiclassificator
python .\it_incients.py
```   

Esto generará dos archivos, `it_problem_classifier.pkl` y `vectorizer.pkl`. Estos archivos se encuentran en la carpeta `aiclassificator`.

## Ejecutar la base de datos
Para ejecutar la base de datos deberá ir al folder **backend/database** y ejecutar el archivo `database.py` para crear la base de datos. Desde el root del proyecto ejecutar los siguientes comandos:
``` 
cd backend/database 
python database.py
```

## Ejecutar servicio del backend
Una vez se crea la base de datos, procederemos a ejecutar el servicio que habilita el API REST para la comunicación con el frontend. Desde el root del proyecto ejecutar los siguientes comandos:
```
cd backend 
python chat_service.py
```

## Ejecutar interfaz de usuario
Ahora cuando el servicio del API REST está en ejecución, en otra terminal deberá ejecutar el frontend. Desde el root del proyecto ejecutar los siguientes comandos:
```
cd frontend
npm install
npm start
```

## Ejemplo de ejecución
Inicie una conversación con el Chatbot y luego envíe un mensaje. Puede saludarlo o preguntarle por un problema de IT. Tenga en cuenta que la respuesta no siempre va a ser la misma.

Ejemplo:   
> You: Hello   
> Chatbot: Greetings! What can I do for you today?  

> You: Network switch has failed   
> Chatbot: I see what you mean, it would be a good idea to inspect the switch and replace if necessary.

> You: I have an issue with the mouse, it is not working    
> Chatbot: Thank you for pointing that out, kindly check the mouse connection and replace batteries if wireless.    

> You: My microphone is not capturing the sound when I talk near to it  
> Chatbot: Indeed, a suitable approach would be to check sound settings and speakers/headphones connection. 

## Sistemas operativos soportados   
Esta solución ha sido probada con los siguientes Sistemas Operativos y sus versiones:   
- Windows 11 Pro 23H2
- Mac OS Sonoma 14.2.1