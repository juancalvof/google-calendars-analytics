import streamlit as st
from PIL import Image
from gca_page_1 import gca_page_1
from gca_page_2 import gca_page_2
from gca_page_3 import gca_page_3

st.beta_set_page_config("GOOGLE CALENDARS ANALYTICS", ":calendar:", "wide", "auto")

pages = {
    "PAGE 1: GENERAL ANALYSIS (ALL CALENDARS)": gca_page_1,
    "PAGE 2: SPECIFIC ANALYSIS (1 CALENDAR)": gca_page_2,
    "PAGE 3: GENERAL ANALYSIS (ALL CALENDARS)": gca_page_3
}

# Sidebar
image = Image.open('IMAGES/google_calendar.jpg')
st.sidebar.image(image, width=150)
st.sidebar.title(f"GOOGLE CALENDARS ANALYTICS")
selected_demo = st.sidebar.radio("SELECT A PAGE:", list(pages.keys()))
st.sidebar.write(f"---")

# Render pages
with st.spinner(f"LOAADING {selected_demo} ..."):
    pages[selected_demo]()

