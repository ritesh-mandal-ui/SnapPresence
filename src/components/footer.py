import base64
from pathlib import Path
import streamlit as st


def get_image_base64():
  current_dir = Path(__file__).parent
  img_path = current_dir.parent / "assets" / "footer_logo.png"

  if img_path.exists():
    with open(img_path, "rb") as f:
      return base64.b64encode(f.read()).decode()
  return None


def footer_home():
  img_base64 = get_image_base64()
  if img_base64:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 40px; margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" style="width: 100%; max-width: 900px; border-radius: 8px;" />
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 40px; color: white; font-weight: bold; font-size: 1.2rem;">
            RITESH<br>MANDAL
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer_dashboard():
  img_base64 = get_image_base64()
  if img_base64:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 40px; margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" style="width: 100%; max-width: 900px; border-radius: 8px;" />
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 40px; color: black; font-weight: bold; font-size: 1.2rem;">
            RITESH<br>MANDAL
        </div>
        """,
        unsafe_allow_html=True,
    )