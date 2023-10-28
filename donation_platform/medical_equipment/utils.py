from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch

# Cargar el modelo preentrenado y el tokenizador
modelo = BertForSequenceClassification.from_pretrained('bert-base-uncased')
tokenizador = BertTokenizer.from_pretrained('bert-base-uncased')

def asignar_categoria(titulo, descripcion):
    # Combinar título y descripción para un análisis más completo
    texto_completo = titulo + ' ' + descripcion

    # Tokenizar el texto
    tokens = tokenizador(texto_completo, return_tensors='pt')

    # Obtener las predicciones del modelo
    with torch.no_grad():
        logits = modelo(**tokens).logits

    # Aplicar la función softmax para obtener probabilidades
    probabilidades = softmax(logits, dim=1).squeeze()

    # Obtener la categoría predicha
    categoria_predicha = modelo.config.id2label[torch.argmax(probabilidades).item()]

    return categoria_predicha

