import openai
from dotenv import load_dotenv
import os

class OpenAIUtils:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generar_respuesta(self, pregunta):
        try:
            # Mensaje inicial para contextualizar el propósito del asistente
            mensajes = [
                {"role": "system",
                 "content": "Eres un asistente experto en el dominio de preguntas relacionadas con datos tecnológicos, especialmente los almacenados en bases de datos como BigQuery."},
                {"role": "user", "content": f"{pregunta}"}
            ]

            # Generar la respuesta con OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=mensajes,
                max_tokens=150,  # Limita la longitud de la respuesta
                temperature=0.7  # Ajusta la creatividad
            )

            # Extraer la respuesta generada
            respuesta = response['choices'][0]['message']['content'].strip()

            # Si la respuesta no está relacionada con BigQuery, devuelve un mensaje genérico
            if "no relacionado con BigQuery" in respuesta.lower() or not self.es_relacionada_con_bigquery(pregunta):
                return "Lo siento, no puedo responder esa pregunta ya que no está relacionada con los datos que manejo."

            return respuesta

        except openai.error.OpenAIError as e:
            print(f"Error de OpenAI: {e}")
            return f"Hubo un error al generar la respuesta: {str(e)}"

    def es_relacionada_con_bigquery(self, pregunta):
        # Lógica simple para verificar si la pregunta parece relacionada con BigQuery
        palabras_clave = ["base de datos", "BigQuery", "tabla", "consulta", "SQL", "dataset"]
        return any(palabra in pregunta.lower() for palabra in palabras_clave)