import streamlit as st
from main_backend import procesar_transaccion_segura

# Configuración visual para accesibilidad
st.set_page_config(page_title="Banco Seguro - Adulto Mayor", layout="centered")

# Encabezado principal accesible
st.title("🛡️ Banco Seguro")
st.write("### Hola, Don Roberto 👋")
st.write("Su cuenta está protegida con el Asistente de Seguridad.")

st.markdown("---")

# Sección de transferencia de dinero
st.header("💸 Hacer una Transferencia")

# Campos de entrada con texto descriptivo
cuenta_destino = st.text_input("1. Escriba la cuenta o número de teléfono del destinatario:", "987654321")
monto = st.number_input("2. ¿Cuánto dinero desea enviar? ($):", min_value=1.0, value=500.0, step=100.0)
concepto = st.text_input("3. ¿Para qué es este dinero? (Concepto):", "Pago de despensa")

# Botón de acción destacado
if st.button("CONFIRMAR Y ENVIAR DINERO", type="primary"):
    cuenta_origen = "CUENTA_ROBERTO_123"
    
    # Procesar la transacción mediante tu backend
    resultado = procesar_transaccion_segura(cuenta_origen, cuenta_destino, monto, concepto)
    
    st.markdown("---")
    
    # Manejo de respuestas según la evaluación de riesgo
    if resultado["estatus"] == "EXITO":
        st.balloons()
        st.success("✅ **¡Transferencia realizada con éxito!**")
        st.write(f"Se enviaron **${monto}** correctamente.")
    else:
        # Pantalla de alerta accesible en caso de riesgo
        st.error("🚨 **TRANSACCIÓN BLOQUEADA POR SEGURIDAD**")
        st.subheader("Detectamos un riesgo en esta operación:")
        
        for alerta in resultado["alertas"]:
            st.warning(f"⚠️ {alerta}")
            
        st.info("👉 **No se ha descontado dinero de su cuenta.** Hemos enviado una notificación de confirmación a su contacto de confianza (Hijo / Familiar).")