import time
import pandas as pd
import os
import requests
from datetime import datetime
import json

# URL del servidor en PythonAnywhere (reemplaza "tuusuario" con tu nombre de usuario)
PYTHONANYWHERE_URL = "https://tuusuario.pythonanywhere.com/api/sensor"

# Nombre del archivo CSV que Arduino.py está generando
CSV_FILE = "Data\\clima_local.csv"


# Función para enviar datos al servidor PythonAnywhere
def enviar_datos_servidor(datos):
    try:
        response = requests.post(PYTHONANYWHERE_URL, json=datos)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Datos enviados correctamente a PythonAnywhere")
        else:
            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] Error al enviar datos: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error de conexión con PythonAnywhere: {e}")


def main():
    print("=== Sincronizador de datos CSV a PythonAnywhere ===")
    print(f"Monitorizando archivo: {CSV_FILE}")
    print(f"Enviando datos a: {PYTHONANYWHERE_URL}")
    print("Presiona Ctrl+C para detener\n")

    # Guarda la última fila procesada
    last_processed_size = 0
    last_processed_rows = 0

    while True:
        try:
            # Verificar si el archivo existe
            if os.path.exists(CSV_FILE):
                # Obtener el tamaño del archivo
                current_size = os.path.getsize(CSV_FILE)

                # Si el archivo ha cambiado desde la última lectura
                if current_size != last_processed_size:
                    # Leer el archivo CSV
                    df = pd.read_csv(CSV_FILE)
                    current_rows = len(df)

                    # Si hay nuevas filas
                    if current_rows > last_processed_rows:
                        # Obtener solo las nuevas filas
                        new_rows = df.iloc[last_processed_rows:current_rows]

                        # Enviar cada nueva fila al servidor
                        for _, row in new_rows.iterrows():
                            # Convertir la fila a un diccionario
                            data = row.to_dict()

                            # Enviar los datos al servidor
                            enviar_datos_servidor(data)
                            print(f"Enviados datos: Temp={data['Temperatura']:.1f}°C, Hum={data['Humedad']:.1f}%")

                        # Actualizar contadores
                        last_processed_size = current_size
                        last_processed_rows = current_rows

                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] Procesadas {len(new_rows)} nuevas filas. Total: {current_rows}")

            # Esperar antes de la siguiente verificación
            time.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()