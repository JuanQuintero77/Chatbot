from google.cloud import bigquery
import os

class BigQueryUtils:
    def __init__(self, credentials_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = bigquery.Client()

    def ejecutar_consulta(self, sql, parametros=None):
        try:
            job_config = bigquery.QueryJobConfig(query_parameters=parametros or [])
            query_job = self.client.query(sql, job_config=job_config)
            return [fila for fila in query_job]
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

    # Métodos para KPIs
    def obtener_campanas_kpi(self):
        sql = "SELECT DISTINCT Campana FROM `chatbot442216.Prueba.TB_Pruebas_Kpi`"
        resultados = self.ejecutar_consulta(sql)
        return [fila.Campana for fila in resultados]

    def obtener_reportes_kpi(self, campana):
        sql = "SELECT DISTINCT Reporte FROM `chatbot442216.Prueba.TB_Pruebas_Kpi` WHERE Campana = @campana"
        parametros = [bigquery.ScalarQueryParameter("campana", "STRING", campana)]
        resultados = self.ejecutar_consulta(sql, parametros)
        return [fila.Reporte for fila in resultados]

    def obtener_kpis(self, reporte):
        sql = """
        SELECT 
            `Nombre_indicador`,
            SAFE_CAST(Valor_indicador AS FLOAT64) * 100 AS Valor_Indicador,
             PARSE_DATETIME('%Y-%m-%d %H:%M:%S', SUBSTR(Fecha_Hora, 1, 19)) AS Fecha
        FROM `chatbot442216.Prueba.TB_Pruebas_Kpi`
        WHERE Reporte = @reporte
        """
        parametros = [bigquery.ScalarQueryParameter("reporte", "STRING", reporte)]
        resultados = self.ejecutar_consulta(sql, parametros)

        return [
            f"{fila.Nombre_indicador}: {fila.Valor_Indicador:.2f}% (Fecha: {fila.Fecha})"
            for fila in resultados
        ]

    # Métodos para Alertas
    def obtener_campanas_alertas(self):
        sql = "SELECT DISTINCT Campana FROM `chatbot442216.Prueba.TB_Pruebas_Alertas`"
        resultados = self.ejecutar_consulta(sql)
        return [fila.Campana for fila in resultados]

    def obtener_reportes_alertas(self, campana):  # Añadir self como primer argumento
        sql = "SELECT DISTINCT Reporte FROM `chatbot442216.Prueba.TB_Pruebas_Alertas` WHERE Campana = @campana"
        parametros = [bigquery.ScalarQueryParameter("campana", "STRING", campana)]
        resultados = self.ejecutar_consulta(sql, parametros)  # Cambiar a self.ejecutar_consulta
        return [fila.Reporte for fila in resultados]

    def obtener_alertas(self, reporte):
        sql = """
        SELECT 
            `Indicador`,
            SAFE_CAST(Valor_indicador AS FLOAT64) * 100 AS Valor_indicador,
            Tipo_alerta,
             PARSE_DATETIME('%Y-%m-%d %H:%M:%S', SUBSTR(Fecha_Hora, 1, 19)) AS Fecha
        FROM `chatbot442216.Prueba.TB_Pruebas_Alertas`
        WHERE Reporte = @reporte
        """
        parametros = [bigquery.ScalarQueryParameter("reporte", "STRING", reporte)]
        resultados = self.ejecutar_consulta(sql, parametros)

        return [
            f"{fila.Indicador}: {fila.Valor_indicador:.2f}% - {fila.Tipo_alerta} (Fecha: {fila.Fecha})"
            for fila in resultados
        ]

    def obtener_alertas_pendientes(self):
        sql = """
        SELECT 
          Id_alerta,
          Fecha_alerta,
          Campana,
          Reporte,
          Nombre_indicador,
          Valor_Indicador,
          Mensaje_Alerta
        FROM 
          `chatbot442216.Prueba.TB_Alertas_historico`
        WHERE 
          Estado = 'No enviado'
        """
        return self.ejecutar_consulta(sql)

    def actualizar_estado_alertas(self, ids_alertas):
        sql = """
        UPDATE `chatbot442216.Prueba.TB_Alertas_historico`
        SET Estado = 'Enviado'
        WHERE Id_alerta IN UNNEST(@ids)
        """
        parametros = [bigquery.ArrayQueryParameter("ids", "STRING", ids_alertas)]
        self.ejecutar_consulta(sql, parametros)


