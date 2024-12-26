from flask import Flask
from app.routes.whatsapp_routes import whatsapp_bp, init_dependencies
from app.services.bigquery_utils import BigQueryUtils
from app.services.user_state import UserState
from app.services.openai_utils import OpenAIUtils
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Leer la ruta del archivo de credenciales de Google
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Validar que la variable de entorno esté configurada
if not credentials_path:
    raise ValueError("La variable 'GOOGLE_APPLICATION_CREDENTIALS' no está configurada en el archivo .env")

# Inicializar las credenciales para Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Inicialización de servicios
bigquery_utils = BigQueryUtils(credentials_path)
user_state = UserState()
ai_utils = OpenAIUtils()

# Crear la aplicación Flask
app = Flask(__name__)

# Inicializar dependencias del Blueprint
init_dependencies(bigquery_utils, user_state)

# Registrar Blueprints
app.register_blueprint(whatsapp_bp, url_prefix='/webhook')

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(port=5000)
