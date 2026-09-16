import streamlit as st


def style_background_home():

    st.markdown(
        """
        <style>

        html,
        body,
        #root,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > section,
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {

            background: #FFFFFF !important;
        }

        .stApp {

            overflow-x: hidden !important;
        }

        [data-testid="stMainBlockContainer"],
        [data-testid="stMainBlockContainer"] > div,
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stAppViewContainer"] > .main > div,
        [data-testid="stAppViewContainer"] > .main > div > div {

            background: transparent !important;
        }

        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"] > div,
        [data-testid="stBottom"] > div > div,
        [data-testid="stBottomBlockContainer"] > div > div {

            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            min-height: 0 !important;
        }

        [data-testid="stBottom"]::before,
        [data-testid="stBottom"]::after,
        [data-testid="stBottomBlockContainer"]::before,
        [data-testid="stBottomBlockContainer"]::after {

            content: none !important;
            display: none !important;
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }

        [data-testid="stAppViewContainer"] > div:last-child,
        [data-testid="stAppViewContainer"] > div:last-child > div {

            background: transparent !important;
            background-color: transparent !important;
        }

        ::-webkit-scrollbar {

            width: 0px;
            height: 0px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def style_background_dashboard():

    st.markdown(
        """
        <style>

        html,
        body,
        #root,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > section,
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {

            background: #E0E3FF !important;
        }

        .stApp {

            overflow-x: hidden !important;
        }

        [data-testid="stMainBlockContainer"],
        [data-testid="stMainBlockContainer"] > div,
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stAppViewContainer"] > .main > div,
        [data-testid="stAppViewContainer"] > .main > div > div {

            background: transparent !important;
        }

        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"] > div,
        [data-testid="stBottom"] > div > div,
        [data-testid="stBottomBlockContainer"] > div > div {

            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            min-height: 0 !important;
        }

        [data-testid="stBottom"]::before,
        [data-testid="stBottom"]::after,
        [data-testid="stBottomBlockContainer"]::before,
        [data-testid="stBottomBlockContainer"]::after {

            content: none !important;
            display: none !important;
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }

        [data-testid="stAppViewContainer"] > div:last-child,
        [data-testid="stAppViewContainer"] > div:last-child > div {

            background: transparent !important;
            background-color: transparent !important;
        }

        ::-webkit-scrollbar {

            width: 0px;
            height: 0px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def style_base_layout():

    st.markdown(
        """
        <style>

        @import url(
            'https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap'
        );

        html,
        body,
        #root {

            margin: 0 !important;
            padding: 0 !important;

            font-family: 'Outfit', sans-serif !important;
        }

        .stApp {

            font-family: 'Outfit', sans-serif !important;

            overflow-x: hidden !important;

            min-height: 100vh !important;
        }

        [data-testid="stAppViewContainer"] {

            min-height: 100vh !important;

            background: transparent !important;
        }

        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        [data-testid="stMainBlockContainer"] > div,
        [data-testid="stMainBlockContainer"] > div > div,
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stAppViewContainer"] > .main > div,
        [data-testid="stAppViewContainer"] > .main > div > div,
        section.main,
        section.main > div,
        section.main > div > div {

            background: transparent !important;
        }

        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"] > div,
        [data-testid="stBottom"] > div > div,
        [data-testid="stBottomBlockContainer"] > div > div,
        [data-testid="stBottom"] > div > div > div,
        [data-testid="stBottomBlockContainer"] > div > div > div {

            background: transparent !important;

            background-color: transparent !important;

            box-shadow: none !important;

            border: none !important;

            min-height: 0 !important;
        }

        [data-testid="stAppViewContainer"] > div:last-child,
        [data-testid="stAppViewContainer"] > div:last-child > div {

            background: transparent !important;

            background-color: transparent !important;
        }

        [data-testid="stBottom"]::before,
        [data-testid="stBottom"]::after,
        [data-testid="stBottomBlockContainer"]::before,
        [data-testid="stBottomBlockContainer"]::after {

            content: none !important;

            display: none !important;

            background: transparent !important;

            box-shadow: none !important;

            border: none !important;
        }

        [data-testid="stMainBlockContainer"]::before,
        [data-testid="stMainBlockContainer"]::after {

            background: transparent !important;
        }

        .block-container {

            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {

            font-family: 'Outfit', sans-serif !important;
        }

        button {

            font-family: 'Outfit', sans-serif !important;

            border-radius: 12px !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease !important;
        }

        button[kind="secondary"] {

            background: #FF5C8A !important;

            color: white !important;

            border: none !important;
        }

        button[kind="tertiary"] {

            background: #111111 !important;

            color: white !important;

            border: none !important;
        }

        button:hover {

            transform: scale(1.02);
        }

        button:disabled {

            transform: none !important;

            cursor: not-allowed !important;
        }

        #MainMenu {

            visibility: hidden;
        }

        header {

            visibility: hidden;
        }

        footer {

            visibility: hidden;
        }

        [data-testid="stDecoration"] {

            display: none !important;
        }

        section.main {

            overflow-x: hidden !important;
        }

        ::-webkit-scrollbar {

            width: 0px;
            height: 0px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )