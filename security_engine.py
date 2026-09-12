import re

LIMITE_MONTO_MAXIMO = 5000.0
LIMITE_DESTINATARIO_NUEVO = 500.0
PALABRAS_SENSIBLES = ["nip", "password", "contraseña", "cvv", "clave", "pin"]

def redactar_concepto(concepto: str) -> str:
    concepto_redactado = concepto
    for palabra in PALABRAS_SENSIBLES:
        patron = re.compile(re.escape(palabra), re.IGNORECASE)
        concepto_redactado = patron.sub("[DATO OCULTADO]", concepto_redactado)
    return concepto_redactado

def evaluar_riesgo_transaccion(monto: float, concepto: str, historial_transacciones: list, cuenta_destino: str = "") -> dict:
    alertas = []
    nivel_riesgo = "BAJO"

    if monto > LIMITE_MONTO_MAXIMO:
        alertas.append(f"El monto (${monto:,.2f}) supera el límite seguro configurado (${LIMITE_MONTO_MAXIMO:,.2f}).")
        nivel_riesgo = "ALTO"

    concepto_lower = concepto.lower()
    if any(palabra in concepto_lower for palabra in PALABRAS_SENSIBLES):
        alertas.append("Se detectó información confidencial en el concepto. Nunca comparta su NIP o contraseña en un pago.")
        nivel_riesgo = "ALTO"

    if len(historial_transacciones) >= 2:
        ultimas_transacciones = historial_transacciones[-2:]
        if all(t.get("amount", 0) > 1000 for t in ultimas_transacciones):
            alertas.append("Frecuencia inusual de transferencias altas consecutivas.")
            if nivel_riesgo != "ALTO":
                nivel_riesgo = "MEDIO"

    cuentas_conocidas = {t.get("payee_id") for t in historial_transacciones if t.get("payee_id")}
    if cuenta_destino and cuenta_destino not in cuentas_conocidas and monto > LIMITE_DESTINATARIO_NUEVO:
        alertas.append("Este destinatario no aparece en sus pagos anteriores. Confirme con un familiar de confianza antes de continuar.")
        if nivel_riesgo != "ALTO":
            nivel_riesgo = "MEDIO"

    return {
        "aprobado_automatico": nivel_riesgo == "BAJO",
        "nivel_riesgo": nivel_riesgo,
        "alertas": alertas,
        "mensaje_usuario": "Transacción segura." if nivel_riesgo == "BAJO" else "Atención: Esta transacción requiere autorización.",
        "concepto_seguro": redactar_concepto(concepto)
    }