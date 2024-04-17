# TODO

# Modelo
pip install pandas
pip install scikit-learn


Archivos 
backend\venv\lib\python3.10\site-packages\kanren\util.py
backend\venv\lib\python3.10\site-packages\unification\core.py

Buscar uso de la librería collections y cambiarlo por collections.abc
Antes
util.py 
from collections import Hashable
Con el cambio 
from collections.abc import Hashable

core.py
Antes
from collections import Iterator
Con el cambio 
from collections.abc import Iterator