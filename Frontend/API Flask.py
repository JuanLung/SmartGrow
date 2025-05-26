from flask import Flask, request, jsonify, send_from_directory
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__, static_folder='static')

# Configuración
DATA_FOLDER = 'Data'
CSV_FILENAME = 'clima_local.csv'
CSV_PATH = os.path.join(DATA_FOLDER, CSV_FILENAME)

# Asegurar que el directorio de datos existe
os.makedirs(DATA_FOLDER, exist_ok=True)

# Crear el archivo CSV si no existe
if not os.path.exists(CSV_PATH):
    df = pd.DataFrame(columns=["Fecha", "Hora", "Temperatura", "Humedad", "Lluvia", "Luz", "Viento"])
    df.to_csv(CSV_PATH, index=False)


# Funciones auxiliares para calcular estados
def calcularLluvia(volts):
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


def calcularLuz(lumens):
    if lumens < 50:
        return "Noche"
    elif lumens > 50 and lumens < 600:
        return "Nublado"
    else:
        return "Soleado"


# Endpoint POST para recibir datos del Arduino
@app.route('/api/sensores', methods=['POST'])
def registrar_datos():
    try:
        # Obtener los datos del cuerpo de la petición
        datos = request.json

        # Validar que los datos contengan los campos necesarios
        campos_requeridos = ["Temperatura", "Humedad", "Lluvia", "Luz", "Viento"]
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'success': False,
                    'message': f'Falta el campo {campo} en los datos'
                }), 400

        # Añadir fecha y hora si no vienen en los datos
        if "Fecha" not in datos:
            datos["Fecha"] = datetime.now().date().isoformat()
        if "Hora" not in datos:
            datos["Hora"] = datetime.now().time().strftime("%H:%M:%S")

        # Leer el CSV existente
        df = pd.read_csv(CSV_PATH)

        # Añadir el nuevo registro
        df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)

        # Guardar el CSV actualizado
        df.to_csv(CSV_PATH, index=False)

        # Añadir interpretaciones para la respuesta
        respuesta = datos.copy()
        respuesta['EstadoLluvia'] = calcularLluvia(float(datos['Lluvia']))
        respuesta['EstadoLuz'] = calcularLuz(float(datos['Luz']))

        return jsonify({
            'success': True,
            'message': 'Datos registrados correctamente',
            'data': respuesta
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al registrar datos: {str(e)}'
        }), 500


# Endpoints GET para que DISPOSITIVOS.html pueda obtener los datos
@app.route('/api/sensores/ultimo', methods=['GET'])
def get_ultimo_registro():
    try:
        # Leer el CSV
        df = pd.read_csv(CSV_PATH)

        if df.empty:
            return jsonify({
                'success': False,
                'message': 'No hay datos registrados'
            }), 404

        # Obtener el último registro
        ultimo_registro = df.iloc[-1].to_dict()

        # Agregar interpretaciones
        ultimo_registro['EstadoLluvia'] = calcularLluvia(ultimo_registro['Lluvia'])
        ultimo_registro['EstadoLuz'] = calcularLuz(ultimo_registro['Luz'])

        return jsonify({
            'success': True,
            'data': ultimo_registro
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener datos: {str(e)}'
        }), 500


@app.route('/api/sensores/fechas', methods=['GET'])
def get_registros_por_fecha():
    try:
        start_date = request.args.get('start')
        end_date = request.args.get('end')

        if not start_date or not end_date:
            return jsonify({
                'success': False,
                'message': 'Se requieren las fechas de inicio y fin'
            }), 400

        # Leer el CSV
        df = pd.read_csv(CSV_PATH)

        if df.empty:
            return jsonify({
                'success': False,
                'message': 'No hay datos registrados'
            }), 404

        # Filtrar por fechas
        filtered_df = df[(df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)]

        if filtered_df.empty:
            return jsonify({
                'success': False,
                'message': 'No hay datos para el rango seleccionado'
            }), 404

        # Convertir a lista de diccionarios
        registros = filtered_df.to_dict('records')

        # Agregar interpretaciones a cada registro
        for registro in registros:
            registro['EstadoLluvia'] = calcularLluvia(registro['Lluvia'])
            registro['EstadoLuz'] = calcularLuz(registro['Luz'])

        return jsonify({
            'success': True,
            'data': registros
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener datos: {str(e)}'
        }), 500


# Configuración para servir archivos estáticos (como DISPOSITIVOS.html)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return send_from_directory('static', 'INDEX.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)