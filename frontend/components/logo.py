import streamlit as st

import re
import base64
import validators
from pathlib import Path

def add_logo(logo_url: str, height: int = 100, svg=False):

    if svg:
        svg_logo = read_svg(logo_url)
        b64 = base64.b64encode(svg_logo.encode("utf-8")).decode("utf-8")
        logo = f'url("data:image/svg+xml;base64,{b64}")'

    elif validators.url(logo_url):
        logo = f'url({logo_url})'
    else:
        logo = f'url("data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()}")'

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                background-position: center top; /* Center the logo at the top */
                background-size: auto {height}px; /* Set the logo height */
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def read_svg(path_svg):
    try:
        with open(path_svg, "r") as file:
            svg_logo = file.read().splitlines()
            _maped_list = map(str, svg_logo)
            svg_logo = "".join(_maped_list)
            temp_svg_logo = re.findall("<svg.*</svg>", svg_logo, flags=re.IGNORECASE)
            svg_logo = temp_svg_logo[0]
    except:
        svg_logo = '<svg xmlns="http://www.w3.org/2000/svg" width="150px" height="1px" viewBox="0 0 150 1"></svg>'
    return svg_logo

def render_svg(svg):
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = (
        r"""
        <div align="center">
        <img src="data:image/svg+xml;base64,%s" alt="Techdocs Logo" style="width: 60em;"/>
        </div>
        """
        % b64
    )
    st.markdown(html, unsafe_allow_html=True)