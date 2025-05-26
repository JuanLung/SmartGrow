#include <DHT.h> // Libreria para sensor de humedad y temperatura
#include <BH1750.h> //Libreria para sensor de iluminación
#include <Wire.h>  //Librería para poder activar la comunicación por el protocolo I2C entre el BH1750 y el arduino

// Definimos el pin digital donde se conecta el sensor de temperatura y humedad
#define DHTPIN 2
#define DHTTYPE DHT11 // Dependiendo del tipo de sensor
DHT dht(DHTPIN, DHTTYPE);// Inicializamos el sensor DHT11
//Definimos pin para sensor de lluvia
int pinSensorLluvia = A0;
// Definimos el tipo de sensor de luz
BH1750 Luxometro;

void setup() {
  Serial.begin(9600);
  delay(5000);
  dht.begin();
  Wire.begin();
  Luxometro.begin();
  delay(5000);
}

void loop() {
  // Leemos la humedad relativa
  float humedad = dht.readHumidity();
  // Leemos la temperatura en grados centígrados (por defecto)
  float temperatura = dht.readTemperature();
  // Leemos sensor pluviometro
  int lluvia = analogRead(pinSensorLluvia);
  // Leemos sensor de luz
  uint16_t luz = Luxometro.readLightLevel();
  
  Serial.println(String(temperatura) + "," + String(humedad) + "," + String(lluvia)+ "," + String(luz));
  delay(5000);
}