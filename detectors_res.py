import logging
from wit import Wit
from textblob import TextBlob

# Configurar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Puedes ajustar el nivel según tus necesidades

# Configurar un manejador para imprimir los mensajes de registro en la consola
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

access_token = 'CDCAER5NSNNBBJHC3WHQVOHHOZTGLTLI'
client = Wit(access_token)

# Wit.ai para analizar el texto con el modelo entrenado que detecta intenciones de insultos, ilegal o adecuado
def analizar_texto(texto):
    try:
        logger.debug("Enviando mensaje a Wit.ai: %s", texto)
        respuesta = client.message(texto)
        logger.debug("Respuesta de Wit.ai: %s", respuesta)

        if 'intents' in respuesta and 'insulto' in respuesta['intents']:
            return 'ofensivo'
        elif 'intents' in respuesta and 'ilegal' in respuesta['intents']:
            return 'ofensivo'
        else:
            return 'no_ofensivo'

    except Exception as e:
        logger.error("Error al procesar la solicitud a Wit.ai: %s", e)
        return 'error'

# TextBlob para analizar sentimientos
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    sentimiento = blob.sentiment.polarity
    return sentimiento

# Ejemplo de uso
#texto_prueba = "hola hijo de puta"
#resultado_wit = analizar_texto(texto_prueba)
#resultado_sentimiento = analizar_sentimiento(texto_prueba)

#logger.debug("Resultado Wit.ai: %s", resultado_wit)
#logger.debug("Resultado Sentimiento: %s", resultado_sentimiento)

