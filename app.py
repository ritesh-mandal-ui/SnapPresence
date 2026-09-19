import streamlit as st
import importlib


def load_custom_ui():
    st.markdown(
        """
        <style>
            :root {
                --sp-bg: #f7f8fc;
                --sp-card: #ffffff;
                --sp-text: #111827;
                --sp-muted: #6b7280;
                --sp-border: #e5e7eb;
                --sp-primary: #111827;
                --sp-primary-hover: #000000;
                --sp-radius: 16px;
            }

            .stApp {
                background: var(--sp-bg);
            }

            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 3rem;
                max-width: 1400px;
            }

            .stButton > button {
                border-radius: 10px;
                border: 1px solid var(--sp-border);
                font-weight: 600;
                min-height: 42px;
                transition:
                    transform 0.18s ease,
                    box-shadow 0.18s ease,
                    background 0.18s ease;
            }

            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 18px rgba(17, 24, 39, 0.10);
            }

            .stButton > button:active {
                transform: translateY(0);
            }

            .stButton > button[kind="primary"] {
                background: var(--sp-primary);
                color: white;
                border-color: var(--sp-primary);
            }

            .stButton > button[kind="primary"]:hover {
                background: var(--sp-primary-hover);
                border-color: var(--sp-primary-hover);
            }

            .stTextInput input,
            .stNumberInput input,
            .stSelectbox div[data-baseweb="select"],
            .stTextArea textarea {
                border-radius: 10px;
            }

            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: var(--sp-radius);
                border-color: var(--sp-border);
                background: var(--sp-card);
            }

            div[data-testid="stMetric"] {
                background: var(--sp-card);
                border: 1px solid var(--sp-border);
                border-radius: var(--sp-radius);
                padding: 1rem 1.1rem;
                box-shadow: 0 4px 18px rgba(17, 24, 39, 0.04);
            }

            div[data-testid="stMetricLabel"] {
                color: var(--sp-muted);
            }

            div[data-testid="stMetricValue"] {
                color: var(--sp-text);
                font-weight: 700;
            }

            button[data-baseweb="tab"] {
                font-weight: 600;
            }

            div[data-testid="stAlert"] {
                border-radius: 12px;
            }

            section[data-testid="stSidebar"] {
                background: #ffffff;
                border-right: 1px solid var(--sp-border);
            }

            section[data-testid="stSidebar"] > div {
                padding-top: 1.5rem;
            }

            div[data-testid="stDataFrame"] {
                border-radius: 14px;
                overflow: hidden;
                border: 1px solid var(--sp-border);
            }

            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
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
                    padding-left: 1rem;
                    padding-right: 1rem;
                    padding-top: 1rem;
                }

                .stButton > button {
                    width: 100%;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():

    st.set_page_config(
        page_title="Snap Presence - Making Attendance faster using AI",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )

    load_custom_ui()

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    if st.session_state.get(
        "quick_enrollment_completed"
    ):

        st.session_state.pop(
            "quick_enrollment_completed",
            None
        )

        st.session_state["login_type"] = "student"
        st.session_state["is_logged_in"] = True
        st.session_state["user_role"] = "student"

        st.query_params.clear()

    join_code = st.query_params.get(
        "join-code"
    )

    if join_code:

        if st.session_state.get(
            "login_type"
        ) != "student":

            st.session_state[
                "login_type"
            ] = "student"

            st.rerun(scope="app")

        if (
            st.session_state.get("is_logged_in")
            and st.session_state.get("user_role") == "student"
            and st.session_state.get("student_data")
        ):

            auto_enroll_module = importlib.import_module(
                "src.components.dialog_auto_enroll"
            )

            auto_enroll_module.auto_enroll(
                join_code
            )

            return

    match st.session_state["login_type"]:

        case "teacher":

            teacher_module = importlib.import_module(
                "src.screens.teacher_screen"
            )

            teacher_module.teacher_screen()

        case "student":

            student_module = importlib.import_module(
                "src.screens.student_screen"
            )

            student_module.student_screen()

        case None:

            home_module = importlib.import_module(
                "src.screens.home_screen"
            )

            home_module.home_screen()


if __name__ == "__main__":
    main()