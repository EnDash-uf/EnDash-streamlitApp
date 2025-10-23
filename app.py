# app.py
import streamlit as st
from lib import db, auth

st.set_page_config(page_title="Climate Dashboard (Starter)", page_icon="🌿", layout="wide")

# Initialize DB & ensure admin
db.init_db()
auth.ensure_admin()

# Sidebar: user status + logout
with st.sidebar:
    st.title("🌿 Dashboard")
    user = auth.current_user()
    if user:
        st.caption(f"Signed in as **{user['username']}**")
        if st.button("Log out"):
            auth.logout()
            st.rerun()
    else:
        st.caption("Not signed in")

st.title("Welcome")
st.write("This is a minimal starter to prove out login, per-user settings, and uploads.")

user = auth.current_user()
if user:
    st.success("You're signed in. Use the sidebar pages to continue:")
    st.markdown("- **Upload**: upload a CSV (private to your account)")
    st.markdown("- **Settings**: set your preferences")
    st.markdown("- **Dashboard**: view a simple summary")
else:
    st.subheader("Sign in")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")
    if submitted:
        ok = auth.login(username, password)
        if ok:
            st.success("Logged in.")
            st.rerun()
        else:
            st.error("Invalid username or password.")

st.divider()
st.caption("Admin credentials are read from `.streamlit/secrets.toml` (local) or app secrets in deployment. Change them immediately.")
