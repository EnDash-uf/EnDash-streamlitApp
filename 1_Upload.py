# pages/1_Upload.py
import streamlit as st
import pandas as pd
from pathlib import Path
import time
from lib import auth, db

st.set_page_config(page_title="Upload", page_icon="📂", layout="wide")
auth.require_login()
user = auth.current_user()

st.title("📂 Upload CSV (private)")

uploaded = st.file_uploader("Choose a .csv file", type=["csv"])
if uploaded is not None:
    clean_name = Path(uploaded.name).name
    user_dir = Path("data") / "uploads" / str(user["id"])
    user_dir.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    save_path = user_dir / f"{ts}_{clean_name}"
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())
    db.add_file_record(user["id"], clean_name, str(save_path))
    st.success(f"Saved `{clean_name}`")
    try:
        df = pd.read_csv(save_path)
        st.caption("Preview of your file (first 10 rows):")
        st.dataframe(df.head(10), use_container_width=True)
        numeric_cols = df.select_dtypes("number").columns.tolist()
        if len(numeric_cols) >= 1:
            st.caption("Quick look: first numeric column over index")
            st.line_chart(df[numeric_cols[0]])
        else:
            st.info("No numeric columns detected for a quick chart.")
    except Exception as e:
        st.error(f"Could not read CSV: {e}")

st.divider()
st.subheader("Your uploads")
files = db.list_user_files(user["id"])
if files:
    for rec in files:
        st.write(f"• {rec['filename']}  — uploaded {rec['uploaded_at']}")
else:
    st.caption("No files yet.")
