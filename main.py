import os
import base64
import requests
from flask import Flask, request, Response
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("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"))

@app.route("/bot", methods=["POST"])
def bot():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        media_url = request.values.get("MediaUrl0", "")

        print(f"Mensagem recebida: {incoming_msg}")
        print(f"Media URL: {media_url}")

        if media_url:
            # Baixa a imagem
            image_response = requests.get(media_url)
            image_base64 = base64.b64encode(image_response.content).decode("utf-8")
            print("Imagem convertida para base64.")

            image_data_url = f"data:image/jpeg;base64,{image_base64}"

            # Cria o prompt para a imagem
            prompt = incoming_msg if incoming_msg else "Pegue esta foto e faça virar um desenho para colorir igual de livros para colorir. As linhas são pretas e bem definidas com praços simples, desenho fofo tipo dos livros de crianças. Não pode ter sombras nem cores. Não pode ter elementos na imagem que não estavam na imagem original. Mantenha os principais elementos da foto, como posição, poses apenas simplifique os detalhes complexos. 724 Se houver pessoas em volta desenhe de forma amigável e arredondada. gere a imagem no estilo livro para colorir."

            # Envia para o modelo GPT-4 com visão
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_data_url}}
                        ]
                    }
                ],
                max_tokens=300
            )

            result = response.choices[0].message.content
        else:
            result = "Por favor, envie uma imagem junto com sua mensagem."

        # Resposta XML compatível com Twilio/WhatsApp
        twilio_resp = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{result}</Message>
</Response>"""

        return Response(twilio_resp, mimetype="application/xml")

    except Exception as e:
        print("Erro no servidor:", e)
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Houve um erro interno no servidor. Tente novamente mais tarde.</Message>
</Response>""", mimetype="application/xml")

@app.route("/", methods=["GET"])
def home():
    return "Servidor Flask rodando com sucesso!"

