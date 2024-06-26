import streamlit as st 
import pandas as pd
from st_pages import Page, show_pages, add_page_title



show_pages(
    [
        Page("1_🏠_app.py", "Home", "🏠"),
        Page("pages/2_🤖_About.py", "About", "🤖"),
        Page("pages/3_🥇_MLS.py", "MLS", "🥇"),
        Page("pages/4_🥈_USL-Championship.py", "USL Championship", "🥈"),
        Page("pages/5_🥉_USL-1.py", "USL1", "🥉")
        ])
        


st.set_page_config(page_icon=":soccer_ball:",
                   layout="wide")

###sidebar section
st.sidebar.write(''':orange[DEMO STAGES.]
                 ''')

st.sidebar.info('''Hey! Want to connect?   [**LinkedIn**](https://www.linkedin.com/in/christian-wl-gentry/)
                | [**Twitter**](https://twitter.com/_chocolatejuice?s=11)''')





st.header("FOOTY USA")

st.write("A data app to explore USA soccer stats and transform boring tables into visualizations. See the sidebar for MLS stats. USL stats coming soon.")
st.image("screenshot.png")

