import streamlit as st

from supabase import Client, ClientOptions, create_client

from src.database.auth_storage import StreamlitCookieStorage


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