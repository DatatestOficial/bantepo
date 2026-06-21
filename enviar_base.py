import os
import glob
from supabase import create_client, Client
import pandas as pd
import json
# Eliminar
# librerias openpyxl pandas supabase pyinstaller 
# pyinstaller --onefile --clean --exclude-module=unittest --exclude-module=pydoc enviar_base.py


URL="https://thjbgxerjgnhctvdyosm.supabase.co"
KEY="sb_publishable_GfipS_hT0h7ph5WzYpOYqg_CH1lVir9"
# Crear la conexión
supabase: Client = create_client(URL,KEY)

def df_to_supabase(df: pd.DataFrame, tabla: str):
    # MAPEO simplificado: agregamos '<M8[us]' para que detecte tu tipo de fecha exacto
    MAPEO = {"object": "TEXT", "int64": "BIGINT", "float64": "NUMERIC", "bool": "BOOLEAN", "<M8[us]": "TIMESTAMP WITH TIME ZONE"}
    columnas = ", ".join([f'"{col}" {MAPEO.get(str(dt), "TEXT")}' for col, dt in zip(df.columns, df.dtypes)])
    sql = f'DROP TABLE IF EXISTS "{tabla}"; CREATE TABLE "{tabla}" (id SERIAL PRIMARY KEY, {columnas});'
    supabase.rpc("crear_tabla", {"query_sql": sql}).execute()
    # Convertir a JSON string con Pandas (esto transforma automáticamente NaN y fechas a formato JSON válido)
    # y luego lo volvemos a leer como un diccionario limpio de Python
    datos_limpios = json.loads(df.to_json(orient="records", date_format="iso"))
    # Enviar el lote limpio a Supabase
    supabase.table(tabla).insert(datos_limpios).execute()# --- FUNCIÓN DEFINITIVA: CREA Y ENVÍA ---

# --- FLUJO AUTOMÁTICO AL DAR DOBLE CLIC ---
if __name__ == "__main__":
    print("Buscando archivos Excel en la carpeta actual...")
    archivos = glob.glob("*.xlsx")
    
    if archivos:
        primer_archivo = archivos[0]
        print(f"Leyendo: {primer_archivo}")
        
        try:
            df_excel = pd.read_excel(primer_archivo)
            nombre_tabla = "base"
            
            print("Enviando base de datos...")
            df_to_supabase(df_excel, nombre_tabla)
            
            print(f"¡Éxito total! Tabla '{nombre_tabla}' actualizada.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
    else:
        print("Error: No se encontró ningún archivo .xlsx en esta carpeta.")
        
    # Mantener abierta la ventana de la consola para ver el mensaje de éxito
    input("\nPresiona Enter para salir...")
