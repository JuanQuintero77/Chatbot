
# 🤖 Chatbot Inteligente con WhatsApp, BigQuery y Google Cloud

Este repositorio contiene un proyecto de chatbot que conecta la **API de WhatsApp (Meta)** con **Google BigQuery**, permitiendo respuestas automáticas basadas en datos y generación de alertas en tiempo real.

> 🧠 Ideal para empresas que necesitan atención automatizada basada en información en tiempo real, dashboards conversacionales o notificaciones proactivas.

---

## 🚀 Funcionalidades principales

- ✅ Integración con la **API oficial de WhatsApp**
- 🔎 Consulta dinámica de datos desde **BigQuery**
- 📈 Generación de respuestas personalizadas según datos históricos o en vivo
- ⚠️ Alertas automáticas vía chat ante eventos críticos
- 🐳 Desplegable con **Docker** para fácil configuración
- 🔐 Variables de entorno para mantener datos sensibles seguros

---

## 🧰 Tecnologías utilizadas

| Tecnología         | Rol                           |
|--------------------|-------------------------------|
| Python             | Lógica del bot y consultas    |
| Google BigQuery    | Origen de datos               |
| WhatsApp Cloud API | Canal de comunicación         |
| Pandas             | Procesamiento de datos        |
| Docker             | Contenerización del entorno   |
| Flask / Webhooks   | Recepción de mensajes         |

---

## ⚙️ Instalación rápida

```bash
git clone https://github.com/JuanQuintero77/Chatbot.git
cd Chatbot
```

1. Crea un archivo `.env` y agrega tus credenciales:
```env
WHATSAPP_TOKEN=tu_token
WHATSAPP_PHONE_NUMBER_ID=tu_id
GCP_PROJECT_ID=tu_proyecto
BIGQUERY_DATASET=tu_dataset
BIGQUERY_TABLE=tu_tabla
```

2. Construye y corre el contenedor:
```bash
docker build -t chatbot .
docker run --env-file .env -p 5000:5000 chatbot
```

---

## 💬 Ejemplo de flujo

**Usuario:** "¿Qué disponibilidad hay del producto XYZ?"  
**Chatbot:** "Producto XYZ tiene 20 unidades disponibles en el almacén central."

---

## 🧪 Ideas de expansión

- Conexión con múltiples fuentes de datos (Google Sheets, APIs REST)
- Soporte para imágenes o documentos en la respuesta
- Dashboard web para monitoreo
- Análisis de sentimiento o clasificación de mensajes con IA

---

## 🙋‍♂️ Autor

**Juan Guillermo Quintero Díaz**  
Data Engineer & Python Developer  
📍 Colombia  
🔗 [GitHub](https://github.com/JuanQuintero77)

---

## 📄 Licencia

MIT License - Libre uso con atribución

---

## ⭐ ¿Te fue útil?

Si este proyecto te sirvió de inspiración o ayuda, dejá una ⭐ en el repositorio. ¡Gracias!
