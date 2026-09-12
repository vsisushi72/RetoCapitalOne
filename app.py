import streamlit as st
from datetime import datetime
from main_backend import procesar_transaccion_segura
from nessie_client import obtener_saldo_cuenta, obtener_historial_transacciones
 
MODO_DEMO_JUECES = True
 
def obtener_saludo() -> str:
    hora = datetime.now().hour
    if hora < 12:
        return "Buenos dias"
    elif hora < 19:
        return "Buenas tardes"
    return "Buenas noches"
 
if "fraudes_bloqueados" not in st.session_state:
    st.session_state["fraudes_bloqueados"] = 12 if MODO_DEMO_JUECES else 0
if "dinero_protegido" not in st.session_state:
    st.session_state["dinero_protegido"] = 45230.0 if MODO_DEMO_JUECES else 0.0
if "texto_grande" not in st.session_state:
    st.session_state["texto_grande"] = False
 
st.set_page_config(page_title="Guardian Financiero Senior", layout="wide")
 
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }
 
    p, span, label, h1, h2, h3, h4, h5, h6, div {
        color: #0F172A !important;
    }
 
    section[data-testid="stSidebar"] {
        background-color: #EEF2FF !important;
        border-right: 2px solid #C7D2FE !important;
    }
 
    .card-panel {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important;
    }
 
    .header-panel {
        background-color: #4338CA !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 24px !important;
    }
    .header-panel h1 {
        color: #FFFFFF !important;
        margin: 0 !important;
        font-size: 30px !important;
        font-weight: 800 !important;
    }
    .header-panel p {
        color: #E0E7FF !important;
        margin: 6px 0 0 0 !important;
        font-size: 16px !important;
    }
 
    .balance-box {
        background-color: #ECFDF5 !important;
        border: 2px solid #10B981 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        text-align: center !important;
        margin-bottom: 20px !important;
    }
    .balance-box span {
        color: #065F46 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    .balance-box h2 {
        color: #047857 !important;
        font-size: 38px !important;
        margin: 6px 0 0 0 !important;
        font-weight: 800 !important;
    }
 
    .alert-danger {
        background-color: #FEF2F2 !important;
        border: 2px solid #EF4444 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        margin-top: 16px !important;
    }
    .alert-danger h3 {
        color: #991B1B !important;
        margin: 0 0 6px 0 !important;
    }
    .alert-danger p {
        color: #7F1D1D !important;
        margin: 0 !important;
    }
 
    .alert-success {
        background-color: #F0FDF4 !important;
        border: 2px solid #22C55E !important;
        border-radius: 12px !important;
        padding: 18px !important;
        margin-top: 16px !important;
    }
    .alert-success h3 {
        color: #166534 !important;
        margin: 0 !important;
    }
 
    .info-card {
        background-color: #FEF3C7 !important;
        border: 2px solid #F59E0B !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
    }
 
    .stTextInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        padding: 10px !important;
    }
 
    .stButton button {
        background-color: #4338CA !important;
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 6px rgba(67, 56, 202, 0.2) !important;
    }
    .stButton button:hover {
        background-color: #3730A3 !important;
        color: #FFFFFF !important;
    }
 
    button[data-baseweb="tab"] {
        background-color: #E2E8F0 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 12px 20px !important;
    }
    button[aria-selected="true"] {
        background-color: #4338CA !important;
    }
    button[aria-selected="true"] p {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
 
    .metric-box {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important;
    }
    .metric-box span {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #475569 !important;
    }
    .metric-box h2 {
        font-size: 30px !important;
        margin: 6px 0 0 0 !important;
        font-weight: 800 !important;
    }
    .metric-saldo h2 { color: #4338CA !important; }
    .metric-bloqueos h2 { color: #DC2626 !important; }
    .metric-protegido h2 { color: #047857 !important; }
 
    .assistant-box {
        background-color: #EEF2FF !important;
        border: 2px solid #4338CA !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        margin-bottom: 20px !important;
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
    }
    .assistant-avatar {
        font-size: 40px !important;
        line-height: 1 !important;
    }
    .assistant-box b {
        color: #3730A3 !important;
        font-size: 16px !important;
    }
    .assistant-box p {
        margin: 4px 0 0 0 !important;
        font-size: 16px !important;
        color: #1E1B4B !important;
    }
 
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important;
    }
    div[data-testid="stExpander"] * {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    </style>
""", unsafe_allow_html=True)
 
if st.session_state["texto_grande"]:
    st.markdown("""
        <style>
        html, body, .stApp, p, span, label, li, div {
            font-size: 20px !important;
        }
        h1 { font-size: 40px !important; }
        h2 { font-size: 34px !important; }
        h3 { font-size: 26px !important; }
        .stButton button {
            font-size: 22px !important;
            padding: 16px 24px !important;
        }
        .stTextInput input, .stNumberInput input {
            font-size: 22px !important;
            padding: 14px !important;
        }
        html, body, .stApp {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        p, span, label, h1, h2, h3, h4, h5, h6, div {
            color: #000000 !important;
        }
        .card-panel, .metric-box, .assistant-box {
            border-width: 3px !important;
        }
        </style>
    """, unsafe_allow_html=True)
 
with st.sidebar:
    st.markdown("""
        <div class="card-panel">
            <h3 style="margin:0 0 10px 0;">Mi Cuenta</h3>
            <p><b>Nombre:</b> Roberto Gómez</p>
            <p><b>Edad:</b> 68 años</p>
            <p><b>Tipo de cuenta:</b> Cuenta Senior</p>
            <hr>
            <p>✅ Tu cuenta está siendo protegida en tiempo real</p>
        </div>
    """, unsafe_allow_html=True)
 
    st.session_state["texto_grande"] = st.checkbox(
        "Texto grande y alto contraste",
        value=st.session_state["texto_grande"]
    )
 
st.markdown("""
    <div class="header-panel">
        <h1>Guardian Financiero Senior</h1>
        <p>Plataforma de transacciones protegidas con deteccion de riesgo en tiempo real</p>
    </div>
""", unsafe_allow_html=True)
 
st.markdown(f"""
    <div class="assistant-box">
        <div class="assistant-avatar">👩‍💼</div>
        <div>
            <b>Ana, tu asesora de seguridad</b>
            <p>{obtener_saludo()}, Roberto. Estoy revisando cada movimiento contigo, no estas solo en esto.</p>
        </div>
    </div>
""", unsafe_allow_html=True)
 
saldo_dashboard = obtener_saldo_cuenta("CUENTA_ROBERTO_123")
col_m1, col_m2, col_m3 = st.columns(3)
 
with col_m1:
    st.markdown(f"""
        <div class="metric-box metric-saldo">
            <span>Saldo disponible</span>
            <h2>${saldo_dashboard:,.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
 
with col_m2:
    st.markdown(f"""
        <div class="metric-box metric-bloqueos">
            <span>Intentos de fraude bloqueados este mes</span>
            <h2>{st.session_state['fraudes_bloqueados']}</h2>
        </div>
    """, unsafe_allow_html=True)
 
with col_m3:
    st.markdown(f"""
        <div class="metric-box metric-protegido">
            <span>Dinero total protegido</span>
            <h2>${st.session_state['dinero_protegido']:,.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
 
st.write("")
 
tab_operacion, tab_bitacora, tab_reglas = st.tabs([
    "Realizar Transferencia",
    "Bitacora de Actividad",
    "Configuracion de Seguridad"
])
 
with tab_operacion:
    col_left, col_right = st.columns([2, 1])
 
    with col_left:
        st.markdown(f"""
            <div class="balance-box">
                <span>Saldo disponible en cuenta corriente:</span>
                <h2>${saldo_dashboard:,.2f} MXN</h2>
            </div>
        """, unsafe_allow_html=True)
 
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        st.subheader("Datos de la transferencia")
 
        cuenta_destino = st.text_input("Numero de cuenta o telefono de destino", value=st.session_state.get("cuenta_test", "987654321"))
        monto = st.number_input("Monto a enviar (MXN)", min_value=1.0, value=float(st.session_state.get("monto_test", 350.0)), step=50.0)
        concepto = st.text_input("Concepto o motivo del pago", value=st.session_state.get("concepto_test", "Pago de servicio de agua"))
 
        if st.button("Enviar Dinero Ahora"):
            resultado = procesar_transaccion_segura("CUENTA_ROBERTO_123", cuenta_destino, monto, concepto)
 
            if resultado["estatus"] == "EXITO":
                st.markdown("""
                    <div class="alert-success">
                        <h3>Operacion procesada con exito</h3>
                        <p>El envio fue autorizado e inscrito correctamente en la red bancaria.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="assistant-box">
                        <div class="assistant-avatar">👩‍💼</div>
                        <div>
                            <b>Ana dice:</b>
                            <p>Bien hecho, esta transaccion se ve segura y ya quedo lista.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state["fraudes_bloqueados"] += 1
                st.session_state["dinero_protegido"] += monto
 
                st.markdown("""
                    <div class="alert-danger">
                        <h3>Operacion detenida por seguridad</h3>
                        <p>El sistema evito el movimiento para proteger su patrimonio. No se realizo cargo alguno.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="assistant-box">
                        <div class="assistant-avatar">👩‍💼</div>
                        <div>
                            <b>Ana dice:</b>
                            <p>Detuve este pago porque note algo inusual. Revisemos juntos los motivos antes de continuar.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
 
                st.write("#### Motivos de la retencion:")
                for alerta in resultado["alertas"]:
                    st.markdown(f"""
                        <div class="info-card">
                            <b>Alerta detectada:</b> {alerta}
                        </div>
                    """, unsafe_allow_html=True)
 
                st.info("Recomendacion: Si recibió instruccion telefonica de un tercero para hacer este pago, no la ejecute.")
        st.markdown('</div>', unsafe_allow_html=True)
 
    with col_right:
        if MODO_DEMO_JUECES:
            st.markdown("""
                <div class="card-panel">
                    <h3>Simulador para Evaluacion</h3>
                    <p>Cargue escenarios rapidos para presentar ante los jueces de Capital One:</p>
                </div>
            """, unsafe_allow_html=True)
 
            if st.button("Probar Transaccion Segura"):
                st.session_state["cuenta_test"] = "987654321"
                st.session_state["monto_test"] = 200.0
                st.session_state["concepto_test"] = "Compra de medicamentos"
                st.rerun()
 
            if st.button("Simular Riesgo: Monto Alto"):
                st.session_state["cuenta_test"] = "987654321"
                st.session_state["monto_test"] = 9500.0
                st.session_state["concepto_test"] = "Transferencia urgente"
                st.rerun()
 
            if st.button("Simular Riesgo: Fuga de NIP"):
                st.session_state["cuenta_test"] = "987654321"
                st.session_state["monto_test"] = 400.0
                st.session_state["concepto_test"] = "Pago con mi NIP 4321"
                st.rerun()
 
            if st.button("Simular Riesgo: Destinatario Nuevo"):
                st.session_state["cuenta_test"] = "555000111"
                st.session_state["monto_test"] = 1500.0
                st.session_state["concepto_test"] = "Ayuda urgente a un conocido"
                st.rerun()
 
with tab_bitacora:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.subheader("Historial de analisis en tiempo real")
    st.write("Registros analizados por el motor de reglas y la API de Capital One:")
 
    historial = obtener_historial_transacciones("CUENTA_ROBERTO_123")
    for item in historial:
        st.markdown(f"""
            <div style="background-color: #F1F5F9; border-left: 4px solid #4338CA; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                <p style="margin:0;"><b>Concepto:</b> {item.get('description', 'Sin concepto')} | <b>Monto:</b> ${item.get('amount', 0.0):,.2f} MXN</p>
                <p style="margin:0; font-size:14px; color:#64748B !important;">Estatus: Verificado y registrado</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
with tab_reglas:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.subheader("Politicas de proteccion activas")
 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="info-card">
                <h4 style="margin:0;">Tope de Alerta Automatica</h4>
                <p style="margin: 4px 0 0 0;">Monto maximo de operacion directa: $5,000.00 MXN.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="info-card">
                <h4 style="margin:0;">Filtro de Datos Confidenciales</h4>
                <p style="margin: 4px 0 0 0;">Bloqueo inmediato si la descripcion contiene NIP, passwords o PIN.</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)