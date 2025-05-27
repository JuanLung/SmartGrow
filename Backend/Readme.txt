--- Descripción de Backend ---
Alumno: Jorge Alan Urias Guluarte 

Esta sección cuenta con tres archivos de python para la extracción de datos y configuración de chatbot, dos csv donde se almacenan los
datos recabados y un archivo tipo .ino que es una extensión utilizada en entornos de desarrollo con arduino. 
Para ejecutar este código correctamente primero se debe de contar con un dispositivo arduino, en este caso se cuenta con un Arduino UNO,
además de los sensores correspondientes (DHT11, BH1750, MD-MHRD). 

1. El primer paso es compilar y almacenar el código dentro del arduino, una vez instalado se mantiene la conexión por puerto serial. Este
archivo lo que hace es inicializar los sensores utilizados y mediante un loop infinito captura la entrada de los sensores cada 10
segundos, guarda esas entradas como cadenas de texto, las concatena y manda el arreglo por puerto serial.

2. Como siguiente paso se debe de ejecutar el código Arduino.py y este comenzará con la extracción de datos mediante la torre controlada
por arduino. Es indispensable corroborar que el puerto de comunicación sea el mismo donde está conectado el arduino. Una vez se ejecuta
este código lo que hace es inicializar la comunicación por puerto serial, luego captar los datos enviados por el arduino y procesar la
cadena de texto para convertirla en entradas a un dataframe el cual se exporta como un archivo CSV llamado clima_local.csv. Además se
establece la comunicación con el chatbot alojado en Telegram mandando alertas cuando se detecten ciertos parámetros configurados, estas
alertas contienen los datos climáticos obtenidos de la torre y la recomendación generada por el modelo de IA.
    2.1 Una vez se recibe un dato por puerto serial y se procese, también se realiza una consulta por medio de IA con los datos
utilizados. Para ello se hace uso del archivo chatbot.py, el cual está importado dentro del código para ser usado como una especie de
librería. En esta parte se realiza la configuración del modelo de inteligencia artificial utilizado. Este modelo es una versión gratuita
la cuál se puede encontrar en la plataforma de Openrouter y acceder a cualquiera de sus modelos gratis por medio de un token. El código
tiene como entrada una cadena de valores lo cuales son los datos recabados por Arduino, además de los datos generales de la empresa como:
nombre, necesidad, hectáreas, cultivo, tecnologías utilizadas. 
    2.2 Una vez se ingresan estas variables se crea un prompt especializado utilizando los datos proporcionados, en este prompt se le pide
al modelo realice recomendaciones y sugerencias en base a la información proporcionada por el usuario y los datos recabados por arduino.
De esta manera se obtiene una recomendación totalmente personalizada y adaptada al usuario. Se manda la consulta a la IA y se regresa la
respuesta al usuario. 

3. El último código utilizado en el backend es ExtraccionClima.py, este archivo se ejecuta de manera independiente. Se utiliza para
recopilar datos climáticos de fuentes externas por medio de una API, en este caso la API de OpenWeatherMap. Este archivo lo que hace es
configurar la API utilizada, selecciona la ubicación del usuario y se realizan consultas a la APi mandando las coordenadas ingresadas. Se
captan los datos y se procesan para ser almacenados en un archivo CSV llamado clima abierto.csv.

