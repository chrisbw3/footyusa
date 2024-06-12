import streamlit as st 
import pandas as pd
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.let_it_rain import rain 


show_pages(
    [
        Page("/Users/christiangentry/Documents/Data_projects/footy/program_files/1_🏠_app.py", "Home", "🏠"),
        Page("/Users/christiangentry/Documents/Data_projects/footy/pages/2_🤖_About.py", "About", "🤖"),
        Page("/Users/christiangentry/Documents/Data_projects/footy/pages/3_🥇_MLS.py", "MLS", "🥇"),
        Page("/Users/christiangentry/Documents/Data_projects/footy/pages/4_🥈_USL-Championship.py", "USL Championship", "🥈"),
        Page("/Users/christiangentry/Documents/Data_projects/footy/pages/5_🥉_USL-1.py", "USL1", "🥉")
        ])
        


st.set_page_config(page_icon=":soccer_ball:",
                   layout="wide")

    )
###sidebar section
st.sidebar.write(''':orange[DEMO STAGES.]
                 ''')

st.sidebar.info('''Hey! Want to connect?   [**LinkedIn**](https://www.linkedin.com/in/christian-wl-gentry/)
                | [**Twitter**](https://twitter.com/_chocolatejuice?s=11)''')





st.header("FOOTY USA")



