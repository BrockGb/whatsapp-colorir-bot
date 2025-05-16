from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import requests
from PIL import Image
from io import BytesIO
import base64

openai.api_key = "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"

app = Flask(__name__)

import traceback

@app.route("/bot", methods=["POST"])
def bot():
    try:
        incoming_msg = request.values.get('Body', '')
        media_url = request.values.get('MediaUrl0', '')

        print("Mensagem recebida:", incoming_msg)
        print("URL da imagem:", media_url)

        if media_url:
            response = requests.get(media_url)
            print("Status da imagem:", response.status_code)
            if response.status_code != 200:
                raise Exception("Erro ao baixar imagem")

            img_bytes = BytesIO(response.content)
            base64_image = base64.b64encode(img_bytes.read()).decode("utf-8")

            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {"role": "system", "content": "Você é um artista que transforma fotos em desenhos para colorir."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Transforme essa imagem num desenho de livro de colorir"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=1000
            )

            print("Resposta da OpenAI:", response)

            reply = MessagingResponse()
            reply.message("Imagem processada com sucesso!")
            return str(reply)
        else:
            reply = MessagingResponse()
            reply.message("Envie uma imagem para processar.")
            return str(reply)

    except Exception as e:
        print("Erro interno:", str(e))
        traceback.print_exc()
        return "Erro interno no servidor", 500


if __name__ == "__main__":
    app.run(debug=True)
