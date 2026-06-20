import pandas as pd
import glob

archivo = glob.glob("*.xlsx")

try:
    # 2. Leer el archivo Excel en un DataFrame de pandas
    df = pd.read_excel(archivo[0])
    
    # 3. Mostrar las primeras filas en la consola para verificar que se cargó bien
    print("¡Archivo importado con éxito!")
    print(df.head())

except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{archivo}' en esta carpeta.")
    print("Verifica que el nombre sea exacto y que esté guardado junto a este script.")


from supabase import create_client, Client

# Configura tus credenciales (reemplaza con tus datos reales)
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "tu-api-key-anon-o-service-role"

# Crear el cliente de conexión
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
