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

    with open(logo_path, "rb") as file:
        import base64

        logo_base64 = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <div style="
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto 20px auto;
        ">
            <img
                src="data:image/png;base64,{logo_base64}"
                style="
                    width: 300px;
                    max-width: 100%;
                    display: block;
                    margin: 0 auto;
                "
            >
        </div>
        """,
        unsafe_allow_html=True
    )


def header_dashboard():

    logo_path = get_logo_path()

    st.image(
        logo_path,
        width=255
    )