import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="College Website Chatbot",
    page_icon="🎓",
    layout="centered"
)

# 🎨 Gradient Background + Luxury Styling
st.markdown("""
            
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 35%, rgba(11,136,161,0.8) 100% );
        color: white;
    }

    /* Chat container */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    /* Chat bubbles */
    .stChatMessage {
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
    }

    /* User bubble */
    .stChatMessage[data-testid="chat-message-user"] {
        background: rgba(255, 255, 255, 0.08);
    }

    /* Assistant bubble */
    .stChatMessage[data-testid="chat-message-assistant"] {
        background: rgba(0, 0, 0, 0.4);
    }

    /* Input box */
    textarea {
        background-color: rgba(0,0,0,0.6) !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* Chat input */
    .stChatInputContainer {
        background: rgba(0,0,0,0.5);
        border-radius: 12px;
        padding: 8px;
    }

</style>
""", unsafe_allow_html=True)

st.title("|   D.C. Patel College - CHATBOT   |",)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Modern chat input
if prompt := st.chat_input("Ask something about the college..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    history_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.messages[-10:]]
    )

    try:
        response = requests.post(
            API_URL,
            json={
                "question": prompt,
                "history": history_text
            }
        )

        if response.status_code == 200:
            answer = response.json()["response"]
        else:
            answer = f"API Error: {response.status_code}"

    except Exception as e:
        answer = "Connection Error"
        st.error(str(e))

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)




