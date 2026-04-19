import streamlit as st, sqlite3, hashlib

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (u TEXT,p TEXT)")

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def signup():
    st.title("Signup")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Create"):
        c.execute("INSERT INTO users VALUES (?,?)",(u,hash_pass(p)))
        conn.commit()
        st.success("Created")

def login():
    st.title("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE u=? AND p=?",(u,hash_pass(p)))
        if c.fetchone():
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Wrong credentials")