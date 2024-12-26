import requests

url = "http://127.0.0.1:5000/webhook/enviar_alertas"
response = requests.post(url)

if response.status_code == 200:
    print("Alerta enviada con éxito:", response.json())
else:
    print("Error al enviar la alerta:", response.status_code, response.text)
