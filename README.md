# IT Incident Chatbot - Knowledge-Based Systems
This Chatbot is designed to automate responses and provide immediate assistance for common IT-related issues within organizations. Utilizing artificial intelligence, it integrates a machine learning model to classify IT incidents based on user queries and responds using a previously defined relation of issues and solutions, the chatbot intelligently classifies IT incidents, communicates through a RESTful API developed with Flask, and offers a user-friendly interface built with React.

## Developers

* Alexander Garro (agarrod@ucenfotec.ac.cr)
* Sergio Oviedo (soviedos@ucenfotec.ac.cr)
* Luis Felipe Soto (lsotocr@ucenfotec.ac.cr)

## Requirements
To run this solution, you need to install Python 3.11.9 and Node 20.11.0.
* [Python 3.11.9](https://www.python.org/downloads/release/python-3119/)
* [Node 20.11.0](https://nodejs.org/en/blog/release/v20.11.0)

## Set up the virtual environment and download dependencies
To set up the virtual environment and download the solution dependencies, you must execute the following commands in the solution root directory from a **Windows PowerShell** terminal.
```
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```    
Once the dependencies are installed, due to some compatibility errors with the installed Python version, a change must be made in the source code of the Kanren and unification libraries.

Search for the use of the **collections** library and change it to **collections.abc** for the files:   
```venv\Lib\site-packages\kanren\util.py```  
```venv\Lib\site-packages\unification\core.py```

#### Example of the change:
``` py
# For util.py:   
from collections import Hashable  
# Change to:    
from collections.abc import Hashable

# For core.py:   
from collections import Iterator   
# Change to:      
from collections.abc import Iterator
```

## Train the model
The model is already trained and the files are provided as part of the repository. However, if you want to run it, you should execute the following command from the root folder:   
```
python .\aiclassificator\it_incients.py
```   

This will generate two files, `it_problem_classifier.pkl` and `vectorizer.pkl`. These files are located in the `aiclassificator` folder.

## Run the database
To run the database, from the project **root folder**, execute the following commands:
``` 
python .\backend\database\database.py
```

## Run backend service
Once the database is created, we will proceed to run the service that enables the REST API for communication with the frontend. From the project **root folder**, execute the following commands:
```
python .\backend\chat_service.py
```

## Run user interface
Now, when the REST API service is running, in another **Windows PowerShell** terminal, you should run the frontend. From the project **root folder**, execute the following commands:
```
cd frontend
npm install
npm start
```

## Execution example
Start a conversation with the Chatbot and then send a message. You can greet it or ask about an IT problem. Keep in mind that the response will not always be the same.

Example:   
> You: Hello   
> Chatbot: Greetings! What can I do for you today?  

> You: Network switch has failed   
> Chatbot: I see what you mean, it would be a good idea to inspect the switch and replace if necessary.

> You: I have an issue with the mouse, it is not working    
> Chatbot: Thank you for pointing that out, kindly check the mouse connection and replace batteries if wireless.    

> You: My microphone is not capturing the sound when I talk near to it  
> Chatbot: Indeed, a suitable approach would be to check sound settings and speakers/headphones connection. 

## Supported Operating Systems   
This solution has been tested with the following Operating Systems and their versions:  
- Windows 11 Pro 23H2
