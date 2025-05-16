from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import requests
from PIL import Image
from io import BytesIO
import base64

openai.api_key = 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

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '')
    media_url = request.values.get('MediaUrl0', '')

    if media_url:
        # Baixa a imagem
        response = requests.get(media_url)
        img_bytes = BytesIO(response.content)
        base64_image = base64.b64encode(img_bytes.read()).decode("utf-8")

        # Chamada ao ChatGPT com visão
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "Você é um artista que transforma fotos em desenhos para colorir."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Pegue esta foto e faça virar um desenho para colorir igual de livros para colorir. As linhas são pretas e bem definidas com praços simples, desenho fofo tipo dos livros de crianças. Não pode ter sombras nem cores. Não pode ter elementos na imagem que não estavam na imagem original. Mantenha os principais elementos da foto, como posição, poses apenas simplifique os detalhes complexos.
724
Se houver pessoas em volta desenhe de forma amigável e arredondada. gere a imagem no estilo livro para colorir."}, 
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        # Pega a resposta do GPT
        reply = MessagingResponse()
        reply.message("Aqui está o seu desenho! (essa parte deve ser adaptada para enviar imagem)")
        return str(reply)

    else:
        reply = MessagingResponse()
        reply.message("Envie uma foto para que eu possa transformá-la em um desenho para colorir!")
        return str(reply)

if __name__ == "__main__":
    app.run(debug=True)
