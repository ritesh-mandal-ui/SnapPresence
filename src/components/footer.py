import base64
from pathlib import Path

import streamlit as st


def get_image_base64():

    current_dir = Path(__file__).parent

    image_path = (
        current_dir.parent
        / "assets"
        / "footer_logo.png"
    )

    if not image_path.exists():
        return None

    with open(image_path, "rb") as file:

        return base64.b64encode(
            file.read()
        ).decode()


def footer_home():

    image_base64 = get_image_base64()

    if image_base64:

        image_tag = (
            f'<img src="data:image/png;base64,{image_base64}" '
            f'style="max-height:25px; display:block;" />'
        )

    else:

        image_tag = (
            '<span style="color:white; font-weight:bold;">'
            'RITESH MANDAL'
            '</span>'
        )

    st.html(
        f"""
        <div style="
            margin-top:2rem;
            padding:0.5rem 0 1rem 0;
            display:flex;
            gap:6px;
            justify-content:center;
            align-items:center;
            background:transparent;
        ">

            <p style="
                font-weight:bold;
                color:white;
                margin:0;
            ">
                Created with ❤️ by
            </p>

            {image_tag}

        </div>
        """
    )


def footer_dashboard():

    image_base64 = get_image_base64()

    if image_base64:

        image_tag = (
            f'<img src="data:image/png;base64,{image_base64}" '
            f'style="max-height:25px; display:block;" />'
        )

    else:

        image_tag = (
            '<span style="color:black; font-weight:bold;">'
            'RITESH MANDAL'
            '</span>'
        )

    st.html(
        f"""
        <div style="
            margin-top:2rem;
            padding:0.5rem 0 1rem 0;
            display:flex;
            gap:6px;
            justify-content:center;
            align-items:center;
            background:transparent;
        ">

            <p style="
                font-weight:bold;
                color:black;
                margin:0;
            ">
                Created with ❤️ by
            </p>

            {image_tag}

        </div>
        """
    )