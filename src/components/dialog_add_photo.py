import streamlit as st

from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write(
        "Add classroom photos to scan for attendance."
    )

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(2)

    with t1:
        camera_type = (
            "primary"
            if st.session_state.photo_tab == "camera"
            else "tertiary"
        )

        if st.button(
            "Camera",
            type=camera_type,
            width="stretch"
        ):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with t2:
        upload_type = (
            "primary"
            if st.session_state.photo_tab == "upload"
            else "tertiary"
        )

        if st.button(
            "Upload photos",
            type=upload_type,
            width="stretch"
        ):
            st.session_state.photo_tab = "upload"
            st.rerun()

    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input(
            "Take Snapshot",
            key="dialog_cam"
        )

        if cam_photo:

            st.session_state.attendance_images.append(
                Image.open(cam_photo)
            )

            st.toast("Photo captured.")
            st.rerun()

    elif st.session_state.photo_tab == "upload":

        uploaded_files = st.file_uploader(
            "Choose image files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload"
        )

        if uploaded_files:

            for file in uploaded_files:

                st.session_state.attendance_images.append(
                    Image.open(file)
                )

            st.toast(
                "Photos uploaded successfully."
            )

            st.rerun()

    st.divider()

    if st.button(
        "Done",
        type="primary",
        width="stretch"
    ):
        st.rerun()