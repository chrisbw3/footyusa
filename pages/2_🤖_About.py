import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title


###sidebar section

st.sidebar.info('''Hey! Want to connect?   [**LinkedIn**](https://www.linkedin.com/in/christian-wl-gentry/)
                | [**Twitter**](https://twitter.com/_chocolatejuice?s=11)''')
selected_team_1 = st.sidebar.selectbox("Select Team", options=df["Home Team"].unique(), index=1)
st.sidebar.write(''':orange[DEMO STAGES.]
                 ''')
