# pages/2_Settings.py
import streamlit as st
from lib import auth, db

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="centered")
auth.require_login()
user = auth.current_user()

st.title("⚙️ Settings")

row = db.get_or_create_settings(user["id"])

with st.form("settings_form"):
    col1, col2 = st.columns(2)
    with col1:
        unit_pref = st.selectbox("Unit preference", ["metric", "imperial"], index=0 if row["unit_pref"]=="metric" else 1)
        temp_unit = st.selectbox("Temperature unit", ["C","F"], index=0 if row["temp_unit"]=="C" else 1)
    with col2:
        temp_set = st.number_input("Ideal temperature setpoint", value=float(row["temp_setpoint"]), step=0.5)
        rh_set = st.number_input("Ideal RH setpoint (%)", value=float(row["rh_setpoint"]), step=1.0)
        vpd_set = st.number_input("Ideal VPD setpoint (kPa)", value=float(row["vpd_setpoint"]), step=0.1)
    saved = st.form_submit_button("Save")

if saved:
    db.update_settings(user["id"], unit_pref, temp_unit, float(temp_set), float(rh_set), float(vpd_set))
    st.success("Settings saved.")
