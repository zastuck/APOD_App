import kaggle.api as api
import streamlit as st
import pandas as pd
import numpy as np
import tempfile
import datetime as dt
import random

st.set_page_config(layout="wide")

@st.cache_data
def load_data(repo:str, file:str):
    api.authenticate()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        api.dataset_download_file(repo, file, path=tmpdir)
        
        df = pd.read_csv(f"{tmpdir}/{file}")
    return df

# api.dataset_download_file("elvisbui/nasa-apod-archive-2000-2026/", "nasa_apod_archive_2000_2026.csv")


df = load_data(
    "elvisbui/nasa-apod-archive-2000-2026/",
    "nasa_apod_archive_2000_2026.csv"
)

years = list(df['year'].sort_values().unique())

st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url("https://apod.nasa.gov/apod/image/2504/PIA21983JupiterLundh.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center;'>NASA APOD Picture of the Day</h1>
    <h4 style='text-align: center;'>Select a date, year, or select a random photo from the NASA Astronomy Picture of the Day Archive (January 1, 2000 - April 24, 2026)</h4>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    date_select = st.date_input(
        "Select Date",
        value=None,
        min_value="2000-01-01",
        max_value="2026-04-24"
    )
with col2:
    year_select = st.selectbox(
        "Select a Year",
        options = years,
        index = None
    )
  
def get_APOD(date:str = None, year:int = None):
    if date:
        APOD = df[df['date'] == date].iloc[0].to_dict()
    elif year:
        APOD = df[df['year'] == year]
        APOD = APOD.sample(n=1).iloc[0].to_dict()
    else:
        APOD = df.sample(n=1).iloc[0].to_dict()
    
    return APOD
    
   
if "apod" in st.session_state:
    del st.session_state.apod     

@st.dialog(title=" ", width = "large")
def APOD_dialog():
    # Initialize session state
    if "apod" not in st.session_state:
        if date_select:
            st.session_state.apod = get_APOD(date=date_select.strftime("%Y-%m-%d"))
        elif year_select:
            st.session_state.apod = get_APOD(year=year_select)
        else:
            st.session_state.apod = get_APOD()
    
    apod = st.session_state.apod
    pub_date = dt.date.fromisoformat(apod['date'])
    
    st.space(size="small")
    

    st.markdown(
    f"""
    <div style="position: relative; display: flex; justify-content: center; width: 100%;">
        <img src="{apod['image_url']}" style="position=absolute; margin=auto; max-width: 100%; border-radius: 8px;">
        <div style="
            position: absolute;
            bottom: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.85));
            color: white;
            width: 100%;
            padding: 20px;
            box-sizing: border-box;
            border-radius: 0 0 8px 8px;
        ">
        <style>
            .apod-explanation {{
                display: block;
            }}
            @media (max-width: 768px) {{
                .apod-explanation {{
                    display: none;
                }}
            }}
        </style>
            <h4 style="margin: 0; line-height: 0.75; cursor: pointer;">{apod['title']}</h4>
            <h6 style="margin: 0 0 0.5vw 0; line-height: 0.75;">{pub_date.strftime("%A, %B %d, %Y")}</h6>
            <p class="apod-explanation" style="margin: 0; font-size: 0.7em; line-height: 1;">{apod['explanation']}</p>
            <p style="margin: 0; font-size: 0.7em; line-height: 0.75;">{apod['credit']}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    st.space(size="xxsmall")

    if st.button("🎲 Randomize 🎲", width="content"):
        del st.session_state.apod 
        if year_select:
            st.session_state.apod = get_APOD(year=year_select)
        else:
            st.session_state.apod = get_APOD()
        st.rerun(scope="fragment")

if st.button("🎲 Select/Randomize 🎲", width="stretch"):
    APOD_dialog()



