import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# page config
st.set_page_config(
    page_title="Book AI"
)

st.title("Book AI")
st.caption("Converse com uma IA especializada em livros.")

# conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user input
if prompt := st.chat_input("Pergunte sobre um livro..."):

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # context/agent instruction
    system_instruction = """ 
    Você é um assistente de inteligência artificial especializado em livros,
    literatura e leitura.

    Seu objetivo é responder dúvidas sobre livros, autores, personagens,
    enredos, temas, estilos literários e interpretações.

    Regras:
    - Responda de maneira clara e didática.
    - Quando o usuário perguntar sobre uma obra específica, considere o
      contexto da obra antes de responder.
    - Não invente informações sobre livros, autores ou personagens.
    - Se não tiver segurança sobre uma informação, deixe isso claro.
    - Se a pergunta não tiver relação com livros ou literatura, informe
      educadamente que seu foco é esse domínio.
    """

    # build the historic to send to the model
    contents = []

    for message in st.session_state.messages:
        contents.append({
            "role": "model" if message["role"] == "assistant" else "user",
            "parts": [
                {
                    "text": message["content"]
                }
            ]
        })

    # Gemini call
    with st.chat_message("assistant"):

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.7,
                "max_output_tokens": 1000,
            }
        )

        answer = response.text

        st.markdown(answer)

    # save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })