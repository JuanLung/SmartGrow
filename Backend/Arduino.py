import serial
import time
from datetime import datetime
import pandas as pd
import os
import asyncio
import telegram
from telegram.ext import ApplicationBuilder
from chatbot import consultaIA

def calcularLluvia(volts):
    if volts > 800:
        return "Sin lluvia"
    elif volts > 600 and volts < 800:
        return "Llovizna ligera"
    elif volts > 400 and volts < 600:
        return "Poca luvia"
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

def extraerDatos(cadena):  # Temperatura, Humedad, Lluvia, Luz, Viento
    valores = []
    dato = ""
    for x in cadena:
        if x != ",":
            dato += x
        else:
            valores.append(float(dato))
            dato = ""
    if dato:  # Para
        # capturar el último valor si no termina en coma
        valores.append(float(dato))
        valores.append(4)
        print(valores)
    return valores

def crearRegistro(cadena_datos):
    datos_base = cadena_datos
    fecha_actual = datetime.now().date().isoformat()
    hora_actual = datetime.now().time().strftime("%H:%M:%S")

    return {
        "Fecha": fecha_actual,
        "Hora": hora_actual,
        "Temperatura": datos_base[0],
        "Humedad": datos_base[1],
        "Lluvia": calcularLluvia(datos_base[2]),
        "Luz": calcularLuz(datos_base[3]),
        "Viento": datos_base[4]
    }


# Crear el DataFrame vacío con columnas definidas
df = pd.DataFrame(columns=["Fecha", "Hora", "Temperatura", "Humedad", "Lluvia", "Luz", "Viento"])
# Crear variable para arduino en puerto serial
arduino = serial.Serial('COM3', 9600)
time.sleep(1)

TOKEN = "7871696620:AAFKCjn99O0AGy4RXiCYd5R2y7QSLnlCU2Y"
idchat = "6561790380"


# using telegram.Bot
async def send(chat, msg):
    await telegram.Bot(TOKEN).sendMessage(chat_id=chat, text=msg)

while True:
    sensor_data = arduino.readline().decode('ascii')
    lista = extraerDatos(sensor_data)
    nuevo_registro = crearRegistro(lista)
    df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
    df.to_csv('clima_local.csv', index=False)
    if nuevo_registro['Luz'] == "Soleado":
        asyncio.run(send(idchat, 'Cubre tu cultivo! Dia soleado.'))
        asyncio.run(send(idchat, consultaIA(nuevo_registro)))
    elif nuevo_registro['Lluvia'] != "Sin lluvia":
        asyncio.run(send(idchat, 'Cubre tu cultivo! Dia lluvioso.'))
        asyncio.run(send(idchat, consultaIA(nuevo_registro)))