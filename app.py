import streamlit as st
from main_backend import procesar_transaccion_segura
from nessie_client import obtener_saldo_cuenta

# 1. Configuración de página
st.set_page_config(page_title="Guardián Senior - Capital One", page_icon="🛡️", layout="centered")

# 2. Estilos CSS Personalizados (Estilo Corporate Memphis / Accesibilidad Senior)
st.markdown("""
    <style>
    /* Fondo principal en tono pastel suave */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Encabezado principal estilo tarjeta pastel */
    .header-card {
        background: linear-gradient(135deg, #6C5CE7 0%, #a29bfe 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.2);
        margin-bottom: 25px;
    }
    
    /* Tarjeta de Saldo */
    .balance-card {
        background-color: #E3FCF7;
        border: 2px solid #00B894;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Botones grandes y accesibles estilo Memphis */
    .stButton>button {
        width: 100%;
        background-color: #6C5CE7;
        color: white;
        font-size: 20px !important;
        font-weight: bold;
        padding: 16px 24px;
        border-radius: 14px;
        border: none;
        box-shadow: 0 6px 0px #4B38B3;
        transition: all 0.1s ease;
    }
    .stButton>button:hover {
        background-color: #5A4AD1;
        transform: translateY(2px);
        box-shadow: 0 4px 0px #4B38B3;
    }
    
    /* Tarjetas de Alerta de Seguridad */
    .warning-card {
        background-color: #FFEAA7;
        border-left: 8px solid #FDCB6E;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
    }
    .danger-card {
        background-color: #FFD8D8;
        border-left: 8px solid #FF7675;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado principal
st.markdown("""
    <div class="header-card">
        <h1 style='margin:0; font-size: 32px;'>🛡️ Guardián Financiero Senior</h1>
        <p style='margin:5px 0 0 0; font-size: 18px;'>Su asistente personal para transacciones seguras y autónomas</p>
    </div>
""", unsafe_allow_html=True)

# 4. Navegación por Pestañas principales
tab_transferir, tab_mi_escudo, tab_aprender = st.tabs([
    "💸 Hacer una Transferencia", 
    "🛡️ Mi Escudo Activo", 
    "💡 Guía Anti-Estafas"
])

# --- PESTAÑA 1: TRANSFERENCIAS AUTÓNOMAS ---
with tab_transferir:
    # Consulta de saldo desde la API de Nessie
    saldo_actual = obtener_saldo_cuenta("CUENTA_ROBERTO_123")
    
    st.markdown(f"""
        <div class="balance-card">
            <span style='font-size: 18px; color: #2D3436;'>Dinero Disponible en su Cuenta:</span>
            <h2 style='margin:5px 0 0 0; font-size: 38px; color: #008767;'>${saldo_actual:,.2f} MXN</h2>
        </div>
    """, unsafe_allow_html=True)

    st.write("### Complete los datos para enviar dinero:")
    
    cuenta_destino = st.text_input("1. ¿A quién le desea enviar dinero? (Número de cuenta o teléfono):", value="987654321")
    monto = st.number_input("2. ¿Cuánto dinero desea enviar? ($):", min_value=1.0, value=500.0, step=100.0)
    concepto = st.text_input("3. Motivo de la transferencia (Ej. Despensa, Servicio):", value="Pago de luz")

    st.write("")
    if st.button("ENVIAR DINERO AHORA"):
        cuenta_origen = "CUENTA_ROBERTO_123"
        resultado = procesar_transaccion_segura(cuenta_origen, cuenta_destino, monto, concepto)
        
        st.markdown("---")
        
        if resultado["estatus"] == "EXITO":
            st.balloons()
            st.success("✅ **¡Operación Exitosa!** El dinero ha sido enviado de forma segura.")
        else:
            # Explicación clara sin necesidad de llamar a un hijo
            st.markdown("""
                <div class="danger-card">
                    <h2 style='color: #D63031; margin-top:0;'>⚠️ Transacción Detenida Preventivamente</h2>
                    <p style='font-size: 18px; color: #2D3436;'>
                        Hemos pausado este envío para proteger su dinero. No se ha realizado ningún cobro.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("#### Razones detectadas por su Guardián:")
            for alerta in resultado["alertas"]:
                st.warning(f"👉 **{alerta}**")
                
            st.info("💡 **Recomendación Autónoma:** Si no conoce a la persona o alguien le pidió este dinero por teléfono de forma urgente, vuelva a verificar antes de intentar nuevamente.")

# --- PESTAÑA 2: ESCUDO DE SEGURIDAD EN TIEMPO REAL ---
with tab_mi_escudo:
    st.write("### Reglas de Protección Activas")
    st.write("Su Guardián trabaja automáticamente en segundo plano evaluando cada operación en la Nessie API:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="warning-card">
                <h4>🔒 Límite Inteligente</h4>
                <p>Alertar automáticamente en operaciones mayores a <b>$5,000.00 MXN</b>.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="warning-card">
                <h4>👁️ Filtro Anti-Fuga</h4>
                <p>Bloqueo de envíos que incluyan textos como <b>NIP, Clave o Contraseña</b>.</p>
            </div>
        """, unsafe_allow_html=True)

# --- PESTAÑA 3: EDUCACIÓN Y PREVENCIÓN ---
with tab_aprender:
    st.write("### Consejos para evitar estafas telefónicas")
    st.write("Aprenda a identificar engaños comunes antes de realizar cualquier movimiento:")
    
    with st.expander("🚨 Si le llaman diciendo que ganaron un premio"):
        st.write("Nunca envíe dinero para 'reclamar' un premio. Los bancos o concursos legítimos jamás le pedirán un depósito previo.")
    
    with st.expander("📞 Llamadas urgentes de supuestos familiares"):
        st.write("Si alguien llama diciendo que un familiar tuvo un accidente, cuelgue inmediatamente y llame directamente a su familiar a su número personal.")