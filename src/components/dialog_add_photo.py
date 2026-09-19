import streamlit as st

from PIL import Image


@st.dialog("Capture or Upload Photos")
def add_photos_dialog():

    st.subheader(
        "Add Classroom Photos"
    )

    st.caption(
        "Capture photos using your camera or upload existing "
        "classroom photos for attendance scanning."
    )

    st.write("")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(
        2,
        gap="small"
    )

    with t1:

        camera_type = (
            "primary"
            if st.session_state.photo_tab == "camera"
            else "secondary"
        )

        if st.button(
            "Camera",
            type=camera_type,
            width="stretch",
            icon=":material/photo_camera:"
        ):

            st.session_state.photo_tab = "camera"
            st.rerun()

    with t2:

        upload_type = (
            "primary"
            if st.session_state.photo_tab == "upload"
            else "secondary"
        )

        if st.button(
            "Upload Photos",
            type=upload_type,
            width="stretch",
            icon=":material/upload:"
        ):

            st.session_state.photo_tab = "upload"
            st.rerun()

    st.write("")

    if st.session_state.photo_tab == "camera":

        with st.container(
            border=True
        ):

            st.subheader(
                "Take a Snapshot"
            )

            st.caption(
                "Capture a clear classroom photo with students visible."
            )

            cam_photo = st.camera_input(
                "Take Snapshot",
                key="dialog_cam"
            )

        if cam_photo:

            st.session_state.attendance_images.append(
                Image.open(cam_photo)
            )

            st.toast(
                "Photo captured."
            )

            st.rerun()

    elif st.session_state.photo_tab == "upload":

        with st.container(
            border=True
        ):

            st.subheader(
                "Upload Classroom Photos"
            )

            st.caption(
                "You can select multiple JPG or PNG images at once."
            )

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

    st.write("")

    photo_count = len(
        st.session_state.attendance_images
    )

    if photo_count:

        st.info(
            f"{photo_count} photo(s) ready for attendance analysis."
        )

    st.divider()

    if st.button(
        "Done",
        type="primary",
        width="stretch",
        icon=":material/check:"
    ):

        st.rerun()