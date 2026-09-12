import os
import requests

API_KEY = os.environ.get("NESSIE_API_KEY", "")
BASE_URL = "http://api.nessieisreal.com"

def obtener_saldo_cuenta(account_id: str) -> float:
    """Obtiene el saldo disponible. Si falla la API, regresa un saldo simulado estable."""
    url = f"{BASE_URL}/accounts/{account_id}?key={API_KEY}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.json().get("balance", 15450.00)
    except Exception as e:
        print(f"Modo Respaldo Activo (Saldo): {e}")
    
    # Saldo de respaldo para la demo
    return 15450.00

def obtener_historial_transacciones(account_id: str) -> list:
    """Consulta transferencias previas. Si falla la API, regresa historial simulado."""
    url = f"{BASE_URL}/accounts/{account_id}/transfers?key={API_KEY}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Modo Respaldo Activo (Historial): {e}")
    
    # Historial de respaldo para la demo
    return [
        {"amount": 200.0, "description": "Pago de luz", "payee_id": "987654321"},
        {"amount": 150.0, "description": "Supermercado", "payee_id": "111222333"}
    ]

def ejecutar_transferencia(account_id_origen: str, account_id_destino: str, monto: float, concepto: str) -> dict:
    """Envía la transacción a la API de Capital One o la simula si la red falla."""
    url = f"{BASE_URL}/accounts/{account_id_origen}/transfers?key={API_KEY}"
    payload = {
        "medium": "balance",
        "payee_id": account_id_destino,
        "amount": monto,
        "transaction_date": "2026-09-12",
        "description": concepto
    }
    try:
        response = requests.post(url, json=payload, timeout=3)
        if response.status_code in [200, 201]:
            return response.json()
    except Exception as e:
        print(f"Modo Respaldo Activo (Transferencia): {e}")
    
    # Respuesta exitosa de respaldo para la demo
    return {"code": 201, "message": "Transferencia procesada correctamente (Simulado)"}