from wit import Wit
from textblob import TextBlob

access_token = 'CDCAER5NSNNBBJHC3WHQVOHHOZTGLTLI'
client = Wit(access_token)

#Wit.ai para analizar el texto con el modelo entrenado que detecta intenciones de insultos, ilegal o adecuado
def analizar_texto(texto):
    respuesta = client.message(texto)

    if 'insulto' in respuesta['intents']:
        return 'ofensivo'
    if 'ilegal' in respuesta['intents']:
        return 'ofensivo'
    else:
        return 'no_ofensivo'

#textblob para analizar sentimientos
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    sentimiento = blob.sentiment.polarity

    return sentimiento
