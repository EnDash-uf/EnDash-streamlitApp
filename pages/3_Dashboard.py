# pages/3_Dashboard.py
import streamlit as st
import pandas as pd
from pathlib import Path
from lib import auth, db

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("📊 Dashboard (very minimal)")

files = db.list_user_files(user["id"])
if not files:
    st.info("Upload a CSV first (Upload page)." )
    st.stop()

options = {f"{rec['filename']} ({rec['uploaded_at']})": rec for rec in files}
label = st.selectbox("Select a file", list(options.keys()))
rec = options[label]
path = Path(rec["saved_path"])

try:
    df = pd.read_csv(path)
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

st.subheader("Summary table")
st.dataframe(df.describe(include='all').transpose(), use_container_width=True)

st.subheader("Quick chart")
num_cols = df.select_dtypes("number").columns.tolist()
if len(num_cols) >= 2:
    x = st.selectbox("x-axis", ["index"] + num_cols, index=0)
    y = st.selectbox("y-axis", num_cols, index=0)
    if x == "index":
        st.line_chart(df[y])
    else:
        st.line_chart(df.set_index(x)[y])
elif len(num_cols) == 1:
    st.line_chart(df[num_cols[0]])
else:
    st.info("No numeric columns to plot yet.")
