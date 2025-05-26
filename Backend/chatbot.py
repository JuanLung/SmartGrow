from openai import OpenAI

def consultaIA(datos):
    #ia="deepseek/deepseek-chat-v3-0324:free"
    ia = "google/gemini-2.0-flash-exp:free"
    empresa = "AgroEj"
    cultivo = "tomate"
    tamaño = "2"
    necesidad = "falta de agua"
    clima = datos
    tec = "sistema de riego por goteo, sensores de monitoreo"
    prod = "ImportFert Nutriente foliar, TecAgro sistema de riego por goteo, InsectFe insecticida."

    prompt = (
        f"Hola, actua como experto en agricultura. La empresa {empresa} se especializa en el cultivo de {cultivo}, "
        f"cuenta con {tamaño} hectarea de campo. Su principal necesidad es {necesidad}. "
        f"La empresa cuenta con las siguientes tecnologías implementadas en su cultivo: {tec}. "
        f"Necesito que realices una recomendación en base a su necesidad e información proporcionada, teniendo en cuenta los siguientes datos de clima en formato json: "
        f"{clima}. El mensaje lo vas a redactar de la siguiente forma: Infomación del clima, recomendación en base al clima especializado a su necesidad, sugerencias adicionales, producto recomendado. "
        f"Cada uno debe ser un parrafo de máximo 300 caracteres con un titulo. La información de clima debe ser mostrada en una pequeña tabla con datos relevantes, escribe el parametro y su valor, no escribas titulos de tabla. "
        f"La sección de recomendación y la sección de sugerencias realizalas en formato de lista. "
        f"Asegurate que los datos de clima proporcionados sean los mismos para el usuario. "
        f"Considera las tecnologías con las que cuenta la empresa y adapta tus recomendaciones a ellas, optimizando su funcionamiento. "
        f"Inicia siempre el mensaje con la siguiente descripción: Alerta de clima para <nombre>. No saludes ni escribas nada al inicio. "
        f"Si, y solo si la recomendación realizada abarca temas relacionados recomienda alguno de los siguientes productos al usuario: {prod}."
    )

    try:
        cliente = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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"
        )

        completion = cliente.chat.completions.create(
            model= ia,
            messages=[{"role": "user", "content": prompt}]
        )

        if completion and completion.choices:
            respuesta = completion.choices[0].message.content
            print(respuesta)
            return str(respuesta)
        else:
            print("⚠️ No se recibió respuesta válida de la IA.")
            return "La IA no pudo generar una respuesta en este momento."

    except Exception as e:
        print(f"❌ Error al consultar la IA: {e}")
        return f"Error: {e}"
