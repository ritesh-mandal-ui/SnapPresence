import base64
from pathlib import Path
import streamlit as st


def get_image_base64():
  # Get the absolute path of the current file (footer.py)
  current_dir = Path(__file__).parent
  # Navigate to src/assets/footer_logo.png
  img_path = current_dir.parent / "assets" / "footer_logo.png"

  if img_path.exists():
    with open(img_path, "rb") as f:
      return base64.b64encode(f.read()).decode()
  return None


def footer_home():
  img_base64 = get_image_base64()
  img_tag = (
      f'<img src="data:image/png;base64,{img_base64}" style="max-height:25px" />'
      if img_base64
      else '<span style="color:white; font-weight:bold;">RITESH MANDAL</span>'
  )

  st.markdown(
      f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-items:center">
        <p style="font-weight:bold; color:white;"> Created with ❤️ by </p>  
        {img_tag}
        </div>
        """,
      unsafe_allow_html=True,
  )


def footer_dashboard():
  img_base64 = get_image_base64()
  img_tag = (
      f'<img src="data:image/png;base64,{img_base64}" style="max-height:25px" />'
      if img_base64
      else '<span style="color:black; font-weight:bold;">RITESH MANDAL</span>'
  )

  st.markdown(
      f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-items:center">
        <p style="font-weight:bold; color:black;"> Created with ❤️ by </p>  
        {img_tag}
        </div>
        """,
      unsafe_allow_html=True,
  )