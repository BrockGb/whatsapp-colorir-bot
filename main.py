from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)

openai.api_key = "SUA_CHAVE_OPENAI"

def gerar_prompt_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message['content']

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    media_url = request.values.get('MediaUrl0', '')

    resp = MessagingResponse()

    if media_url:
        try:
            # Monta o prompt com a URL da imagem
            prompt = f"Pegue esta foto e faça virar um desenho para colorir igual de livros para colorir. As linhas são pretas e bem definidas com praços simples, desenho fofo tipo dos livros de crianças. Não pode ter sombras nem cores. Não pode ter elementos na imagem que não estavam na imagem original. Mantenha os principais elementos da foto, como posição, poses apenas simplifique os detalhes complexos. 724 Se houver pessoas em volta desenhe de forma amigável e arredondada. gere a imagem no estilo livro para colorir.: {media_url}"

            # Pede o ChatGPT para gerar o desenho/texto
            resposta_chatgpt = gerar_prompt_chatgpt(prompt)

            # Envia a resposta do ChatGPT para o usuário
            resp.message(resposta_chatgpt)

        except Exception as e:
            resp.message(f"Desculpe, ocorreu um erro: {str(e)}")

    else:
        resp.message("Envie uma foto para que eu possa transformá-la em um desenho para colorir!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
