from flask import Blueprint, request, jsonify
from app.services.whatsapp_utils import enviar_respuesta_con_botones, enviar_respuesta_whatsapp


import os

# Crear el Blueprint
whatsapp_bp = Blueprint('whatsapp', __name__)

# Inicializar dependencias globales
bigquery_utils = None
user_state = None

def init_dependencies(bq_utils, u_state):
    global bigquery_utils, user_state
    bigquery_utils = bq_utils
    user_state = u_state


# Método GET
@whatsapp_bp.route('', methods=['GET'])
def whatsapp_verificacion():
    token = os.getenv("VERIFY_TOKEN", "12345")  # Token por defecto si no está configurado

    # Recupera los parámetros enviados por Meta
    mode = request.args.get('hub.mode')
    challenge = request.args.get('hub.challenge')
    verify_token = request.args.get('hub.verify_token')

    # Verifica el token y el modo
    if mode == "subscribe" and verify_token == token:
        return challenge, 200  # Retorna el desafío para completar la verificación
    return "Error: Token inválido", 403  # Responde con error si no es válido

#Método Post
@whatsapp_bp.route('', methods=['POST'])
def whatsapp_webhook():
    try:
        data = request.get_json()
        print(data)  # Imprime los datos recibidos para depuración

        # Validar la estructura básica del JSON
        if not data or 'entry' not in data or not data['entry']:
            print("Estructura del JSON inválida o vacía.")
            return jsonify({"status": "ignored"}), 400

        # Validar si la entrada es un evento de 'statuses'
        changes = data['entry'][0].get('changes', [])
        value = changes[0].get('value', {}) if changes else {}
        statuses = value.get('statuses', [])
        if statuses:
            # Evento de estado (mensaje enviado, entregado, leído)
            for status in statuses:
                print(f"Estado del mensaje: {status['status']} - ID: {status['id']}")
            return jsonify({"status": "status_event_handled"}), 200

        # Validar si hay mensajes en los cambios
        messages = value.get('messages', [])
        if not messages:
            print("No se encontraron mensajes en la entrada.")
            return jsonify({"status": "ignored"}), 400

        # Validar si el mensaje contiene el campo 'from'
        message = messages[0]
        sender = message.get('from')
        if not sender:
            print("El mensaje no contiene el campo 'from'.")
            return jsonify({"status": "ignored"}), 400

        # Verificar si el mensaje contiene una respuesta interactiva
        if "interactive" in message:
            interactive_data = message["interactive"]
            if "button_reply" in interactive_data:
                button_id = interactive_data["button_reply"]["id"]

                estado = user_state.obtener_estado(sender)

                # Menú principal
                if estado == "menu":
                    if button_id == "consultar_kpis":
                        print(f"Estado antes del botón: {user_state.obtener_estado(sender)}")
                        user_state.actualizar_estado(sender, "listar_campanas_kpi")
                        print(f"Estado después del botón: {user_state.obtener_estado(sender)}")
                        campanas = bigquery_utils.obtener_campanas_kpi()
                        botones = [{"type": "reply", "reply": {"id": f"campana_kpi_{i}", "title": camp[:20]}} for i, camp in enumerate(campanas)]
                        enviar_respuesta_con_botones(sender, "Selecciona una campaña:", botones)
                    elif button_id == "consultar_alertas":
                        user_state.actualizar_estado(sender, "listar_campanas_alertas")
                        campanas = bigquery_utils.obtener_campanas_alertas()
                        botones = [{"type": "reply", "reply": {"id": f"campana_alerta_{i}", "title": camp[:20]}} for i, camp in enumerate(campanas)]
                        enviar_respuesta_con_botones(sender, "Selecciona una campaña:", botones)
                    elif button_id == "salir":
                        user_state.actualizar_estado(sender, "menu")
                        enviar_respuesta_whatsapp(sender, "Gracias por usar el asistente. ¡Hasta pronto!")
                        return jsonify({"status": "success"}), 200

                # Flujo de campañas para KPIs
                elif estado.startswith("listar_campanas_kpi"):
                    if button_id.startswith("campana_kpi_"):
                        campana_id = int(button_id.split("_")[-1])
                        campanas = bigquery_utils.obtener_campanas_kpi()
                        campana_seleccionada = campanas[campana_id]
                        print(f"Estado antes del botón: {user_state.obtener_estado(sender)}")
                        user_state.actualizar_estado(sender, f"listar_reportes_kpi:{campana_seleccionada}")
                        print(f"Estado después del botón: {user_state.obtener_estado(sender)}")
                        reportes = bigquery_utils.obtener_reportes_kpi(campana_seleccionada)
                        botones = [{"type": "reply", "reply": {"id": f"reporte_kpi_{i}", "title": rep[:20]}} for i, rep in enumerate(reportes)]
                        enviar_respuesta_con_botones(sender, f"Seleccionaste la campaña: {campana_seleccionada}. Selecciona un reporte:", botones)
                    return jsonify({"status": "success"}), 200

                elif estado.startswith("listar_reportes_kpi"):
                    campana_seleccionada = estado.split(":")[1]
                    reportes = bigquery_utils.obtener_reportes_kpi(campana_seleccionada)
                    if button_id.startswith("reporte_kpi_"):
                        reporte_id = int(button_id.split("_")[-1])
                        reporte_seleccionado = reportes[reporte_id]
                        user_state.actualizar_estado(sender, "menu")
                        kpis = bigquery_utils.obtener_kpis(reporte_seleccionado)
                        if kpis:
                            respuesta = f"Seleccionaste el reporte: {reporte_seleccionado}.\nEstos son los KPIs disponibles:\n" + "\n".join(f"- {kpi}" for kpi in kpis)
                        else:
                            respuesta = f"No se encontraron KPIs para el reporte: {reporte_seleccionado}."
                        respuesta += "\nEscribe 'menu' para regresar al menú principal."
                        enviar_respuesta_whatsapp(sender, respuesta)
                    return jsonify({"status": "success"}), 200

                # Flujo de campañas para Alertas
                elif estado.startswith("listar_campanas_alertas"):
                    if button_id.startswith("campana_alerta_"):
                        campana_id = int(button_id.split("_")[-1])
                        campanas = bigquery_utils.obtener_campanas_alertas()
                        campana_seleccionada = campanas[campana_id]
                        user_state.actualizar_estado(sender, f"listar_reportes_alertas:{campana_seleccionada}")
                        reportes = bigquery_utils.obtener_reportes_alertas(campana_seleccionada)
                        botones = [{"type": "reply", "reply": {"id": f"reporte_alerta_{i}", "title": rep[:20]}} for i, rep in enumerate(reportes)]
                        enviar_respuesta_con_botones(sender, f"Seleccionaste la campaña: {campana_seleccionada}. Selecciona un reporte:", botones)
                    return jsonify({"status": "success"}), 200

                elif estado.startswith("listar_reportes_alertas"):
                    campana_seleccionada = estado.split(":")[1]
                    reportes = bigquery_utils.obtener_reportes_alertas(campana_seleccionada)
                    if button_id.startswith("reporte_alerta_"):
                        reporte_id = int(button_id.split("_")[-1])
                        reporte_seleccionado = reportes[reporte_id]
                        user_state.actualizar_estado(sender, "menu")
                        alertas = bigquery_utils.obtener_alertas(reporte_seleccionado)
                        if alertas:
                            respuesta = f"Seleccionaste el reporte: {reporte_seleccionado}.\nEstas son las alertas disponibles:\n" + "\n".join(f"- {alerta}" for alerta in alertas)
                        else:
                            respuesta = f"No se encontraron alertas para el reporte: {reporte_seleccionado}."
                        respuesta += "\nEscribe 'menu' para regresar al menú principal."
                        enviar_respuesta_whatsapp(sender, respuesta)
                    return jsonify({"status": "success"}), 200

        # Mensaje de bienvenida
        estado = user_state.obtener_estado(sender)
        if not estado or estado == "menu":
            enviar_respuesta_con_botones(sender, "Hola, soy tu asistente virtual, elige una opción:", [
                {"type": "reply", "reply": {"id": "consultar_kpis", "title": "Consultar KPIs"}},
                {"type": "reply", "reply": {"id": "consultar_alertas", "title": "Consultar Alertas"}},
                {"type": "reply", "reply": {"id": "salir", "title": "Salir"}}
            ])
            return jsonify({"status": "success"}), 200

        print("El webhook no pudo manejar este mensaje.")
        return jsonify({"status": "unhandled"}), 200

    except Exception as e:
        print(f"Error en webhook: {str(e)}")
        return jsonify({"status": "error", "error": str(e)}), 500


@whatsapp_bp.route('/enviar_alertas', methods=['POST'])
def enviar_alertas_periodicas():
    try:
        # Confirmar que bigquery_utils está inicializado
        if not bigquery_utils:
            raise ValueError("bigquery_utils no está inicializado")

        alertas = bigquery_utils.obtener_alertas_pendientes()
        print(f"Alertas pendientes: {alertas}")
        if not alertas:
            print("No hay alertas nuevas para enviar.")
            return jsonify({"status": "success", "message": "No hay alertas nuevas"}), 200

        ids_alertas_enviadas = []
        for alerta in alertas:
            try:
                Fecha_alerta = alerta["Fecha_alerta"]
                fecha_formateada = Fecha_alerta.replace(microsecond=0).strftime("%d/%m/%Y %H:%M:%S")
                Valor_indicador = alerta["Valor_Indicador"]
                Valor_indicador_formateado = Valor_indicador * 100
            except ValueError as ve:
                print(f"Error al formatear la fecha, error: {ve}")
            enviar_respuesta_whatsapp("573113967072", f"🚨 Alerta: {alerta['Mensaje_Alerta']} \n"
                                                     f"Campaña: {alerta['Campana']}\n"
                                                     f"Reporte: {alerta['Reporte']}\n"
                                                     f"Indicador: {alerta['Nombre_indicador']}\n"
                                                     f"Valor: {Valor_indicador_formateado}\n"
                                                     f"Fecha: {fecha_formateada}")
            ids_alertas_enviadas.append(alerta["Id_alerta"])

        # Actualizar estado de alertas
        bigquery_utils.actualizar_estado_alertas(ids_alertas_enviadas)
        print(f"Estados actualizados para alertas: {ids_alertas_enviadas}")
        return jsonify({"status": "success", "message": f"Se enviaron {len(ids_alertas_enviadas)} alertas"}), 200
    except Exception as e:
        print(f"Error al enviar alertas: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500