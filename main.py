from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI  # Importa o novo cliente
import requests

openai_api_key = "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"

app = Flask(__name__)

client = OpenAI(api_key=openai_api_key)  # Cria cliente OpenAI

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '')
    media_url = request.values.get('MediaUrl0', '')

    resp = MessagingResponse()

    if media_url:
        try:
            messages = [
                {
                    "role": "system",
                    "content": "Você é um artista que transforma fotos em desenhos para colorir."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": (
                            "Pegue esta foto e faça virar um desenho para colorir igual de livros para colorir. As linhas são pretas e bem definidas com traços simples, desenho fofo tipo dos livros de crianças. Não pode ter sombras nem cores. Não pode ter elementos na imagem que não estavam na imagem original. Mantenha os principais elementos da foto, como posição, poses, apenas simplifique os detalhes complexos. Se houver pessoas em volta desenhe de forma amigável e arredondada. Gere a imagem no estilo livro para colorir."
                        )},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": media_url
                            }
                        }
                    ]
                }
            ]

            completion = client.chat.completions.create(
                model="gpt-4o-mini",  # ou "gpt-4-vision-preview" se tiver acesso
                messages=messages,
                max_tokens=1000
            )

            resposta_texto = completion.choices[0].message.content.strip()

            resp.message(f"Aqui está o seu desenho (descrição): {resposta_texto}")

        except Exception as e:
            resp.message(f"Desculpe, ocorreu um erro ao processar a imagem: {str(e)}")

    else:
        resp.message("Envie uma foto para que eu possa transformá-la em um desenho para colorir!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
