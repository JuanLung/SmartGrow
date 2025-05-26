import requests
import pandas as pd
from datetime import datetime

key = "071e04e456103efab37559205e4f08c8"
lat ="31.860052374685505"
lon ="-116.58102543816265"
API = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat +"&lon="+ lon +"&appid="+ key

json1 = requests.get(API).json()
#print(datos_json)
#json1 = {'coord': {'lon': -116.581, 'lat': 31.8601}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 288.29, 'feels_like': 288.47, 'temp_min': 288.29, 'temp_max': 288.29, 'pressure': 1014, 'humidity': 100, 'sea_level': 1014, 'grnd_level': 983}, 'visibility': 10000, 'wind': {'speed': 1.33, 'deg': 12, 'gust': 1.59}, 'clouds': {'all': 48}, 'dt': 1746193240, 'sys': {'type': 2, 'id': 2001695, 'country': 'MX', 'sunrise': 1746190757, 'sunset': 1746239225}, 'timezone': -25200, 'id': 4006702, 'name': 'Ensenada', 'cod': 200}

df = pd.DataFrame(columns=["Fecha", "Hora", "Latitud", "Longitud", "Clima", "Temperatura", "Sensacion",
                           "Humedad","Temp_min","Temp_max","Viento","Ciudad"])

fecha_actual = datetime.now().date().isoformat()
hora_actual = datetime.now().time().strftime("%H:%M:%S")

registro = {
    "Fecha": fecha_actual,
    "Hora": hora_actual,
    "Latitud": json1['coord']['lat'],
    "Longitud": json1['coord']['lon'],
    "Clima": json1['weather'][0]['main'],
    "Temperatura": json1['main']['temp'],
    "Sensacion": json1['main']['feels_like'],
    "Humedad": json1['main']['humidity'],
    "Temp_min": json1['main']['temp_min'],
    "Temp_max": json1['main']['temp_max'],
    "Viento": json1['wind']['speed'],
    "Ciudad": json1['name']
}

df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
df.to_csv('clima_abierto.csv', index=False)
print(df)

