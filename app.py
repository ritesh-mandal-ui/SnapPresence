import streamlit as st
import importlib


def main():

    st.set_page_config(
        page_title="Snap Presence - Making Attendance faster using AI",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    # =====================================================
    # QUICK ENROLLMENT COMPLETED
    # =====================================================

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

    # =====================================================
    # CHECK JOIN CODE
    # =====================================================

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

    # =====================================================
    # NORMAL APP ROUTING
    # =====================================================

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