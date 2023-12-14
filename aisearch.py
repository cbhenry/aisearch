import google.generativeai as genai
import streamlit as st
import json

print('* Enter the application')

st.title("Google AI Powered Search")
st.subheader("BETA-Version, bugs 🐞 are accepted.")
st.subheader("Drop message to :blue[Henry] (_if you know him_) if met 🐞🐛.", divider="rainbow")

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

    with st.chat_message("model"):
        message_placeholder = st.empty()
        full_response = ""
        for response in model.generate_content(
            [
                {"role": m["role"], "parts": m["parts"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            print(response.__dict__)
            full_response += (response.text or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "model", "parts": full_response})