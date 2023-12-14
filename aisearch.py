import google.generativeai as genai
import streamlit as st

st.title("Google AI Powered")

genai.configure(api_key=st.secrets["AITK"])
model = genai.GenerativeModel(model_name='gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])

if prompt := st.chat_input("What is up?"):
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
            full_response += (response.text or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "model", "parts": full_response})