import streamlit as st
from datetime import date
import pandas as pd
from supabase import create_client, Client
import json
from login import to_plain_dict

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN INICIAL 
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.get("authentication_status"):
    st.set_page_config(
    page_title="GESTION",
    page_icon="📊",
    layout="wide",  # Aprovecha todo el ancho de la pantalla
    initial_sidebar_state="collapsed"
)

else:
    st.stop()
    st.set_page_config(
    page_title="GESTION",
    page_icon="📊",
    layout="centered",  # Aprovecha todo el ancho de la pantalla
    initial_sidebar_state="collapsed"
    )

st.markdown("""
    <style>
        /* Quitar el menú superior por defecto de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Personalizar tarjetas de métricas */
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #1E3A8A; /* Azul corporativo */
        }
        div[data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            color: #4B5563;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Contenedores visuales tipo tarjeta */
        .card {
            background-color: #F9FAFB;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 1px solid #E5E7EB;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* 1. Fondo de los chips seleccionados (Color Corporativo / Azul Financiero) */
        span[data-baseweb="tag"] {
            background-color: #0F172A !important; /* Azul Marino Obscuro Minimalista */
            color: #FFFFFF !important;            /* Texto Blanco */
            border-radius: 4px !important;        /* Esquinas más rectas y formales */
            padding: 4px 8px !important;
            font-weight: 500 !important;
        }
        
        /* Icono de cerrar (X) dentro de los chips del multiselect */
        span[data-baseweb="tag"] svg {
            fill: #94A3B8 !important;             /* Gris suave para la X */
        }
        span[data-baseweb="tag"] svg:hover {
            fill: #EF4444 !important;             /* Rojo sutil solo al pasar el cursor */
        }

        /* 2. Caja contenedora del selector (Estado Reposo) */
        div[data-baseweb="select"] > div {
            border: 1px solid #E2E8F0 !important; /* Borde ultra delgado y gris claro */
            background-color: #FFFFFF !important; /* Fondo blanco limpio */
            border-radius: 6px !important;
            box-shadow: none !important;          /* Sin sombras pesadas */
        }

        /* 3. Comportamiento al hacer clic o pasar el mouse (Enfoque) */
        div[data-baseweb="select"]:focus-within > div,
        div[data-baseweb="select"]:hover > div {
            border-color: #B45309 !important;     /* Borde Dorado Champagne/Oro Viejo */
        }

        /* 4. Título del componente (Label) */
        label[data-testid="stWidgetLabel"] p {
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            color: #475569 !important;            /* Gris pizarra elegante */
            text-transform: uppercase;            /* Aspecto formal */
            letter-spacing: 0.5px;
        }
    </style>
""", unsafe_allow_html=True)
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
@st.cache_data(ttl=3600*12)#En 6 horas borra la cache
def consultar_base_cacheada():
    URL = to_plain_dict(st.secrets["supabase"]["URL"])
    KEY = to_plain_dict(st.secrets["supabase"]["KEY"])
    supabase: Client = create_client(URL,KEY)
    data = supabase.table("base").select("*").execute().data
    return pd.DataFrame(data)

try:
    st.title("Bienvenido al portal de Gestión")
    st.divider() # Una línea sutil para separar el contenido
    # 2. Leer el archivo Excel en un DataFrame de pandas
    # print(data)
    df = consultar_base_cacheada()
    nombres = df["Nombre del Acreditado"].unique() if "Nombre del Acreditado" in df.columns else None
    col1, col2 = st.columns([2,3])
    with col1:
        nombre_busqueda = st.multiselect("Seleccione Nombre del Acreditado",nombres)
    df[df["Nombre del Acreditado"].isin(nombre_busqueda)] if "Nombre del Acreditado" in df.columns else None
    if st.button("🔄 Obtener datos recientes"):
        st.cache_data.clear() # Borra TODA la caché de la aplicación
        st.rerun()      

except FileNotFoundError:
    print(f"Error: No se encontró la base")
