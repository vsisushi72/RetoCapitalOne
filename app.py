import streamlit as st
import random
import time
from datetime import datetime
from main_backend import procesar_transaccion_segura
from nessie_client import obtener_saldo_cuenta, obtener_historial_transacciones

MODO_DEMO_JUECES = True
RUTA_LOGO = "assets/capital_one_logo.jpeg"

TARJETA_DEMO_NOMBRE = "Roberto Gomez"
TARJETA_DEMO_NUMERO = "4539 1488 0343 6467"
TARJETA_DEMO_NIP = "4321"

TIPS_SEGURIDAD = [
    "Nunca compartas tu NIP o contraseña, ni con el banco ni con nadie por telefono.",
    "Si alguien te presiona para transferir dinero con urgencia, cuelga y verifica con un familiar.",
    "Yo reviso cada pago automaticamente antes de que salga de tu cuenta.",
    "Un destinatario nuevo con monto alto siempre merece una segunda confirmacion."
]

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
if "nivel_fuente" not in st.session_state:
    st.session_state["nivel_fuente"] = "normal"
if "mensaje_ana" not in st.session_state:
    st.session_state["mensaje_ana"] = f"{obtener_saludo()}, Roberto. {random.choice(TIPS_SEGURIDAD)}"
if "titulo_ana" not in st.session_state:
    st.session_state["titulo_ana"] = "Ana, tu asesora de seguridad"
if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "splash"

st.set_page_config(page_title="Guardian Financiero Senior", layout="wide")

if st.session_state["pantalla"] == "splash":
    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    with col_centro:
        st.write("")
        st.write("")
        st.write("")
        st.image(RUTA_LOGO, use_container_width=True)
        st.markdown("""
            <p style="text-align:center; font-size:18px; color:#475569; margin-top:16px;">
                Cargando Guardian Financiero Senior...
            </p>
        """, unsafe_allow_html=True)
    time.sleep(2.5)
    st.session_state["pantalla"] = "login"
    st.rerun()

if st.session_state["pantalla"] == "login":
    st.write("### Ingresa a tu cuenta")
    st.write("(Pantalla provisional, el diseno final se agrega despues)")

    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    with col_centro:
        numero_ingresado = st.text_input("Numero de tarjeta (16 digitos)", max_chars=19, placeholder="0000 0000 0000 0000")
        nip_ingresado = st.text_input("NIP", max_chars=4, type="password", placeholder="****")

        if st.button("Ingresar"):
            numero_limpio = "".join(ch for ch in numero_ingresado if ch.isdigit())
            tarjeta_limpia = "".join(ch for ch in TARJETA_DEMO_NUMERO if ch.isdigit())

            if numero_limpio == tarjeta_limpia and nip_ingresado == TARJETA_DEMO_NIP:
                st.session_state["pantalla"] = "seleccion"
                st.rerun()
            else:
                st.error("Numero de tarjeta o NIP incorrectos. Intenta de nuevo.")
    st.stop()

if st.session_state["pantalla"] == "seleccion":
    st.write("### Elige como quieres usar la aplicacion")
    st.write("(Botones provisionales, el diseno final se agrega despues)")

    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button("Interfaz Clasica", "https://www.capitalone.com")
    with col_b:
        if st.button("Interfaz Facil"):
            st.session_state["pantalla"] = "tamano_fuente"
            st.rerun()
    st.stop()

if st.session_state["pantalla"] == "tamano_fuente":
    st.write("### Elige el tamano de letra con el que quieres ver la app")
    st.write("(Botones provisionales, el diseno final se agrega despues)")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("Texto Normal"):
            st.session_state["nivel_fuente"] = "normal"
            st.session_state["pantalla"] = "app"
            st.rerun()
    with col_b:
        if st.button("Texto Grande"):
            st.session_state["nivel_fuente"] = "grande"
            st.session_state["pantalla"] = "app"
            st.rerun()
    with col_c:
        if st.button("Texto Muy Grande"):
            st.session_state["nivel_fuente"] = "muy_grande"
            st.session_state["pantalla"] = "app"
            st.rerun()
    st.stop()

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

    .ana-anchor {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 9999 !important;
        max-width: 320px !important;
        background-color: #EEF2FF !important;
        border: 2px solid #4338CA !important;
        border-radius: 18px !important;
        padding: 16px 18px !important;
        display: flex !important;
        align-items: flex-start !important;
        gap: 12px !important;
        box-shadow: 0 8px 20px rgba(67, 56, 202, 0.25) !important;
    }
    .ana-anchor .assistant-avatar {
        font-size: 34px !important;
    }
    .ana-anchor b {
        color: #3730A3 !important;
        font-size: 14px !important;
    }
    .ana-anchor p {
        margin: 4px 0 0 0 !important;
        font-size: 14px !important;
        color: #1E1B4B !important;
    }
    @media (max-width: 640px) {
        .ana-anchor {
            left: 12px !important;
            right: 12px !important;
            bottom: 12px !important;
            max-width: none !important;
        }
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

if st.session_state["nivel_fuente"] in ("grande", "muy_grande"):
    if st.session_state["nivel_fuente"] == "grande":
        tam_base, tam_h1, tam_h2, tam_h3, tam_boton, tam_input = "20px", "40px", "34px", "26px", "22px", "22px"
    else:
        tam_base, tam_h1, tam_h2, tam_h3, tam_boton, tam_input = "26px", "48px", "40px", "32px", "28px", "28px"

    st.markdown(f"""
        <style>
        html, body, .stApp, p, span, label, li, div {{
            font-size: {tam_base} !important;
        }}
        h1 {{ font-size: {tam_h1} !important; }}
        h2 {{ font-size: {tam_h2} !important; }}
        h3 {{ font-size: {tam_h3} !important; }}
        .stButton button {{
            font-size: {tam_boton} !important;
            padding: 16px 24px !important;
        }}
        .stTextInput input, .stNumberInput input {{
            font-size: {tam_input} !important;
            padding: 14px !important;
        }}
        html, body, .stApp {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }}
        p, span, label, h1, h2, h3, h4, h5, h6, div {{
            color: #000000 !important;
        }}
        .card-panel, .metric-box, .assistant-box, .ana-anchor {{
            border-width: 3px !important;
        }}
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

    opciones_fuente = {"normal": "Normal", "grande": "Grande", "muy_grande": "Muy Grande"}
    st.session_state["nivel_fuente"] = st.radio(
        "Tamano de letra",
        options=list(opciones_fuente.keys()),
        format_func=lambda k: opciones_fuente[k],
        index=list(opciones_fuente.keys()).index(st.session_state["nivel_fuente"])
    )

st.markdown("""
    <div class="header-panel">
        <h1>Guardian Financiero Senior</h1>
        <p>Plataforma de transacciones protegidas con deteccion de riesgo en tiempo real</p>
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
                st.session_state["titulo_ana"] = "Ana dice:"
                st.session_state["mensaje_ana"] = "Bien hecho, esta transaccion se ve segura y ya quedo lista."
            else:
                st.session_state["fraudes_bloqueados"] += 1
                st.session_state["dinero_protegido"] += monto

                st.markdown("""
                    <div class="alert-danger">
                        <h3>Operacion detenida por seguridad</h3>
                        <p>El sistema evito el movimiento para proteger su patrimonio. No se realizo cargo alguno.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.session_state["titulo_ana"] = "Ana dice:"
                st.session_state["mensaje_ana"] = "Detuve este pago porque note algo inusual. Revisemos juntos los motivos antes de continuar."

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
    st.markdown("""
        <div class="assistant-box" style="margin-bottom:16px;">
            <div class="assistant-avatar">👩‍💼</div>
            <div>
                <b>Ana dice:</b>
                <p>Aqui puedes ver tus movimientos recientes, para que nunca haya sorpresas en tu cuenta.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
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
    st.markdown("""
        <div class="assistant-box" style="margin-bottom:16px;">
            <div class="assistant-avatar">👩‍💼</div>
            <div>
                <b>Ana dice:</b>
                <p>Estas son las reglas que uso para cuidar tu dinero, explicadas en palabras simples.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

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

st.markdown(f"""
    <div class="ana-anchor">
        <div class="assistant-avatar">👩‍💼</div>
        <div>
            <b>{st.session_state['titulo_ana']}</b>
            <p>{st.session_state['mensaje_ana']}</p>
        </div>
    </div>
""", unsafe_allow_html=True)