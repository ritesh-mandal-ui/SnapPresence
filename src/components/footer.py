import streamlit as st


def footer_home():

    st.markdown(
        """
        <style>

        .st-key-home-footer {
            position: fixed !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 6px !important;
            width: 100% !important;
            z-index: 999 !important;
            background: rgba(247, 248, 252, 0.94) !important;
            backdrop-filter: blur(10px) !important;
            padding: 7px 12px 9px 12px !important;
            margin: 0 !important;
            border-top: 1px solid #e5e7eb !important;
        }

        .st-key-home-footer [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            justify-content: center !important;
        }

        .st-key-home-footer [data-testid="column"] {
            padding: 0 !important;
        }

        .st-key-home-footer [data-testid="stMarkdownContainer"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
        }

        .sp-footer-content {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            width: 100%;
            white-space: nowrap;
            font-size: 13px;
            line-height: 1.2;
        }

        .sp-footer-created {
            color: #6b7280;
            font-weight: 500;
        }

        .sp-footer-name {
            color: #111827;
            font-weight: 700;
            letter-spacing: 0.7px;
            transition:
                letter-spacing 0.2s ease,
                transform 0.2s ease;
        }

        .sp-footer-name:hover {
            letter-spacing: 1px;
            transform: translateY(-1px);
        }

        @media (max-width: 768px) {

            .st-key-home-footer {
                padding: 6px 8px 8px 8px !important;
            }

            .sp-footer-content {
                font-size: 12px;
                gap: 6px;
            }

        }

        @media (max-width: 380px) {

            .sp-footer-content {
                font-size: 11px;
                gap: 5px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container(key="home-footer"):

        st.markdown(
            """
            <div class="sp-footer-content">
                <span class="sp-footer-created">Created with ❤️ by</span>
                <span class="sp-footer-name">RITESH MANDAL</span>
            </div>
            """,
            unsafe_allow_html=True
        )


def footer_dashboard():

    st.markdown(
        """
        <style>

        .sp-dashboard-footer {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 8px 12px 12px 12px;
            margin-top: 20px;
        }

        .sp-dashboard-footer-content {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            width: 100%;
            white-space: nowrap;
            font-size: 13px;
            line-height: 1.2;
        }

        .sp-dashboard-footer-created {
            color: #6b7280;
            font-weight: 500;
        }

        .sp-dashboard-footer-name {
            color: #111827;
            font-weight: 700;
            letter-spacing: 0.7px;
            transition:
                letter-spacing 0.2s ease,
                transform 0.2s ease;
        }

        .sp-dashboard-footer-name:hover {
            letter-spacing: 1px;
            transform: translateY(-1px);
        }

        @media (max-width: 768px) {

            .sp-dashboard-footer {
                padding: 8px 8px 12px 8px;
            }

            .sp-dashboard-footer-content {
                font-size: 12px;
                gap: 6px;
            }

        }

        @media (max-width: 380px) {

            .sp-dashboard-footer-content {
                font-size: 11px;
                gap: 5px;
            }

        }

        </style>

        <div class="sp-dashboard-footer">
            <div class="sp-dashboard-footer-content">
                <span class="sp-dashboard-footer-created">Created with ❤️ by</span>
                <span class="sp-dashboard-footer-name">RITESH MANDAL</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )