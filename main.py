from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import requests
from io import BytesIO

openai.api_key = "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"

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '')
    media_url = request.values.get('MediaUrl0', '')

    resp = MessagingResponse()

    if media_url:
        try:
            # Note: OpenAI GPT-4 Vision não aceita base64 embutido, precisa da URL pública da imagem.
            # Então enviamos a URL direta da imagem para o modelo.

            messages = [
                {
                    "role": "system",
                    "content": "Você é um artista que transforma fotos em desenhos para colorir."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": (
                            "Pegue esta foto e faça virar um desenho para colorir igual de livros para colorir. "
                            "As linhas são pretas e bem definidas com traços simples, desenho fofo tipo dos livros de crianças. "
                            "Não pode ter sombras nem cores. Não pode ter elementos na imagem que não estavam na imagem original. "
                            "Mantenha os principais elementos da foto, como posição, poses, apenas simplifique os detalhes complexos. "
                            "Se houver pessoas em volta desenhe de forma amigável e arredondada. Gere a imagem no estilo livro para colorir."
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

            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Ou "gpt-4-vision-preview" se disponível no seu acesso
                messages=messages,
                max_tokens=1000
            )

            # A resposta da API com visão pode incluir texto ou até links para imagens geradas.
            # Aqui vamos assumir que o texto da resposta está no primeiro choice.
            resposta_texto = completion.choices[0].message.content.strip()

            resp.message(f"Aqui está o seu desenho (descrição): {resposta_texto}")

        except Exception as e:
            resp.message(f"Desculpe, ocorreu um erro ao processar a imagem: {str(e)}")

    else:
        resp.message("Envie uma foto para que eu possa transformá-la em um desenho para colorir!")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
