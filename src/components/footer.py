from pathlib import Path

import streamlit as st


def get_logo_path():

    current_dir = Path(__file__).parent

    image_path = (
        current_dir.parent
        / "assets"
        / "footer_logo.png"
    )

    if image_path.exists():
        return str(image_path)

    return None


def footer_home():

    logo_path = get_logo_path()

    st.markdown(
        """
        <style>

        [data-testid="stImage"] img {
            border-radius: 0 !important;
        }

        .st-key-home-footer {
            position: fixed !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100% !important;
            z-index: 999 !important;
            background: rgba(247, 248, 252, 0.94) !important;
            backdrop-filter: blur(10px) !important;
            padding: 6px 0 8px 0 !important;
            margin: 0 !important;
            border-top: 1px solid #e5e7eb !important;
        }

        .st-key-home-footer [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            justify-content: center !important;
        }

        .st-key-home-footer [data-testid="column"] {
            padding: 0 !important;
        }

        .st-key-home-footer [data-testid="stImage"] {
            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            margin: 0 !important;
        }

        .st-key-home-footer [data-testid="stMarkdownContainer"] {
            display: flex !important;
            justify-content: flex-end !important;
            align-items: center !important;
            height: 100% !important;
            white-space: nowrap !important;
        }

        @media (max-width: 768px) {

            .st-key-home-footer {
                padding: 5px 8px 7px 8px !important;
            }

            .st-key-home-footer [data-testid="stHorizontalBlock"] {
                width: fit-content !important;
                margin: 0 auto !important;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container(key="home-footer"):

        col1, col2, col3 = st.columns(
            [1, 1.8, 1],
            vertical_alignment="center"
        )

        with col2:

            footer_col1, footer_col2 = st.columns(
                [1.2, 1],
                gap="small",
                vertical_alignment="center"
            )

            with footer_col1:

                st.markdown(
                    "Created with ❤️ by",
                    text_alignment="right"
                )

            with footer_col2:

                if logo_path:

                    st.image(
                        logo_path,
                        width=105
                    )

                else:

                    st.write("RITESH MANDAL")


def footer_dashboard():

    logo_path = get_logo_path()

    st.markdown(
        """
        <style>

        [data-testid="stImage"] img {
            border-radius: 0 !important;
        }

        .st-key-home-footer [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(
        [1, 1],
        vertical_alignment="center"
    )

    with col1:

        st.markdown(
            "Created with ❤️ by",
            text_alignment="right"
        )

    with col2:

        if logo_path:

            st.image(
                logo_path,
                width=105
            )

        else:

            st.write("RITESH MANDAL")