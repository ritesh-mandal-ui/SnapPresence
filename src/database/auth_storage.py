import streamlit as st

from streamlit_cookies_controller import CookieController


class StreamlitCookieStorage:

    def __init__(self):
        self.cookies = CookieController(
            key="supabase_auth"
        )

    def get_item(self, key):
        try:
            return self.cookies.get(key)
        except Exception:
            return None

    def set_item(self, key, value):
        self.cookies.set(
            key,
            value,
            max_age=3600,
            same_site="lax"
        )

    def remove_item(self, key):
        try:
            self.cookies.remove(key)
        except Exception:
            pass