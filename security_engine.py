import re

LIMITE_MONTO_MAXIMO = 5000.0
PALABRAS_SENSIBLES = ["nip", "password", "contraseña", "cvv", "clave", "pin"]

def evaluar_riesgo_transaccion(monto: float, concepto: str, historial_transacciones: list) -> dict:
    """
    Evalúa si la transacción presenta riesgos o fugas de datos antes de enviarla a la API.
    """
    alertas = []
    nivel_riesgo = "BAJO"

    # Regla 1: Control de Monto
    if monto > LIMITE_MONTO_MAXIMO:
        alertas.append(f"El monto (${monto}) supera el límite seguro configurado (${LIMITE_MONTO_MAXIMO}).")
        nivel_riesgo = "ALTO"

    # Regla 2: Detección de Datos Sensibles en la descripción
    concepto_lower = concepto.lower()
    for palabra in PALABRAS_SENSIBLES:
        if palabra in concepto_lower:
            alertas.append(f"Se detectó información confidencial ('{palabra}') en el concepto.")
            nivel_riesgo = "ALTO"

    # Regla 3: Frecuencia de transacciones consecutivas
    if len(historial_transacciones) >= 2:
        ultimas_transacciones = historial_transacciones[-2:]
        if all(t.get("amount", 0) > 1000 for t in ultimas_transacciones):
            alertas.append("Frecuencia inusual de transferencias altas consecutivas.")
            if nivel_riesgo != "ALTO":
                nivel_riesgo = "MEDIO"

    return {
        "aprobado_automatico": nivel_riesgo == "BAJO",
        "nivel_riesgo": nivel_riesgo,
        "alertas": alertas,
        "mensaje_usuario": "Transacción segura." if nivel_riesgo == "BAJO" else "Atención: Esta transacción requiere autorización."
    }