import io

import segno
import streamlit as st


@st.dialog("Share Class Link")
def share_subject_dialog(
    subject_name,
    subject_code
):

    app_domain = "snappresence-main.streamlit.app"

    join_url = (
        f"{app_domain}/?join-code={subject_code}"
    )

    st.header("Scan to Join")

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

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Copy Link")

        st.text_input(
            "Class Link",
            value=join_url,
            label_visibility="collapsed"
        )

        st.text_input(
            "Subject Code",
            value=subject_code,
            label_visibility="collapsed"
        )

        st.info(
            "Copy this link to share on WhatsApp or Email."
        )

    with col2:

        st.markdown("### Scan to Join")

        st.image(
            output.getvalue(),
            caption="QR code for class joining"
        )