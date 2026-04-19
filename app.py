import streamlit as st
from backend import stream_answer
from storage import *
from auth import login, signup
from voice import speech_to_text
from vision import extract_text_from_image
from pdf_chat import process_pdf
import uuid

st.set_page_config(page_title="Agent Pro", layout="wide")

# AUTH
if "user" not in st.session_state:
    st.session_state.user = None

menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

if not st.session_state.user:
    if menu == "Login":
        login()
    else:
        signup()
    st.stop()

USER = st.session_state.user

# SESSION INIT
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "db" not in st.session_state:
    st.session_state.db = None

# SIDEBAR
st.sidebar.title("💬 Chats")
search = st.sidebar.text_input("🔍 Search")

chats = load_chats(USER)

for chat_id, title in chats.items():
    if search.lower() in title.lower():
        if st.sidebar.button(title, key=chat_id):
            st.session_state.chat_id = chat_id
            st.session_state.messages = load_chat(USER, chat_id)

        if st.sidebar.button("❌", key=chat_id+"del"):
            delete_chat(USER, chat_id)

if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_id = str(uuid.uuid4())
    st.session_state.messages = []

# PDF
pdf_file = st.sidebar.file_uploader("📄 Upload PDF", type="pdf")
if pdf_file:
    st.session_state.db = process_pdf(pdf_file)
    st.success("PDF Ready!")

# UI
st.title("🤖 Agent Pro")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# INPUT
col1, col2, col3 = st.columns([3,1,1])

with col1:
    user_input = st.chat_input("Type message")

with col2:
    audio = st.file_uploader("🎤 Voice", type=["wav","mp3"])

with col3:
    img = st.camera_input("📷 Camera")

# VOICE
if audio:
    user_input = speech_to_text(audio)
    st.success(user_input)

# IMAGE
if img:
    user_input = extract_text_from_image(img)
    st.success(user_input)

# PROCESS
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    db = st.session_state.get("db", None)

    # Limit history
    history = st.session_state.messages[-5:]

    # Agent status
    if db and "pdf" in user_input.lower():
        st.info("📄 Agent using PDF knowledge")
    else:
        st.info("🤖 Agent reasoning...")

    response_box = st.empty()
    full = ""

    for chunk in stream_answer(user_input, db, history):
        full += chunk
        response_box.markdown(full + "▌")

    response_box.markdown(full)

    st.session_state.messages.append({"role":"assistant","content":full})

    save_chat(USER, st.session_state.chat_id, st.session_state.messages)