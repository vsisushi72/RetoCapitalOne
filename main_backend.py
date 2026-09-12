from security_engine import evaluar_riesgo_transaccion
from nessie_client import obtener_historial_transacciones, ejecutar_transferencia

def procesar_transaccion_segura(account_id_origen: str, account_id_destino: str, monto: float, concepto: str, autorizacion_familiar: bool = False) -> dict:
    """
    Orquesta el flujo principal:
    1. Consulta historial en Capital One.
    2. Evalúa riesgos y anomalías.
    3. Si es segura o está autorizada por un contacto de confianza, ejecuta el pago.
    4. Si hay riesgo, detiene la operación y envía las alertas a la interfaz.
    """
    # 1. Obtener historial previo para análisis de comportamiento
    historial = obtener_historial_transacciones(account_id_origen)

    # 2. Analizar riesgos con el motor de seguridad
    evaluacion_riesgo = evaluar_riesgo_transaccion(monto, concepto, historial)

    # 3. Decidir si se procesa o se bloquea
    if evaluacion_riesgo["aprobado_automatico"] or autorizacion_familiar:
        # Petición a la API de Capital One
        resultado_api = ejecutar_transferencia(account_id_origen, account_id_destino, monto, concepto)
        return {
            "estatus": "EXITO",
            "mensaje": "Transacción realizada con éxito.",
            "detalles_api": resultado_api,
            "evaluacion_riesgo": evaluacion_riesgo
        }
    else:
        # Bloqueo preventivo para proteger al adulto mayor
        return {
            "estatus": "BLOQUEADO_POR_SEGURIDAD",
            "mensaje": evaluacion_riesgo["mensaje_usuario"],
            "alertas": evaluacion_riesgo["alertas"],
            "nivel_riesgo": evaluacion_riesgo["nivel_riesgo"],
            "requiere_confirmacion_contacto_confianza": True
        }

# Prueba de ejecución en consola local
if __name__ == "__main__":
    print("--- PRUEBA 1: Transacción Normal (Segura) ---")
    res1 = procesar_transaccion_segura("CUENTA_ORIGEN_123", "DESTINO_456", 200.0, "Pago de despensa")
    print(res1)

    print("\n--- PRUEBA 2: Transacción con Alerta de Seguridad (Monto alto + NIP) ---")
    res2 = procesar_transaccion_segura("CUENTA_ORIGEN_123", "DESTINO_456", 7000.0, "Transferencia NIP 1234")
    print(res2)