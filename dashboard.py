import streamlit as st
from datetime import date
import openpyxl
# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN INICIAL 
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.get("authentication_status"):
    # st.toast(f"- {st.session_state['username']}", icon="👋")
    st.set_page_config(page_title="GESTION",page_icon="🌽",layout="wide")
else:
    st.set_page_config(page_title="GESTION",page_icon="🌽",layout="centered")

# ═══════════════════════════════════════════════════════════════════════════════
# Cerrar sesión
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    authenticator = st.session_state.authenticator
    st.markdown(f"""<span style="font-size: 18px;"> Hola, {st.session_state.get("username").title() if "username" in st.session_state else "Nada"} </span>""", unsafe_allow_html=True)
    authenticator.logout("Cerrar sesión", "sidebar")
    if st.session_state.get("authentication_status") is None:
        st.stop()
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# Filtros y buscador
# ═══════════════════════════════════════════════════════════════════════════════
import pandas as pd
import glob

archivo = glob.glob("*.xlsx")

try:
    st.title("Bienvenido al portal de Gestión")
    st.divider() # Una línea sutil para separar el contenido
    # 2. Leer el archivo Excel en un DataFrame de pandas
    df = pd.read_excel(archivo[0])

    nombres = df["Nombre del Acreditado"].unique()
    print(nombres)
    
    col1, col2 = st.columns([1,3])
    with col1:
        nombre_busqueda = st.multiselect("Seleccione Nombre del Acreditado",nombres)

    df[df["Nombre del Acreditado"].isin(nombre_busqueda)]

except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{archivo}' en esta carpeta.")

with st.expander("Información Legal y de Privacidad"):
    st.markdown(f"""
    **Aviso de Uso Interno e Informativo**  
    Esta plataforma es una herramienta de consulta exclusiva para el personal autorizado del Gobierno. Desarrollada por el Área de Estadística y Actualización, los resultados presentados son de carácter estrictamente informativo y no constituyen documentos oficiales, resoluciones ni actos administrativos vinculantes.<br> <br>
    Este software es de código abierto distribuido bajo la Licencia Apache 2.0. - Área de Estadística y Actualización.<br>
    {st.secrets["password"] if "password" in st.secrets else "Nada"}
    """, unsafe_allow_html=True)
