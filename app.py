import streamlit as st
import random
import time
import base64
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

def imagen_a_base64(ruta: str) -> str:
    with open(ruta, "rb") as archivo_imagen:
        return base64.b64encode(archivo_imagen.read()).decode("utf-8")

def etiqueta_tamano_letra(valor: int) -> str:
    return f"""
        <div style="display:inline-block;
                    font-size:14px; font-weight:700; letter-spacing:0.4px;
                    text-transform:uppercase; color:#5B6570; padding:4px 8px;
                    margin-bottom:5px;">
            Tamaño de letra: {valor}%
        </div>
    """

if "fraudes_bloqueados" not in st.session_state:
    st.session_state["fraudes_bloqueados"] = 12 if MODO_DEMO_JUECES else 0
if "dinero_protegido" not in st.session_state:
    st.session_state["dinero_protegido"] = 45230.0 if MODO_DEMO_JUECES else 0.0
if "escala_fuente" not in st.session_state:
    st.session_state["escala_fuente"] = 100
if "mensaje_ana" not in st.session_state:
    st.session_state["mensaje_ana"] = f"{obtener_saludo()}, Roberto. {random.choice(TIPS_SEGURIDAD)}"
if "titulo_ana" not in st.session_state:
    st.session_state["titulo_ana"] = "Ana, tu asesora de seguridad"
if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "splash"

st.set_page_config(page_title="Guardian Financiero Senior", layout="wide")

# ============================================================
# ESTILOS BASE Y REGLAS DE LIMPIEZA (PALETA CORPORATIVA FORMAL)
# ============================================================
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #F2F4F7 !important;
        color: #1A2027 !important;
        font-family: 'Segoe UI', 'Inter', Roboto, Helvetica, Arial, sans-serif !important;
    }

    p, span, label, h1, h2, h3, h4, h5, h6, div {
        color: #1A2027 !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #DCE1E7 !important;
    }

    .card-panel {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-radius: 12px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 2px 8px rgba(18, 38, 58, 0.06) !important;
    }

    .header-panel {
        background-color: #12263A !important;
        border-radius: 12px !important;
        border-bottom: 4px solid #B08D57 !important;
        margin-bottom: 24px !important;
    }
    .header-panel h1 {
        color: #FFFFFF !important;
        margin: 0 !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
    }
    .header-panel p {
        color: #E4ECF5 !important;
        margin: 6px 0 0 0 !important;
    }

    .balance-box {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-left: 4px solid #1E5631 !important;
        border-radius: 12px !important;
        text-align: left !important;
        margin-bottom: 20px !important;
        box-shadow: 0 2px 8px rgba(18, 38, 58, 0.05) !important;
    }
    .balance-box span {
        color: #5B6570 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.4px !important;
    }
    .balance-box h2 {
        color: #12263A !important;
        margin: 6px 0 0 0 !important;
        font-weight: 700 !important;
    }

    .alert-danger {
        background-color: #FBECEC !important;
        border: 1px solid #D98A8A !important;
        border-left: 4px solid #A13A3A !important;
        border-radius: 10px !important;
        padding: 18px !important;
        margin-top: 16px !important;
    }
    .alert-danger h3 {
        color: #7A1F1F !important;
        margin: 0 0 6px 0 !important;
        font-weight: 700 !important;
    }
    .alert-danger p {
        color: #5C2323 !important;
        margin: 0 !important;
    }

    .alert-success {
        background-color: #EAF4EC !important;
        border: 1px solid #9CC7A8 !important;
        border-left: 4px solid #1E5631 !important;
        border-radius: 10px !important;
        padding: 18px !important;
        margin-top: 16px !important;
    }
    .alert-success h3 {
        color: #1E5631 !important;
        margin: 0 !important;
        font-weight: 700 !important;
    }

    .info-card {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-left: 4px solid #B08D57 !important;
        border-radius: 10px !important;
        margin-bottom: 12px !important;
    }

    .stTextInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #1A2027 !important;
        border: 1px solid #C7CFD8 !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border: 1px solid #12263A !important;
        box-shadow: 0 0 0 1px #12263A !important;
    }

    .stButton button {
        background-color: #12263A !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: none !important;
    }
    .stButton button:hover {
        background-color: #1F3B57 !important;
        color: #FFFFFF !important;
    }

    /* FIX: el texto de estos botones vive dentro de un <p>, y la regla
       general "p { color:#1A2027 }" de arriba lo pintaba oscuro sobre
       fondo oscuro y se perdia. Aqui se fuerza blanco y una letra mas
       grande SOLO en los botones oscuros que lo necesitaban
       (Ingresar, Continuar, Enviar Dinero Ahora). Los botones de
       navegacion (VER SALDO / TRANSFERENCIA / MOVIMIENTOS) y el de
       "Cuenta Senior" no se tocan porque tienen fondo blanco/imagen. */
    .st-key-btn_ingresar button p,
    .st-key-btn_continuar_tamano button p,
    .st-key-btn_enviar_dinero button p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 19px !important;
    }

    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 0 !important;
        padding: 12px 20px !important;
        border-bottom: 2px solid transparent !important;
    }
    button[aria-selected="true"] {
        background-color: transparent !important;
        border-bottom: 2px solid #12263A !important;
    }
    button[aria-selected="true"] p {
        color: #12263A !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="tab-list"] {
        border-bottom: 1px solid #DCE1E7 !important;
        gap: 4px !important;
    }

    .metric-box {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-radius: 12px !important;
        text-align: left !important;
        box-shadow: 0 2px 8px rgba(18, 38, 58, 0.05) !important;
    }
    .metric-box span {
        font-weight: 600 !important;
        color: #5B6570 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.4px !important;
    }
    .metric-box h2 {
        margin: 6px 0 0 0 !important;
        font-weight: 700 !important;
    }
    .metric-saldo { border-top: 3px solid #12263A !important; }
    .metric-bloqueos { border-top: 3px solid #A13A3A !important; }
    .metric-protegido { border-top: 3px solid #1E5631 !important; }
    .metric-saldo h2 { color: #12263A !important; }
    .metric-bloqueos h2 { color: #A13A3A !important; }
    .metric-protegido h2 { color: #1E5631 !important; }

    .assistant-box {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-left: 4px solid #12263A !important;
        border-radius: 12px !important;
        padding: 18px 20px !important;
        margin-bottom: 20px !important;
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
        box-shadow: 0 2px 8px rgba(18, 38, 58, 0.05) !important;
    }
    .assistant-avatar {
        font-size: 36px !important;
        line-height: 1 !important;
    }
    .assistant-box b {
        color: #12263A !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.3px !important;
    }
    .assistant-box p {
        margin: 4px 0 0 0 !important;
        font-size: 15px !important;
        color: #1A2027 !important;
    }

    .ana-anchor {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 9999 !important;
        max-width: 320px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-left: 4px solid #12263A !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        display: flex !important;
        align-items: flex-start !important;
        gap: 12px !important;
        box-shadow: 0 8px 24px rgba(18, 38, 58, 0.18) !important;
    }
    .ana-anchor .assistant-avatar {
        font-size: 30px !important;
    }
    .ana-anchor b {
        color: #12263A !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.3px !important;
    }
    .ana-anchor p {
        margin: 4px 0 0 0 !important;
        font-size: 14px !important;
        color: #1A2027 !important;
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
        border: 1px solid #DCE1E7 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpander"] * {
        background-color: #FFFFFF !important;
        color: #1A2027 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-radius: 12px !important;
    }

    .auth-card {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-top: 4px solid #12263A !important;
        border-radius: 14px !important;
        padding: 36px 32px !important;
        box-shadow: 0 4px 20px rgba(18, 38, 58, 0.08) !important;
    }
    .auth-card h2 {
        margin: 0 0 6px 0 !important;
        text-align: center !important;
        font-weight: 700 !important;
    }
    .auth-card p.auth-subtitle {
        text-align: center !important;
        color: #5B6570 !important;
        margin: 0 0 24px 0 !important;
        font-size: 14px !important;
    }

    .option-tile {
        background-color: #FFFFFF !important;
        border: 1px solid #DCE1E7 !important;
        border-radius: 14px !important;
        padding: 22px 20px !important;
        text-align: center !important;
        height: 100% !important;
        box-shadow: 0 2px 10px rgba(18, 38, 58, 0.05) !important;
    }
    .option-tile h3 {
        margin: 0 0 6px 0 !important;
        font-weight: 700 !important;
    }
    .option-tile p {
        color: #5B6570 !important;
        font-size: 14px !important;
        margin: 0 0 14px 0 !important;
    }

    .brand-lockup {
        text-align: center !important;
        color: #5B6570 !important;
        font-size: 15px !important;
        margin-top: 16px !important;
        letter-spacing: 0.3px !important;
    }

    a[data-testid="stLinkButton"] > div,
    .stLinkButton a {
        background-color: #FFFFFF !important;
        color: #12263A !important;
        border: 1px solid #12263A !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        width: 100% !important;
        justify-content: center !important;
    }

    /* SLIDER EN TONO CORPORATIVO */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #12263A !important;
        border: 3px solid #FFFFFF !important;
        box-shadow: 0 0 0 2px #12263A !important;
        width: 20px !important;
        height: 20px !important;
    }
    div[data-testid="stSlider"] * {
        color: #1A2027 !important;
        background-color: transparent !important;
    }
    /* Los numeros del slider (100% / valor actual / 150%) son pintados
       por Streamlit con su propio fondo oscuro, y la regla de arriba
       les dejaba el texto oscuro tambien -> letra invisible sobre fondo
       oscuro, igual que paso antes con el encabezado. En vez de pelear
       por dejarlos transparentes (su fondo real puede venir de un
       elemento "portal" fuera de nuestro alcance), se les da un fondo
       navy A PROPOSITO y letra blanca, garantizando contraste siempre,
       vengan de donde vengan en el DOM. */
    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"],
    div[data-testid="stSlider"] [data-testid="stSliderThumbValue"],
    div[data-testid="stSlider"] div[role="slider"] div,
    div[data-baseweb="tooltip"] {
        background-color: #12263A !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
    }
    div[data-testid="stSliderTickBarWithLabels"] {
        background-color: transparent !important;
    }
    div[data-testid="stSlider"] [data-baseweb="tooltip"] {
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state["pantalla"] == "splash":
    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    with col_centro:
        st.write("")
        st.write("")
        st.write("")
        st.image(RUTA_LOGO, use_container_width=True)
        st.markdown("""
            <p class="brand-lockup">
                Cargando Guardian Financiero Senior...
            </p>
        """, unsafe_allow_html=True)
    time.sleep(2.5)
    st.session_state["pantalla"] = "login"
    st.rerun()

if st.session_state["pantalla"] == "login":
    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("""
            <div class="auth-card">
                <h2>Ingresa a tu cuenta</h2>
                <p class="auth-subtitle">Escribe los datos de tu tarjeta para continuar de forma segura</p>
        """, unsafe_allow_html=True)

        numero_ingresado = st.text_input("Numero de tarjeta (16 digitos)", max_chars=19, placeholder="0000 0000 0000 0000")
        nip_ingresado = st.text_input("NIP", max_chars=4, type="password", placeholder="****")

        with st.container(key="btn_ingresar"):
            clic_ingresar = st.button("Ingresar")

        if clic_ingresar:
            numero_limpio = "".join(ch for ch in numero_ingresado if ch.isdigit())
            tarjeta_limpia = "".join(ch for ch in TARJETA_DEMO_NUMERO if ch.isdigit())

            if numero_limpio == tarjeta_limpia and nip_ingresado == TARJETA_DEMO_NIP:
                st.session_state["pantalla"] = "seleccion"
                st.rerun()
            else:
                st.error("Numero de tarjeta o NIP incorrectos. Intenta de nuevo.")

        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if st.session_state["pantalla"] == "seleccion":
    col_izq, col_centro, col_der = st.columns([1, 3, 1])
    with col_centro:
        st.markdown("""
            <h2 style="text-align:center;">¿Como quieres usar la aplicacion?</h2>
            <p class="brand-lockup" style="margin-bottom:24px;">Elige la opcion con la que te sientas mas comodo</p>
        """, unsafe_allow_html=True)

        img_clasico_b64 = imagen_a_base64("assets/modelo_clasico.png")
        img_senior_b64 = imagen_a_base64("assets/modelo_senior.png")

        col_a, col_b = st.columns(2)

        with col_a:
            # Clasica sale de la app hacia una pagina externa, un enlace normal esta bien aqui
            st.markdown(f"""
                <div class="option-tile">
                    <a href="https://www.capitalone.com" target="_self" style="text-decoration:none;">
                        <img src="data:image/png;base64,{img_clasico_b64}"
                             style="width:100%; height:230px; object-fit:cover; border-radius:10px; cursor:pointer; display:block;">
                    </a>
                    <p style="margin:14px 0 0 0; text-align:center; color:#5B6570; font-size:15px;">La banca en linea de siempre, con todas las opciones disponibles.</p>
                </div>
            """, unsafe_allow_html=True)

        with col_b:
            # Senior se queda DENTRO de la app: en vez de superponer un boton
            # invisible sobre la imagen (poco confiable), hacemos que el propio
            # boton tenga la imagen como fondo. Es un solo elemento clicable,
            # nativo de Streamlit, por lo que no recarga la pagina ni reinicia
            # la sesion (no vuelve a pedir tarjeta y NIP).
            with st.container(key="tile_senior"):
                clic_senior = st.button(" ", key="btn_senior", use_container_width=True)
                st.markdown(
                    "<p style='margin:14px 0 0 0; text-align:center; color:#5B6570; font-size:15px;'>Botones grandes, letra ajustable y proteccion explicada en palabras simples.</p>",
                    unsafe_allow_html=True
                )

    st.markdown(f"""
        <style>
        .st-key-tile_senior {{
            background-color: #FFFFFF !important;
            border: 1px solid #DCE1E7 !important;
            border-radius: 14px !important;
            padding: 22px 20px !important;
            height: 100% !important;
            box-shadow: 0 2px 10px rgba(18, 38, 58, 0.05) !important;
        }}
        .st-key-tile_senior div[data-testid="stButton"] button {{
            background-image: url("data:image/png;base64,{img_senior_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: transparent !important;
            width: 100%;
            height: 230px !important;
            min-height: 0 !important;
            border: none !important;
            border-radius: 10px !important;
            color: transparent;
            box-shadow: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    if clic_senior:
        st.session_state["pantalla"] = "tamano_fuente"
        st.rerun()

    st.stop()

if st.session_state["pantalla"] == "tamano_fuente":
    col_izq, col_centro, col_der = st.columns([1, 3, 1])
    with col_centro:
        st.markdown("""
            <h2 style="text-align:center; color:#1A2027;">¿Que tan grande quieres ver el texto?</h2>
            <p style="text-align:center; color:#5B6570; font-size:15px;">
                Mueve la barra hasta que el ejemplo de abajo se vea comodo para ti.
                Podras cambiarlo despues en cualquier momento desde el menu lateral.
            </p>
        """, unsafe_allow_html=True)

        escala = st.slider(
            "Tamano de letra",
            min_value=100,
            max_value=150,
            value=st.session_state["escala_fuente"],
            step=10,
            format="%d%%",
            label_visibility="collapsed"
        )
        st.session_state["escala_fuente"] = escala

        st.markdown(f"<div style='text-align:center;'>{etiqueta_tamano_letra(escala)}</div>", unsafe_allow_html=True)

        tam_preview = round(18 * escala / 100)
        st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #DCE1E7; border-top:4px solid #12263A; border-radius:14px; padding:24px; text-align:center; margin:16px 0;">
                <p style="font-size:{tam_preview}px; color:#1A2027; margin:0; line-height:1.5;">
                    Asi se vera el texto en tu aplicacion.<br>Saldo disponible: $18,420.00 MXN
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        with st.container(key="btn_continuar_tamano"):
            clic_continuar = st.button("Continuar con este tamano")
        if clic_continuar:
            st.session_state["pantalla"] = "app"
            st.rerun()
    st.stop()


# ============================================================
# CÁLCULO PROPORCIONAL Y ESCALADO DINÁMICO DE CONTENEDORES
# ============================================================
escala = min(max(st.session_state["escala_fuente"], 100), 150)
st.session_state["escala_fuente"] = escala

# Escalado de tipografía
# (Bases mas grandes para que, incluso al 100%, el texto se lea con
# comodidad; el slider de "Tamano de letra" sigue multiplicando desde aqui)
tam_base = round(19 * escala / 100)
tam_h1 = round(36 * escala / 100)
tam_h2 = round(28 * escala / 100)
tam_h3 = round(22 * escala / 100)
tam_boton = round(19 * escala / 100)
tam_input = round(19 * escala / 100)

# Escalado de dimensiones de contenedores (tarjetas y rectángulos)
pad_card = round(20 * escala / 100)
pad_header = round(24 * escala / 100)
pad_boton = round(12 * escala / 100)
pad_input = round(10 * escala / 100)
min_alto_metrica = round(130 * escala / 100)

st.markdown(f"""
    <style>
    /* Escalado de fuentes */
    p, span, label, li {{
        font-size: {tam_base}px !important;
    }}
    h1 {{ font-size: {tam_h1}px !important; }}
    h2 {{ font-size: {tam_h2}px !important; }}
    h3 {{ font-size: {tam_h3}px !important; }}

    /* Escalado de controles */
    .stButton button {{
        font-size: {tam_boton}px !important;
        padding: {pad_boton}px {pad_boton * 2}px !important;
    }}
    .stTextInput input, .stNumberInput input {{
        font-size: {tam_input}px !important;
        padding: {pad_input}px !important;
    }}

    /* Escalado dinámico de contendores para crecer con la fuente */
    .card-panel {{
        padding: {pad_card}px !important;
    }}
    .header-panel {{
        padding: {pad_header}px !important;
    }}
    .metric-box {{
        padding: {pad_card}px !important;
        min-height: {min_alto_metrica}px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }}
    .balance-box {{
        padding: {pad_card}px !important;
    }}
    .info-card {{
        padding: {pad_card - 4}px !important;
    }}

    /* Los botones oscuros deben mantenerse en blanco tambien al reescalar letra */
    .st-key-btn_enviar_dinero button p {{
        color: #FFFFFF !important;
        font-size: {max(tam_boton, 18)}px !important;
        font-weight: 700 !important;
    }}
    </style>
""", unsafe_allow_html=True)

if "seccion_activa" not in st.session_state:
    st.session_state["seccion_activa"] = "saldo"

# ============================================================
# ESTADO LOCAL DE SALDO Y MOVIMIENTOS
# Se cargan una sola vez desde el backend/Nessie y, a partir de ahi,
# viven en session_state para que una transferencia se refleje al
# instante (se descuenta el saldo y aparece en movimientos) sin
# depender de la latencia o el cacheo del API externo.
# ============================================================
if "saldo_actual" not in st.session_state:
    st.session_state["saldo_actual"] = float(obtener_saldo_cuenta("CUENTA_ROBERTO_123"))
if "historial_local" not in st.session_state:
    st.session_state["historial_local"] = list(obtener_historial_transacciones("CUENTA_ROBERTO_123"))

with st.sidebar:
    st.markdown("""
        <div class="card-panel">
            <h3 style="margin:0 0 10px 0; font-size:16px; text-transform:uppercase; letter-spacing:0.3px;">Mi Cuenta</h3>
            <p style="margin:4px 0;"><b>Nombre:</b> Roberto Gómez</p>
            <p style="margin:4px 0;"><b>Edad:</b> 68 años</p>
            <p style="margin:4px 0;"><b>Tipo de cuenta:</b> Cuenta Senior</p>
            <hr style="border-color:#DCE1E7;">
            <p style="margin:4px 0;">✅ Tu cuenta está siendo protegida en tiempo real</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(etiqueta_tamano_letra(escala), unsafe_allow_html=True)
        nueva_escala = st.slider(
            "Ajustar tamano de letra",
            min_value=100,
            max_value=150,
            value=escala,
            step=10,
            format="%d%%",
            label_visibility="collapsed",
            key="slider_sidebar_fuente"
        )

    if nueva_escala != st.session_state["escala_fuente"]:
        st.session_state["escala_fuente"] = nueva_escala
        st.rerun()

    with st.expander("Configuracion de Seguridad"):
        st.markdown("""
            <p style="margin:0 0 10px 0; color:#5B6570; font-size:14px;">
                Estas son las reglas que Ana usa para cuidar tu dinero, explicadas en palabras simples.
            </p>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="info-card">
                <h4 style="margin:0; font-size:15px;">Tope de Alerta Automatica</h4>
                <p style="margin: 4px 0 0 0; color:#5B6570; font-size:14px;">Monto maximo de operacion directa: $5,000.00 MXN.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="info-card">
                <h4 style="margin:0; font-size:15px;">Filtro de Datos Confidenciales</h4>
                <p style="margin: 4px 0 0 0; color:#5B6570; font-size:14px;">Bloqueo inmediato si la descripcion contiene NIP, passwords o PIN.</p>
            </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------
# El titulo y subtitulo se generan como IMAGEN (SVG -> base64),
# no como texto HTML. Motivo: algo del navegador (muy probable:
# el "modo oscuro forzado" de Chrome/Android, que auto-oscurece
# el texto de las paginas pero deja las imagenes intactas) le
# seguia cambiando el color al texto sin importar el CSS o los
# estilos en linea con !important. Una imagen no se ve afectada
# por eso -- por eso el logo de Capital One SI se veia bien y el
# texto no. Convirtiendo el titulo en imagen queda inmune.
# ------------------------------------------------------------
tam_titulo_header = round(38 * escala / 100)
tam_subtitulo_header = round(18 * escala / 100)
alto_logo_header = round(76 * escala / 100)
logo_header_b64 = imagen_a_base64(RUTA_LOGO)

svg_titulo_header = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="950" height="90">
    <text x="0" y="42" font-family="Segoe UI, Arial, sans-serif" font-size="{tam_titulo_header}" font-weight="800" fill="#FFFFFF">Guardian Financiero Senior</text>
    <text x="0" y="74" font-family="Segoe UI, Arial, sans-serif" font-size="{tam_subtitulo_header}" fill="#E4ECF5">Plataforma de transacciones protegidas con deteccion de riesgo en tiempo real</text>
</svg>
""".strip()
svg_titulo_header_b64 = base64.b64encode(svg_titulo_header.encode("utf-8")).decode("utf-8")

st.markdown(f"""
    <div class="header-panel" style="display:flex; align-items:center; justify-content:space-between; gap:22px;">
        <img src="data:image/svg+xml;base64,{svg_titulo_header_b64}"
             style="height:70px; width:auto; display:block;">
        <img src="data:image/jpeg;base64,{logo_header_b64}"
             style="height:{alto_logo_header}px; width:auto; border-radius:8px; background-color:#FFFFFF; padding:8px; flex-shrink:0;">
    </div>
""", unsafe_allow_html=True)

saldo_dashboard = st.session_state["saldo_actual"]

# ============================================================
# ACCESOS PRINCIPALES: VER SALDO / TRANSFERENCIA / MOVIMIENTOS
# Botones nativos y funcionales (cambian de seccion sin recargar
# la pagina ni perder la sesion), con colores de la paleta.
# ============================================================
col_n1, col_n2, col_n3 = st.columns(3)

with col_n1:
    with st.container(key="nav_saldo"):
        clic_saldo = st.button("VER SALDO", key="btn_nav_saldo", use_container_width=True)
with col_n2:
    with st.container(key="nav_transferencia"):
        clic_transferencia = st.button("TRANSFERENCIA", key="btn_nav_transferencia", use_container_width=True)
with col_n3:
    with st.container(key="nav_movimientos"):
        clic_movimientos = st.button("MOVIMIENTOS", key="btn_nav_movimientos", use_container_width=True)

st.markdown(f"""
    <style>
    .st-key-nav_saldo button, .st-key-nav_transferencia button, .st-key-nav_movimientos button {{
        height: 110px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: #FFFFFF !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        letter-spacing: 0.4px !important;
        font-size: {max(tam_boton, 17)}px !important;
        box-shadow: 0 2px 10px rgba(18, 38, 58, 0.05) !important;
    }}
    /* El texto real vive en un <p> dentro del boton; se fuerza el mismo
       color e tamaño ahi para que no se pierda ni se vea mas chico. */
    .st-key-nav_saldo button p, .st-key-nav_transferencia button p, .st-key-nav_movimientos button p {{
        font-size: {max(tam_boton, 17)}px !important;
        font-weight: 700 !important;
    }}
    .st-key-nav_saldo button {{
        border: 1px solid #DCE1E7 !important;
        border-top: 4px solid #12263A !important;
        color: #12263A !important;
    }}
    .st-key-nav_saldo button p {{
        color: #12263A !important;
    }}
    .st-key-nav_saldo button::before {{
        content: "💰";
        font-size: 30px;
        margin-bottom: 8px;
    }}
    .st-key-nav_transferencia button {{
        border: 1px solid #DCE1E7 !important;
        border-top: 4px solid #B08D57 !important;
        color: #8A6C3F !important;
    }}
    .st-key-nav_transferencia button p {{
        color: #8A6C3F !important;
    }}
    .st-key-nav_transferencia button::before {{
        content: "🔁";
        font-size: 30px;
        margin-bottom: 8px;
    }}
    .st-key-nav_movimientos button {{
        border: 1px solid #DCE1E7 !important;
        border-top: 4px solid #1E5631 !important;
        color: #1E5631 !important;
    }}
    .st-key-nav_movimientos button p {{
        color: #1E5631 !important;
    }}
    .st-key-nav_movimientos button::before {{
        content: "🧾";
        font-size: 30px;
        margin-bottom: 8px;
    }}
    .st-key-nav_saldo button:hover, .st-key-nav_transferencia button:hover, .st-key-nav_movimientos button:hover {{
        background-color: #F7F9FB !important;
    }}
    </style>
""", unsafe_allow_html=True)

if clic_saldo:
    st.session_state["seccion_activa"] = "saldo"
    st.rerun()
if clic_transferencia:
    st.session_state["seccion_activa"] = "transferencia"
    st.rerun()
if clic_movimientos:
    st.session_state["seccion_activa"] = "movimientos"
    st.rerun()

st.write("")

# ============================================================
# CONTENIDO SEGUN LA SECCION ACTIVA
# ============================================================
if st.session_state["seccion_activa"] == "saldo":
    st.markdown(f"""
        <div class="balance-box">
            <span style="font-size:{max(round(14 * escala / 100), 13)}px;">Saldo disponible en cuenta corriente</span>
            <h2 style="font-size:{tam_h2}px;">${saldo_dashboard:,.2f} MXN</h2>
        </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
            <div class="metric-box metric-bloqueos">
                <span style="font-size:{max(round(14 * escala / 100), 13)}px;">Intentos de fraude bloqueados este mes</span>
                <h2 style="font-size:{tam_h2}px;">{st.session_state['fraudes_bloqueados']}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
            <div class="metric-box metric-protegido">
                <span style="font-size:{max(round(14 * escala / 100), 13)}px;">Dinero total protegido</span>
                <h2 style="font-size:{tam_h2}px;">${st.session_state['dinero_protegido']:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state["seccion_activa"] == "transferencia":
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    st.subheader("Datos de la transferencia")

    cuenta_destino = st.text_input("Numero de cuenta o telefono de destino", value=st.session_state.get("cuenta_test", "987654321"))
    monto = st.number_input("Monto a enviar (MXN)", min_value=1.0, value=float(st.session_state.get("monto_test", 350.0)), step=50.0)
    concepto = st.text_input("Concepto o motivo del pago", value=st.session_state.get("concepto_test", "Pago de servicio de agua"))

    with st.container(key="btn_enviar_dinero"):
        clic_enviar = st.button("Enviar Dinero Ahora")

    if clic_enviar:
        resultado = procesar_transaccion_segura("CUENTA_ROBERTO_123", cuenta_destino, monto, concepto)

        if resultado["estatus"] == "EXITO":
            # Se descuenta el saldo local y se agrega el movimiento al
            # historial de inmediato, para que "Ver saldo" y "Movimientos"
            # queden actualizados sin depender de otra llamada al backend.
            st.session_state["saldo_actual"] = float(st.session_state["saldo_actual"]) - float(monto)
            st.session_state["historial_local"].insert(0, {
                "description": concepto,
                "amount": float(monto),
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            })

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

elif st.session_state["seccion_activa"] == "movimientos":
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

    historial = st.session_state["historial_local"]
    for item in historial:
        st.markdown(f"""
            <div style="background-color: #FFFFFF; border: 1px solid #DCE1E7; border-left: 4px solid #12263A; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                <p style="margin:0;"><b>Concepto:</b> {item.get('description', 'Sin concepto')} | <b>Monto:</b> ${item.get('amount', 0.0):,.2f} MXN</p>
                <p style="margin:0; font-size:13px; color:#5B6570 !important;">Estatus: Verificado y registrado</p>
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