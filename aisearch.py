import google.generativeai as genai
from openai import OpenAI
import streamlit as st
import json

print('* Enter the application')

def adaptModel(message, option):
    if option == "Google Gemini" and message["role"] == "assistant":
        message["role"] = 'model'
    return message

st.title("AI Powered Search - for those who being blocked")
st.subheader("Lots of bugs, dont expected to much, donate to extend the tokens.")
st.image("alipay.png", width=100)
st.write("Drop message to :blue[Henry] (_if you know him_) if met 🐞🐛.", divider="rainbow")

option = st.selectbox(
    "Select AI Model:",
    ("Google Gemini", "DeepSeek-Chat", "DeekSeek-Reasoner"),
)

genai.configure(api_key=st.secrets["AITK"])
model = genai.GenerativeModel(model_name='gemini-pro', safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },{
            "category": "HARM_CATEGORY_SEXUAL",
            "threshold": "BLOCK_NONE",
        },{
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        }
        ]
        )

model2 = OpenAI(api_key=st.secrets["AITK2"], base_url="https://api.deepseek.com")

print("* constructed model")

if "messages" not in st.session_state:
    st.session_state.messages = []

print("* init messages")

for message in st.session_state.messages:
    print("** check messages")
    with st.chat_message(message["role"]):
        print("*** chat messages")
        st.markdown(message["parts"])

if prompt := st.chat_input("What is up?"):
    print(prompt)
    st.session_state.messages.append({"role": "user", "parts": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    assistant = "assistant"
    if option == "Google Gemini":
        assistant = "model"

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            if option == "Google Gemini":
                adapteModelMessage = [adaptModel(m, option) for m in st.session_state.messages]
                completion = model.generate_content(
                    [
                        {"role": m["role"], "parts": m["parts"]}
                        for m in adapteModelMessage
                    ],
                    stream=True,
                )
                for chunk in completion:
                    print(chunk);
                    full_response += chunk.text
                    print(full_response);
                    message_placeholder.markdown(full_response + "▌")
            elif option == "DeepSeek-Chat":
                completion = model2.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": m["role"], "content": m["parts"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
            elif option == "DeekSeek-Reasoner":
                completion = model2.chat.completions.create(
                    model="deepseek-coder",
                    messages=[
                        {"role": m["role"], "content": m["parts"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "parts": full_response})
        except Exception as e:
            print(e)
            st.toast(e, icon='🎉')
