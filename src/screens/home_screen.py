import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_home

from src.ui.base_layout import (
    style_base_layout,
    style_background_home
)


def home_screen():

    style_background_home()
    style_base_layout()

    header_home()

    st.title("Attendance that happens in seconds.")

    st.caption(
        "Choose your portal and experience faster, smarter and simpler attendance with Snap Presence."
    )

    st.write("")

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    with col1:

        with st.container(border=True):

            st.subheader("🎓 I'm a Student")

            st.caption("STUDENT")

            st.write(
                "Mark your attendance using Face ID or Voice and manage all your enrolled subjects."
            )

            st.image(
                "https://i.ibb.co/844D9Lrt/mascot-student.png",
                width=135
            )

            if st.button(
                "Student Portal",
                type="primary",
                icon=":material/arrow_outward:",
                icon_position="right",
                use_container_width=True
            ):

                st.session_state["login_type"] = "student"
                st.rerun()

    with col2:

        with st.container(border=True):

            st.subheader("👨‍🏫 I'm a Teacher")

            st.caption("TEACHER")

            st.write(
                "Manage subjects, take attendance and monitor attendance records from one place."
            )

            st.image(
                "https://i.ibb.co/CsmQQV6X/mascot-prof.png",
                width=155
            )

            if st.button(
                "Teacher Portal",
                type="primary",
                icon=":material/arrow_outward:",
                icon_position="right",
                use_container_width=True
            ):

                st.session_state["login_type"] = "teacher"
                st.rerun()

    st.write("")

    st.subheader("Snap Presence Features")

    feature1, feature2, feature3, feature4 = st.columns(4)

    with feature1:

        with st.container(border=True):

            st.write("◉ Face Recognition")
            st.caption("AI-powered attendance")

    with feature2:

        with st.container(border=True):

            st.write("◉ Voice Attendance")
            st.caption("Fast voice-based marking")

    with feature3:

        with st.container(border=True):

            st.write("◉ Smart Records")
            st.caption("Attendance management")

    with feature4:

        with st.container(border=True):

            st.write("◉ Quick Enrollment")
            st.caption("Join subjects instantly")

    st.write("")
    st.write("")
    st.write("")

    footer_home()