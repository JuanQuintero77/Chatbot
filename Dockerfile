# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de credenciales
COPY chatbot442216-07e7fb091986.json /app/credentials.json


# Configura la variable de entorno para las credenciales
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

# Copia el archivo requirements.txt e instala dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY app/ app/

# Expone el puerto 5000
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["gunicorn", "-b", ":5000", "app.main:app"]
