from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse
import requests
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

def photo_to_sketch(image_url):
    # Baixa a imagem
    response = requests.get(image_url)
    img = np.array(Image.open(BytesIO(response.content)).convert('RGB'))

    # Converte para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Inverte a imagem
    inv = 255 - gray

    # Aplica desfoque gaussiano
    blur = cv2.GaussianBlur(inv, (21, 21), 0)

    # Divide a imagem original pelo inverso do desfoque para efeito sketch
    sketch = cv2.divide(gray, 255 - blur, scale=256)

    # Converte para PIL Image para facilitar envio
    pil_sketch = Image.fromarray(sketch)

    # Salva a imagem em bytes
    img_byte_arr = BytesIO()
    pil_sketch.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    return img_byte_arr

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    media_url = request.values.get('MediaUrl0', '')

    resp = MessagingResponse()

    if media_url:
        try:
            # Converte a imagem para sketch
            sketch_img = photo_to_sketch(media_url)

            # Salva temporariamente para enviar pelo Twilio
            temp_filename = "sketch.jpg"
            with open(temp_filename, 'wb') as f:
                f.write(sketch_img.read())

            # Reseta o ponteiro para leitura no próximo uso (se quiser usar BytesIO diretamente)
            sketch_img.seek(0)

            # Envia a imagem de volta via Twilio (WhatsApp)
            message = resp.message("Aqui está seu desenho para colorir!")
            message.media(f"https://YOUR_DOMAIN/{temp_filename}")

            # Opcional: apagar arquivo depois (se for server com espaço limitado)
            # os.remove(temp_filename)

        except Exception as e:
            resp.message(f"Desculpe, ocorreu um erro ao processar a imagem: {str(e)}")

    else:
        resp.message("Envie uma foto para que eu possa transformá-la em um desenho para colorir!")

    return str(resp)

# Endpoint para servir a imagem salva
@app.route('/sketch.jpg')
def serve_sketch():
    return send_file("sketch.jpg", mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True)
