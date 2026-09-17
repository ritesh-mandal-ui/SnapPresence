import streamlit as st
import importlib


def main():
    st.set_page_config(
        page_title="Snap Presence - Making Attendance faster using AI",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

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

    join_code = st.query_params.get("join-code")

    if join_code:

        if st.session_state.get("login_type") != "student":
            st.session_state["login_type"] = "student"
            st.rerun()

        if (
            st.session_state.get("is_logged_in")
            and st.session_state.get("user_role") == "student"
        ):
            auto_enroll_module = importlib.import_module(
                "src.components.dialog_auto_enroll"
            )
            auto_enroll_module.auto_enroll_dialog(join_code)


if __name__ == "__main__":
    main()