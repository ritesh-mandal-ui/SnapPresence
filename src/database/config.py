import streamlit as st

from supabase import Client, ClientOptions, create_client

from src.database.auth_storage import StreamlitCookieStorage


# Normal client: preserve the existing teacher Auth session.
auth_storage = StreamlitCookieStorage()

supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"],
    options=ClientOptions(
        flow_type="pkce",
        storage=auth_storage,
        persist_session=True
    )
)


# Privileged client: server-side use only.
# Never expose this client or its key to browser-side code.
supabase_admin: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_SECRET_KEY"],
    options=ClientOptions(
        auto_refresh_token=False,
        persist_session=False
    )
)
