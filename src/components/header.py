import streamlit as st
from pathlib import Path


def get_logo_path():

    logo_path = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "logo.png"
    )

    return str(logo_path)


def header_home():

    logo_path = get_logo_path()

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:
        st.image(
            logo_path,
            width=300
        )


def header_dashboard():

    logo_path = get_logo_path()

    st.image(
        logo_path,
        width=255
    )