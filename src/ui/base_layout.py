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
                background: #f7f8fc !important;
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
            }

            [data-testid="stAppViewContainer"] > div:last-child,
            [data-testid="stAppViewContainer"] > div:last-child > div {
                background: transparent !important;
                background-color: transparent !important;
            }

            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }

            ::-webkit-scrollbar-track {
                background: transparent;
            }

            ::-webkit-scrollbar-thumb {
                background: #d1d5db;
                border-radius: 999px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: #9ca3af;
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
                background: #f7f8fc !important;
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
            }

            [data-testid="stAppViewContainer"] > div:last-child,
            [data-testid="stAppViewContainer"] > div:last-child > div {
                background: transparent !important;
                background-color: transparent !important;
            }

            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }

            ::-webkit-scrollbar-track {
                background: transparent;
            }

            ::-webkit-scrollbar-thumb {
                background: #d1d5db;
                border-radius: 999px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: #9ca3af;
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
                'https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap'
            );

            :root {
                --sp-bg: #f7f8fc;
                --sp-card: #ffffff;
                --sp-text: #111827;
                --sp-muted: #6b7280;
                --sp-border: #e5e7eb;
                --sp-primary: #111111;
                --sp-primary-hover: #000000;
                --sp-radius: 16px;
            }

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
                color: var(--sp-text) !important;
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
            }

            [data-testid="stAppViewContainer"] > div:last-child,
            [data-testid="stAppViewContainer"] > div:last-child > div {
                background: transparent !important;
                background-color: transparent !important;
            }

            [data-testid="stMainBlockContainer"]::before,
            [data-testid="stMainBlockContainer"]::after {
                background: transparent !important;
            }

            .block-container {
                max-width: 1400px !important;
                padding-top: 1.25rem !important;
                padding-bottom: 2rem !important;
            }

            h1,
            h2,
            h3,
            h4,
            h5,
            h6 {
                font-family: 'Outfit', sans-serif !important;
                color: var(--sp-text) !important;
                letter-spacing: -0.025em !important;
            }

            p,
            label,
            span,
            div {
                font-family: 'Outfit', sans-serif;
            }

            button {
                font-family: 'Outfit', sans-serif !important;
                border-radius: 11px !important;
                font-weight: 600 !important;
                transition:
                    transform 0.18s ease,
                    box-shadow 0.18s ease,
                    background 0.18s ease !important;
            }

            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 7px 20px rgba(17, 24, 39, 0.10);
            }

            button:active {
                transform: translateY(0);
            }

            button:disabled {
                transform: none !important;
                cursor: not-allowed !important;
                box-shadow: none !important;
            }

            button[kind="primary"] {
                background: #111111 !important;
                color: #ffffff !important;
                border: 1px solid #111111 !important;
            }

            button[kind="primary"]:hover {
                background: #000000 !important;
                border-color: #000000 !important;
            }

            button[kind="secondary"] {
                background: #ffffff !important;
                color: #111111 !important;
                border: 1px solid #d1d5db !important;
            }

            button[kind="secondary"]:hover {
                background: #f3f4f6 !important;
                border-color: #9ca3af !important;
            }

            button[kind="tertiary"] {
                background: #111111 !important;
                color: #ffffff !important;
                border: 1px solid #111111 !important;
            }

            .stTextInput input,
            .stNumberInput input,
            .stTextArea textarea {
                background: #ffffff !important;
                border: 1px solid var(--sp-border) !important;
                border-radius: 11px !important;
                color: #111827 !important;
                -webkit-text-fill-color: #111827 !important;
                transition:
                    border-color 0.18s ease,
                    box-shadow 0.18s ease !important;
            }

            .stTextInput input::placeholder,
            .stNumberInput input::placeholder,
            .stTextArea textarea::placeholder {
                color: #6b7280 !important;
                -webkit-text-fill-color: #6b7280 !important;
                opacity: 1 !important;
            }

            .stTextInput input:focus,
            .stNumberInput input:focus,
            .stTextArea textarea:focus {
                border-color: #9ca3af !important;
                box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.06) !important;
            }

            div[data-baseweb="select"] {
                border-radius: 11px !important;
            }

            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: var(--sp-card) !important;
                border: 1px solid var(--sp-border) !important;
                border-radius: var(--sp-radius) !important;
                box-shadow: 0 5px 22px rgba(17, 24, 39, 0.045) !important;
            }

            div[data-testid="stMetric"] {
                background: var(--sp-card) !important;
                border: 1px solid var(--sp-border) !important;
                border-radius: var(--sp-radius) !important;
                padding: 1rem 1.15rem !important;
                box-shadow: 0 5px 22px rgba(17, 24, 39, 0.045) !important;
            }

            div[data-testid="stMetricLabel"] {
                color: var(--sp-muted) !important;
                font-weight: 500 !important;
            }

            div[data-testid="stMetricValue"] {
                color: var(--sp-text) !important;
                font-weight: 750 !important;
            }

            button[data-baseweb="tab"] {
                font-weight: 600 !important;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #111111 !important;
            }

            div[data-testid="stAlert"] {
                border-radius: 12px !important;
            }

            section[data-testid="stSidebar"] {
                background: #ffffff !important;
                border-right: 1px solid var(--sp-border) !important;
            }

            section[data-testid="stSidebar"] > div {
                padding-top: 1.25rem !important;
            }

            div[data-testid="stDataFrame"] {
                border-radius: 14px !important;
                overflow: hidden !important;
                border: 1px solid var(--sp-border) !important;
            }

            [data-testid="stFileUploader"] {
                background: #ffffff !important;
                border-radius: 14px !important;
            }

            [data-testid="stFileUploaderDropzone"] {
                border-radius: 14px !important;
                border: 1px dashed #d1d5db !important;
                background: #ffffff !important;
            }

            [data-testid="stFileUploaderDropzone"]:hover {
                border-color: #9ca3af !important;
                background: #fafafa !important;
            }

            #MainMenu,
            header,
            footer {
                visibility: hidden !important;
            }

            [data-testid="stDecoration"] {
                display: none !important;
            }

            section.main {
                overflow-x: hidden !important;
            }

            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }

            ::-webkit-scrollbar-track {
                background: transparent;
            }

            ::-webkit-scrollbar-thumb {
                background: #d1d5db;
                border-radius: 999px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: #9ca3af;
            }

            @media (max-width: 768px) {
                .block-container {
                    padding-left: 1rem !important;
                    padding-right: 1rem !important;
                    padding-top: 1rem !important;
                }

                button {
                    min-height: 42px !important;
                }
            }

            @media (prefers-reduced-motion: reduce) {
                *,
                *::before,
                *::after {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )