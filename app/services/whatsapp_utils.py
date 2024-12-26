import os
import requests

def enviar_respuesta_con_botones(to, texto, botones):
    """Envía un mensaje con botones interactivos."""
    url = 'https://graph.facebook.com/v17.0/461074520431275/messages'
    headers = {
        'Authorization': f'Bearer {os.getenv("WHATSAPP_API_TOKEN")}',
        'Content-Type': 'application/json'
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": texto
            },
            "action": {
                "buttons": botones
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Botones enviados a {to}")
    else:
        print(f"Error al enviar botones: {response.text}")

def enviar_respuesta_whatsapp(to, message):
    """Envía una respuesta de texto simple a través de WhatsApp."""
    url = 'https://graph.facebook.com/v17.0/461074520431275/messages'
    headers = {
        'Authorization': f'Bearer {os.getenv("WHATSAPP_API_TOKEN")}',
        'Content-Type': 'application/json'
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Mensaje enviado a {to}: {message}")
    else:
        print(f"Error al enviar mensaje: {response.text}")
