
# Challenge: usuarios y pagos
Para ejecutar el proyecto se debe crear un archivo ".env" siguiendo el ejemplo en "template.env"; reemplazar variable MONGO_URI por la uri de acceso a la database mongo.
Por ejemplo:

    MONGO_URI = mongodb://localhost:27017
#### Ejecutar:
 - `python -m venv venv` para crear carpeta con entorno virtual.
- archivo `activate.bat` ubicado en `venv/Scripts/` para activar entorno venv.
- `pip install -r requirements.txt` para instalar módulos requeridos mediante pip.
- `python create_db.py` para popular la database.
- `python scheduler.py` para ejecutar el programador de los pagos cada 30 días.
