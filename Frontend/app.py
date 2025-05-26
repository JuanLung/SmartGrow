from flask import Flask, jsonify, request, render_template, send_from_directory
import pandas as pd
import os
import json
from datetime import datetime, timedelta
import requests
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Configuración de directorios
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Crear directorio de datos si no existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Ruta al CSV de datos
CLIMA_CSV = os.path.join(DATA_DIR, 'clima_local.csv')


def calcular_lluvia(volts):
    if volts > 800:
        return "Sin lluvia"
    elif volts > 600 and volts < 800:
        return "Llovizna ligera"
    elif volts > 400 and volts < 600:
        return "Poca lluvia"
    elif volts > 200 and volts < 400:
        return "Lluvia moderada"
    else:
        return "Lluvia intensa"


def calcular_luz(lumens):
    if lumens < 50:
        return "Noche"
    elif lumens > 50 and lumens < 600:
        return "Nublado"
    else:
        return "Soleado"


# Función para crear un registro de prueba (para cuando no hay Arduino conectado)
def crear_registro_prueba():
    import random

    # Valores aleatorios para simulación
    temperatura = round(random.uniform(18.0, 30.0), 1)
    humedad = random.randint(40, 90)
    lluvia = random.randint(0, 1000)
    luz = random.randint(10, 900)
    viento = round(random.uniform(0, 25), 1)

    fecha_actual = datetime.now().date().isoformat()
    hora_actual = datetime.now().time().strftime("%H:%M:%S")

    return {
        "Fecha": fecha_actual,
        "Hora": hora_actual,
        "Temperatura": temperatura,
        "Humedad": humedad,
        "Lluvia": lluvia,
        "Luz": luz,
        "Viento": viento
    }


# Función para consultar la IA (simulada para este ejemplo)
def consulta_ia(datos):
    recomendacion = "Basado en las condiciones actuales: "

    if datos["Temperatura"] > 28:
        recomendacion += "La temperatura es alta, considera aumentar el riego. "
    elif datos["Temperatura"] < 15:
        recomendacion += "La temperatura es baja, protege los cultivos sensibles al frío. "

    if datos["Humedad"] > 80:
        recomendacion += "La humedad es elevada, vigila posibles enfermedades fúngicas. "
    elif datos["Humedad"] < 40:
        recomendacion += "La humedad es baja, considera aumentar el riego. "

    if calcular_lluvia(datos["Lluvia"]) != "Sin lluvia":
        recomendacion += "Se detecta lluvia, considera proteger cultivos sensibles. "

    if calcular_luz(datos["Luz"]) == "Soleado":
        recomendacion += "Día soleado, asegúrate de que los cultivos tengan suficiente agua. "

    return recomendacion


# Ruta para servir archivos estáticos
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)


# Ruta principal que redirige a INDEX.html
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'INDEX.html')


# API para obtener datos del último registro
@app.route('/api/sensores/ultimo', methods=['GET'])
def ultimo_registro():
    try:
        # Comprobar si existe el archivo CSV
        if os.path.exists(CLIMA_CSV):
            # Leer el CSV y obtener el último registro
            df = pd.read_csv(CLIMA_CSV)
            if not df.empty:
                ultimo = df.iloc[-1].to_dict()

                # Añadir estados interpretados
                ultimo['EstadoLluvia'] = calcular_lluvia(ultimo['Lluvia'])
                ultimo['EstadoLuz'] = calcular_luz(ultimo['Luz'])
                ultimo['Recomendacion'] = consulta_ia(ultimo)

                return jsonify({"success": True, "data": ultimo})

        # Si no hay datos o archivo, generar datos de prueba
        registro_prueba = crear_registro_prueba()
        registro_prueba['EstadoLluvia'] = calcular_lluvia(registro_prueba['Lluvia'])
        registro_prueba['EstadoLuz'] = calcular_luz(registro_prueba['Luz'])
        registro_prueba['Recomendacion'] = consulta_ia(registro_prueba)

        # Si no existe el archivo o directorio, crear un nuevo CSV con el registro de prueba
        if not os.path.exists(CLIMA_CSV):
            df_nuevo = pd.DataFrame([registro_prueba])
            df_nuevo.to_csv(CLIMA_CSV, index=False)

        return jsonify({"success": True, "data": registro_prueba, "note": "Datos simulados"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# API para obtener datos entre fechas
@app.route('/api/sensores/fechas', methods=['GET'])
def datos_por_rango_fechas():
    try:
        startDate = request.args.get('start')
        endDate = request.args.get('end')

        if not startDate or not endDate:
            return jsonify({"success": False, "error": "Se requieren fechas de inicio y fin"}), 400

        # Comprobar si existe el archivo CSV
        if os.path.exists(CLIMA_CSV):
            # Leer el CSV y filtrar por rango de fechas
            df = pd.read_csv(CLIMA_CSV)
            df_fechas = df[(df['Fecha'] >= startDate) & (df['Fecha'] <= endDate)]

            if not df_fechas.empty:
                # Convertir a lista de diccionarios
                registros = df_fechas.to_dict('records')

                # Añadir estados interpretados
                for registro in registros:
                    registro['EstadoLluvia'] = calcular_lluvia(registro['Lluvia'])
                    registro['EstadoLuz'] = calcular_luz(registro['Luz'])

                return jsonify({"success": True, "data": registros})

        # Si no hay datos para ese rango, generar datos de ejemplo
        import random
        registros_ejemplo = []

        start_date = datetime.strptime(startDate, '%Y-%m-%d')
        end_date = datetime.strptime(endDate, '%Y-%m-%d')
        date_range = (end_date - start_date).days + 1

        for i in range(date_range):
            current_date = start_date + timedelta(days=i)
            fecha = current_date.strftime('%Y-%m-%d')

            # Generar datos para diferentes horas del día
            for hour in [0, 4, 8, 12, 16, 20]:
                registro = crear_registro_prueba()
                registro['Fecha'] = fecha
                registro['Hora'] = f"{hour:02d}:00:00"
                registro['EstadoLluvia'] = calcular_lluvia(registro['Lluvia'])
                registro['EstadoLuz'] = calcular_luz(registro['Luz'])
                registros_ejemplo.append(registro)

        return jsonify({"success": True, "data": registros_ejemplo, "note": "Datos simulados"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# API para registrar datos de sensores (para recibir datos de Arduino o simulador)
@app.route('/api/sensores/registrar', methods=['POST'])
def registrar_datos():
    try:
        # Obtener datos del cuerpo de la petición
        datos = request.json

        # Verificar datos mínimos requeridos
        campos_requeridos = ['Temperatura', 'Humedad', 'Lluvia', 'Luz', 'Viento']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({"success": False, "error": f"Falta el campo {campo}"}), 400

        # Añadir fecha y hora si no están presentes
        if 'Fecha' not in datos:
            datos['Fecha'] = datetime.now().date().isoformat()
        if 'Hora' not in datos:
            datos['Hora'] = datetime.now().time().strftime("%H:%M:%S")

        # Añadir a CSV
        df_nuevo = pd.DataFrame([datos])

        if os.path.exists(CLIMA_CSV):
            df = pd.read_csv(CLIMA_CSV)
            df = pd.concat([df, df_nuevo], ignore_index=True)
            df.to_csv(CLIMA_CSV, index=False)
        else:
            df_nuevo.to_csv(CLIMA_CSV, index=False)

        return jsonify({"success": True, "message": "Datos registrados correctamente"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Simulador para generar datos cuando no hay Arduino conectado
def simulador_arduino():
    import time
    import threading

    def generar_datos():
        while True:
            try:
                # Crear registro simulado
                registro = crear_registro_prueba()

                # Guardar en CSV
                df_nuevo = pd.DataFrame([registro])

                if os.path.exists(CLIMA_CSV):
                    df = pd.read_csv(CLIMA_CSV)
                    df = pd.concat([df, df_nuevo], ignore_index=True)
                    # Mantener sólo los últimos 1000 registros para no crecer indefinidamente
                    if len(df) > 1000:
                        df = df.tail(1000)
                    df.to_csv(CLIMA_CSV, index=False)
                else:
                    df_nuevo.to_csv(CLIMA_CSV, index=False)

                print(f"Datos simulados generados: {registro}")

                # Esperar 5 minutos antes de generar el siguiente registro
                time.sleep(300)
            except Exception as e:
                print(f"Error en simulador: {e}")
                time.sleep(60)  # Si hay error, esperar un minuto y reintentar

    # Iniciar el simulador en un hilo separado
    thread = threading.Thread(target=generar_datos, daemon=True)
    thread.start()
    print("Simulador de Arduino iniciado en segundo plano")


# Iniciar simulador si estamos en entorno de desarrollo o PythonAnywhere
if __name__ == '__main__' or 'PYTHONANYWHERE_DOMAIN' in os.environ:
    # Iniciar simulador solo si no existe el archivo de configuración que indique Arduino real
    if not os.path.exists(os.path.join(BASE_DIR, 'arduino_real.cfg')):
        simulador_arduino()

    # Si estamos en PythonAnywhere, la aplicación ya se ejecutará por WSGI
    if __name__ == '__main__':
        app.run(debug=True, port=5000)