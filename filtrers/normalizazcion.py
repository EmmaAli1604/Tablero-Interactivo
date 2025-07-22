from rapidfuzz import fuzz #Hay que instalar rapidfuzz
import pandas as pd

def normalizacion(nombres):
    # Umbral de similitud (ajustable)
    UMBRAL = 80

    # Diccionario para almacenar el mapeo final
    mapeo = {}

    # Lista para los nombres ya "normalizados"
    nombres_normalizados = []

    for nombre in nombres:
        encontrado = False
        for ref in nombres_normalizados:
            if fuzz.token_sort_ratio(nombre.lower(), ref.lower()) >= UMBRAL:
                mapeo[nombre] = ref  # Mapear al primero que se encontró
                encontrado = True
                break
    if not encontrado:
        mapeo[nombre] = nombre  # Es nuevo, se convierte en su propia referencia
        nombres_normalizados.append(nombre)

    # Aplicar mapeo a la serie original
    nombres_normalizados_serie = nombres.map(mapeo)

    print(nombres_normalizados_serie)
    
df['fecha_normalizada'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce')
print(df['fecha_normalizada'].dtype)
df['fecha_formateada'] = df['fecha_normalizada'].dt.strftime('%d/%m/%Y') #es para mostrar un formato es string