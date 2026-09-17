from pathlib import Path

import streamlit as st


def get_logo_path():

    current_dir = Path(__file__).parent

    image_path = (
        current_dir.parent
        / "assets"
        / "footer_logo.png"
    )

    if image_path.exists():
        return str(image_path)

    return None


def footer_home():

    logo_path = get_logo_path()

    st.markdown(
        """
        <style>

        [data-testid="stImage"] img {
            border-radius: 0 !important;
        }

        /* =====================================================
           HOME FOOTER
           ===================================================== */

        .st-key-home-footer {

            position: fixed !important;

            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;

            width: 100% !important;

            z-index: 999 !important;

            background: transparent !important;

            padding: 8px 0 10px 0 !important;

            margin: 0 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container(key="home-footer"):

        col1, col2, col3 = st.columns(
            [1, 1.2, 1],
            vertical_alignment="center"
        )

        with col2:

            footer_col1, footer_col2 = st.columns(
                [1, 1],
                vertical_alignment="center"
            )

            with footer_col1:

                st.markdown(
                    """
                    <div style="
                        text-align:right;
                        font-size:16px;
                        font-weight:bold;
                        color:#111111;
                        white-space:nowrap;
                    ">
                        Created with ❤️ by
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with footer_col2:

                if logo_path:

                    st.markdown(
                        "<div style='margin-top:7px;'></div>",
                        unsafe_allow_html=True
                    )

                    st.image(
                        logo_path,
                        width=120
                    )

                else:

                    st.markdown(
                        """
                        <div style="
                            font-weight:bold;
                            color:#111111;
                            white-space:nowrap;
                        ">
                            RITESH MANDAL
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


def footer_dashboard():

    logo_path = get_logo_path()

    st.markdown(
        """
        <style>

        [data-testid="stImage"] img {
            border-radius: 0 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(
        [1.5, 1],
        vertical_alignment="center"
    )

    with col1:

        st.markdown(
            """
            <div style="
                text-align:right;
                font-weight:bold;
                color:#111111;
                white-space:nowrap;
            ">
                Created with ❤️ by
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        if logo_path:

            st.markdown(
                "<div style='height:8px;'></div>",
                unsafe_allow_html=True
            )

            st.image(
                logo_path,
                width=120
            )

        else:

            st.markdown(
                """
                <div style="
                    font-weight:bold;
                    color:#111111;
                    white-space:nowrap;
                ">
                    RITESH MANDAL
                </div>
                """,
                unsafe_allow_html=True
            )