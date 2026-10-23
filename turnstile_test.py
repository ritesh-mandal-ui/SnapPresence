
import streamlit as st

from src.components.turnstile import render_turnstile

st.set_page_config(page_title="Turnstile Test", page_icon="🔐")

st.title("Cloudflare Turnstile Test")
st.write("Verify karo ki browser widget Python ko token bhej raha hai.")

token = render_turnstile(
    action="teacher_login",
    key="turnstile_isolated_test",
)

if token:
    st.success("Widget token received successfully.")
    st.write("Token ko security ke liye display nahi kiya gaya.")
else:
    st.info("Verification complete hone par yahan status update hoga.")
