import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title
st.set_page_config(page_icon=":soccer_ball:")


###sidebar section

st.sidebar.info('''Want to connect? Follow for updates:  
             [**Twitter**](https://x.com/_footyusa)''')

#st.image("/Users/christiangentry/Downloads/Footy USA/fulllogo_transparent_nobuffer.png", use_column_width=True, width=200)
st.markdown(
    f'<div style="display: flex; justify-content: center;">'
    f'<img src="/Users/christiangentry/Downloads/Footy USA/fulllogo_transparent_nobuffer.png" style="width: 50%;">'
    f'</div>',
    unsafe_allow_html=True
)
st.markdown("<h1 style='text-align: center;'>Vision</h1>", unsafe_allow_html=True)


st.write('''Soccer in the United States is on the rise. With more fans joining the game, lower divisions gaining stronger support, and
         the rise of European stars coming to play here, there's been no better time to start watching like now. For many,
         there's nothing better than casually supporting your club, but for others there's a curiosity to dig deeper. Footy USA
         is a platform to dive into sports statistics for soccer across the country. From gathering data from multiple sources
         to transforming numbers into digestable visualizations and graphing, your journey to understanding the game at a deeper level starts here.''')
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader("Structure & Design")
    st.write('''This project combines league, team, and players data across multiple sources for the MLS, USL Championship, and USL League 1.
             Currently only MLS is available, with USL stats in the works.''')
    st.write(" [Follow Footy USA on X for updates](https://x.com/_footyusa).")
    st.write("[View the github repository here.](https://github.com/chrisbw3/FootyUSA)")

with col2:
    st.subheader("Tools")
    st.write('''Users have a range of options to plot scatter, bar, and radar graphs along with heatmaps. Customize selections
             by adding additional teams for camparative analysis, remove outlier players, and group players by primary positions.''')
st.divider()
col3, col4 = st.columns(2)

with col3:
    st.image('/Users/christiangentry/Downloads/IMG_0050.JPG', caption='Meeting my FCC hero, Emmanuel Ledesma')

with col4:
    st.write('''I went to my first FC Cincinnati game in 2017, during the last visit from the Rochester Rhinos.
             That year is rich in history for long time fans of the club, and
             feeling pure energy and connection with the team made my dreams
             of supporting my local team a reality.''')
                                  
    st.write('''Through the ups and downs, this club
             has and will always be a part of me.
             I felt the passion to blend my love for the club 
         with my ambitions in working with data.''')
    st.write('''Cincy 'til I die!''')
  
