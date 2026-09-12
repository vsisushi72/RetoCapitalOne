import requests

# API Key de pruebas de Nessie (Capital One)
API_KEY = "TU_API_KEY_AQUI" 
BASE_URL = "http://api.nessieisreal.com"

def obtener_saldo_cuenta(account_id: str) -> float:
    """Obtiene el saldo disponible de un cliente."""
    url = f"{BASE_URL}/accounts/{account_id}?key={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("balance", 0.0)
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
    return 0.0

def obtener_historial_transacciones(account_id: str) -> list:
    """Consulta el historial de transferencias recientes del usuario."""
    url = f"{BASE_URL}/accounts/{account_id}/transfers?key={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error al obtener historial: {e}")
    return []

def ejecutar_transferencia(account_id_origen: str, account_id_destino: str, monto: float, concepto: str) -> dict:
    """Envía la petición para realizar la transferencia bancaria."""
    url = f"{BASE_URL}/accounts/{account_id_origen}/transfers?key={API_KEY}"
    payload = {
        "medium": "balance",
        "payee_id": account_id_destino,
        "amount": monto,
        "transaction_date": "2026-09-12",
        "description": concepto
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}