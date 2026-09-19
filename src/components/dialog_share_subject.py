import io

import segno
import streamlit as st


@st.dialog("Share Class Link")
def share_subject_dialog(
    subject_name,
    subject_code
):

    app_domain = (
        "https://snappresence-yfxlcxdgu8vubz9ktrwmvz.streamlit.app"
    )

    join_url = (
        f"{app_domain}/?join-code={subject_code}"
    )

    st.subheader(
        "Share Your Class"
    )

    st.caption(
        f"Invite students to join {subject_name}."
    )

    st.write("")

    qr = segno.make(
        join_url
    )

    output = io.BytesIO()

    qr.save(
        output,
        kind="png",
        scale=10,
        border=1
    )

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    with col1:

        with st.container(
            border=True
        ):

            st.subheader(
                "Class Link"
            )

            st.caption(
                "Share this link with your students."
            )

            st.text_input(
                "Class Link",
                value=join_url,
                label_visibility="collapsed"
            )

            st.write("")

            st.text_input(
                "Subject Code",
                value=subject_code,
                label_visibility="collapsed"
            )

            st.info(
                "Copy the class link and share it through "
                "WhatsApp, Email or any other platform."
            )

    with col2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Scan to Join"
            )

            st.caption(
                "Students can scan this QR code to join instantly."
            )

            st.image(
                output.getvalue(),
                caption="Scan to join the class"
            )