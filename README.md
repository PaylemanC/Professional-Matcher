# ProfessionalMatch
Permite a un desarrollador cargar su perfil profesional y compararlo con ofertas laborales IT, generando un análisis de compatibilidad para identificar coincidencias y diferencias entre el perfil y la vacante. Ayuda a optimizar postulaciones, adaptar el perfil a cada oportunidad y destacar habilidades relevantes.

### Tecnologías utilizadas

| Librería/Framework | Uso |
| --- | --- |
| **Django** | Framework para la creación general de la web |
| **Scikit-learn** | Cálculo de similitud coseno entre embeddings para comparar textos |
| **Sentence-Transformers** | Generación de embeddings semánticos de textos para análisis de similitud |
| **KeyBERT** | Extracción de palabras clave relevantes |
| **Spacy** | Procesamiento de lenguaje natural, lematización y tokenización en español en los utils.py |
| **NumPy** | Manipulación de arrays para embeddings y operaciones del EmbeddingCache |

## Instalación

1. **Clona el repositorio**

```bash
git clone https://github.com/PaylemanC/Professional-Matcher.git
cd Professional-Matcher
```

2. **Crea y activa un entorno virtual**

    _*Para desactivar el entorno puedes usar `deactivate`._

```bash
python -m venv env

# Windows
env\Scripts\activate
# Mac/Linux
source env/bin/activate
```


3. **Instala dependencias**

    *Este proceso puede demorar. 

```bash
pip install -r requirements.txt
```


4. **Crea y configura tu local.py + database**

    Crea un archivo **local.py** _(es importante que sea este y no otro nombre)_ en la carpeta **professionalmatch/settings**.

    Copia y completa la siguiente estructura en **local.py**:

```python
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '', # Nombre de la base de datos
        'USER': 'root', # Usuario default u otro
        'PASSWORD': '', # Contraseña
        'HOST': 'localhost',
        'PORT': '3306', # Puerto default u otro
        'OPTIONS': {
            'sql_mode': 'traditional'
        }
    }
}

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

*Asegúrate de tener creada la base de datos en MySQL con el nombre que hayas especificado en `NAME`:
```bash
mysql -u root -p
```

```sql
CREATE DATABASE professional_match;
USE professional_match;
```

4. **Aplica migraciones + fixtures**

Migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

Fixtures:

```bash
python manage.py loaddata technologies.json
```

5. **Opcional: Crea un superusuario**

```bash
python manage.py createsuperuser
```

## Run server local

```bash
python manage.py runserver
```

Y accede en tu navegador en (default):

```sh
http://127.0.0.1:8000/
```

## Testing
Correr tests de los modelos: 

```bash
python manage.py test
```