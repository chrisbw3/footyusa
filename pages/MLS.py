import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from fpdf import FPDF
import tempfile
import os
import matplotlib.pyplot as plt
from highlight_text import fig_text
from mplsoccer import PyPizza, FontManager

st.set_page_config(page_icon=":soccer_ball:",
                   layout="wide")



show_pages(
    [
        Page("/Users/christiangentry/Documents/Data_projects/footy/program_files/app.py", "Home", "🏠"),
        Page("/Users/christiangentry/Documents/Data_projects/footy/pages/About.py", "About", "🤖"),
        Page("/Users/christiangentry/Documents/Data_projects/footy/pages/MLS.py", "MLS", "🥇"),
        Page("/Users/christiangentry/Documents/Data_projects/footy/pages/USL-Championship.py", "USL Championship", "🥈"),
        Page("/Users/christiangentry/Documents/Data_projects/footy/pages/USL-1.py", "USL1", "🥉")
        ])



font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                          'src/hinted/Roboto-Regular.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                          'src/hinted/Roboto-Italic.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                        'RobotoSlab[wght].ttf')


df = pd.read_csv('/Users/christiangentry/Documents/Data_projects/footy/data/leagues/MLS/mlf.csv')
df2 = pd.read_csv('/Users/christiangentry/Documents/Data_projects/footy/data/leagues/MLS/GSC.csv')
df3 = pd.read_csv('/Users/christiangentry/Documents/Data_projects/footy/data/leagues/MLS/playing_time.csv')
df4 = pd.read_csv('/Users/christiangentry/Documents/Data_projects/footy/data/leagues/MLS/passing.csv')
df5 = pd.read_csv('/Users/christiangentry/Documents/Data_projects/footy/data/leagues/MLS/shooting.csv')
df6 = pd.read_csv('/Users/christiangentry/Documents/Data_projects/footy/data/leagues/MLS/possession.csv')
df2 = df2.rename(columns={'SCA_SCA90': 'SCA90', 'GCA_GCA90': 'GCA90'})

combined_df = pd.merge(df3, df2, on='Player', how='left')
combined_df = combined_df.fillna(0)



###sidebar section
st.sidebar.info('''Want to connect? Follow for updates:
                 [**Twitter**](https://x.com/_footyusa)''')
def team_selection():
    selected_team_1 = st.sidebar.selectbox("Select Team", options=df["Home Team"].unique(), index=1)
    return selected_team_1
selected_team_1 = team_selection()



c1, c2 = st.columns([1,1.4])


with c1:
    st.title("The Weight of Possession")
    
    filtered_df1 = df[df['Home Team'] == selected_team_1]
    most_used_formation = filtered_df1['Formation'].mode().iloc[0]
    count_games = ((filtered_df1['GF'] > filtered_df1['xG']) & (filtered_df1['Poss'] < 50)).sum()
    count_games2 = ((filtered_df1['GF'] < filtered_df1['xG']) & (filtered_df1['Poss'] > 50)).sum()
    possession_txt = st.write('''Sometimes possession isn't always better. Depending on a team's playing style,
            formation, and opponent, a counter-attacking tactic might seal the deal rather than a
             possession-dominant game.''')
    fig1_formation_txt = st.metric(f"{selected_team_1}'s Most Common Formation", value=most_used_formation)
    fig1_txt_1 = st.write(f'''The number of games where {selected_team_1}'s GF > xG and 
           Poss < 50''')
    st.subheader(count_games)

    fig1_txt_2 = st.write(f'''The number of games where {selected_team_1}'s GF < xG and 
              Poss > 50''')
    st.subheader(count_games2)


with c2:  
    filtered_df1 = df[df['Home Team'] == selected_team_1]
    
    fig1_mls = px.scatter(filtered_df1, x='Poss', y='GF', hover_data=['Home Team', 'Formation'])
    line_trace = px.scatter(filtered_df1, x='Poss', y='xG', color_discrete_sequence=['red']).data[0]
    fig1_mls.add_trace(line_trace)

    
    annotations = []
    for i in range(len(filtered_df1)):
        x_val = filtered_df1['Poss'].iloc[i]
        primary_y_val = filtered_df1['GF'].iloc[i]
        secondary_y_val = filtered_df1['xG'].iloc[i]

        if secondary_y_val > primary_y_val:
            arrow_y = primary_y_val + (secondary_y_val - primary_y_val) / 2
            arrow_direction = 'up'
            ay = -20  # Arrow pointing up
            arrow_color = 'red'
        else:
            arrow_y = secondary_y_val + (primary_y_val - secondary_y_val) / 2
            arrow_direction = 'down'
            ay = 20  # Arrow pointing down
            arrow_color = 'green'
        
        annotations.append(
            go.layout.Annotation(
                x=x_val,
                y=arrow_y,
                xref='x',
                yref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=arrow_color,
                ax=0,
                ay=ay,
                text=''
            )
        )
    fig1_mls.update_layout(annotations=annotations,
    plot_bgcolor='rgba(0, 0, 0, 0)', 
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    font=dict(
        color="white"
    ),
    xaxis=dict(
        showgrid=False 
    )
)
    fig1_mls.update_traces(marker=dict(color='lightblue'))
    st.plotly_chart(fig1_mls, use_container_width=True)



    





c15, c16 = st.columns(2)

with c15:
    st.header("Advanced Possession Analysis")
    preference = st.radio("",["Selected Team Top 5", "Custom Selection (Select players)"])
    columns=["Touches_Def 3rd", "Touches_Mid 3rd", "Touches_Att 3rd", "Take-Ons_Att", "Carries_PrgC", "Carries_Mis", "Carries_Dis"]
    stat = st.selectbox("Select Stat", options=columns,index=2)

    if preference == "Custom Selection (Select players)":
        selected_player_2 = st.multiselect("Select Players", df6['Player'].tolist(), default='Luciano Acosta')
    else: (f"{selected_team_1} is selected (see sidebar).")


with c16:
    if preference == "Custom Selection (Select players)":
        if selected_player_2 and stat:
            filtered_df = df6[df6['Player'].isin(selected_player_2)]
            fig5_mls = px.bar(filtered_df, x='Player', y=stat, color_continuous_scale=px.colors.sequential.Viridis)
        else:
            st.write("No players/stat selected.")
            fig5_mls = None
    else:
        if stat:    
            filtered_df = df6[df6['Team'] == selected_team_1]
            filtered_df = filtered_df.nlargest(5, stat)
            fig5_mls = px.bar(filtered_df, x='Player', y=stat)
        else:
            st.write("No stat selected.")
            fig5_mls=None
    
    if fig5_mls:
        st.plotly_chart(fig5_mls, use_container_width=True)

    fig5_mls.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)', 
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    font=dict(color="white"))
    fig5_mls.update_traces(marker_color='blue', selector=dict(type='bar'))

st.divider()
c9, c10 = st.columns([1,1])

with c9:
    st.title("Game Outcomes")
    st. write('''There are some opponents who seem to always win (or lose) against your team. 
              Have you ever asked yourself if this is really your team's fifth game winning 2-1? Not only do
              the mix of team tactics leave potential repeats of game outcome, but so do form & luck against opponents.''')


with c10:
    heatmap = px.density_heatmap(filtered_df1, x='GA', y='GF', nbinsx=10, nbinsy=10, color_continuous_scale=px.colors.diverging.Tealrose)
    heatmap.update_yaxes(tickformat=".1f")
    heatmap.update_yaxes(tickvals=filtered_df1['GF'], ticktext=list(map(int, filtered_df1['GF'])))
    heatmap.update_xaxes(tickvals=filtered_df1['GF'], ticktext=list(map(int, filtered_df1['GF'])))
    st.plotly_chart(heatmap, use_container_width=True)

    heatmap.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)', 
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    font=dict(
        color="white"
    ),
    xaxis=dict(
        showgrid=False 
    )
)





st.divider()
c3, c4 = st.columns([1,1.9])
with c3:
    st.markdown("<h1 style='text-align: center;'>Shots & Goals</h1>", unsafe_allow_html=True)
    gsc_txt_mls = st.write('''Goal/shot creating actions are two offensive actions directly 
             leading to goals/shots, such as: passes, take-ons, and drawing fouls.''')
    additional_teams1 = st.multiselect("Select additional teams to compare.", combined_df['Team_x'].unique())
    selected_action_type = st.selectbox("Action Type", ['GCA90', 'SCA90'])
    selected_pos1 = st.multiselect("Select Positions", options=combined_df["POS_x"].unique(), default=combined_df["POS_x"].unique(), key="pos1")
    additional_teams1 = [selected_team_1] + additional_teams1
    filtered_combined_df = combined_df[(combined_df['Team_x'].isin(additional_teams1)) & (combined_df['POS_x'].isin(selected_pos1))]

    def get_marker_size(row):
        if row['Playing Time_MP'] and row['Playing Time_MP'] != 0:
            return row['Playing Time_MP']
        else:
            return row['MP']

    filtered_combined_df['MarkerSize'] = filtered_combined_df.apply(get_marker_size, axis=1)
    players_to_remove = st.multiselect("Select players to remove outlier data", filtered_combined_df['Player'].unique())
    filtered_combined_df = filtered_combined_df[~filtered_combined_df['Player'].isin(players_to_remove)]
with c4:
    fig2_mls = px.scatter(filtered_combined_df, x='Playing Time_Min', y=selected_action_type, color='Team_x', size='MarkerSize', hover_data=['Player'],
                        color_discrete_map={team: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, team in enumerate(additional_teams1)})
    fig2_mls.update_traces(marker=dict(
                            line=dict(width=2,
                                        color='Coral')),
                selector=dict(mode='markers'))
    fig2_mls.add_hline(y=filtered_combined_df[selected_action_type].mean(), line_color="Red")

    fig2_mls.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        font=dict(
            color="white"
        ),
        xaxis=dict(
            showgrid=False 
        )
    )
    st.plotly_chart(fig2_mls, use_container_width=True)   

    

st.subheader("Additional Shooting Stats")  
c13, c14 = st.columns(2)

with c13:
    filtered_df3 = df3[['Player', 'Playing Time_Min']]
    df5 = pd.merge(filtered_df3, df5, on='Player', how='left')
    df5.columns = df5.columns.str.strip()
    filtered_df5 = df5[df5['Team'] == selected_team_1]
    filtered_df5_2 = df5[df5['Team'] == selected_team_1]
    filtered_players2 = df5[df5['Team'] == selected_team_1]
    selected_player_1 = st.selectbox("Select Player", filtered_players2, key=1)

    additional_teams1 = st.multiselect("Select Additional Teams", df5['Team'].unique(), key=2)

    all_selected_teams = [selected_team_1] + additional_teams1
    filtered_df5 = df5[df5['Team'].isin(all_selected_teams)]

    fig4_mls = px.scatter(filtered_df5, x='Standard_Sh', y='Standard_SoT', color='Team',
                        hover_data=["Player", "Standard_Gls"], size='Standard_Gls',
                        color_discrete_map={team: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, team in enumerate(all_selected_teams)})
    fig4_mls.update_traces(marker=dict(
                            line=dict(width=2,
                                        color='Coral')),
                selector=dict(mode='markers'))
    fig4_mls.add_hline(y=filtered_df5['Standard_SoT'].mean(), line_color="Red")

    fig4_mls.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        font=dict(
            color="white"
        ),
        xaxis=dict(
            showgrid=False 
        )
    )

    st.plotly_chart(fig4_mls, use_container_width=True)
with c14:
    
    pizza_columns = df5[["Standard_Gls", "Standard_Dist", "Expected_np:G-xG", "Playing Time_Min"]].columns.tolist()
      
    filtered_df5_no_zeros = df5.dropna(subset=pizza_columns, how='all')

    # Convert NaN values to zeros
    filtered_df5_no_zeros[pizza_columns] = filtered_df5_no_zeros[pizza_columns].fillna(0)

    # Calculate league averages
    league_averages = filtered_df5_no_zeros[pizza_columns].mean().round().astype(int)
    values_2 = pd.Series(league_averages, index=pizza_columns)

    values = filtered_df5_no_zeros[filtered_df5_no_zeros['Player'] == selected_player_1][pizza_columns].astype(int)
  
    min_range = filtered_df5_no_zeros[pizza_columns].min().round(0).astype(int)
    max_range = filtered_df5_no_zeros[pizza_columns].max().round(0).astype(int)


    baker = PyPizza(
        params=pizza_columns,
        min_range=min_range,        
        max_range=max_range,        
        background_color="#060b16", 
        straight_line_color="#000000",
        last_circle_color="#000000", 
        last_circle_lw=2.5, 
        other_circle_lw=0,
        other_circle_color="#000000", 
        straight_line_lw=1
    )

   
    fig, ax = baker.make_pizza(
        values.values[0],         
        compare_values=values_2,   
        figsize=(8,7),              
        color_blank_space="same",   
        blank_alpha=0.4,         
        param_location=110,        
        kwargs_slices=dict(
            facecolor="#1A78CF", edgecolor="#000000",
            zorder=1, linewidth=1
        ),                          
        kwargs_compare=dict(
            facecolor="#ff9300", edgecolor="#222222", zorder=3, linewidth=1,
        ),                          
        kwargs_params=dict(
            color="#ffffff", fontsize=12, zorder=5,
            va="center"
        ),                          
        kwargs_values=dict(
            color="#ffffff", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="#1A78CF",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          
        kwargs_compare_values=dict(
            color="#ffffff", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="#FF9300",
                boxstyle="round,pad=0.2", lw=1
            )
        )                            
    )

    fig_text(
    0.515, 0.99, f"<{selected_player_1}'s Shooting> vs <League Average>", size=17, fig=fig,
    highlight_textprops=[{"color": '#1A78CF'}, {"color": '#EE8900'}],
    ha="center", fontproperties=font_bold.prop, color="#ffffff"
)
 
    with st.spinner("Rendering..."):
        plt.savefig("radar_chart1.png", dpi=90, bbox_inches='tight', pad_inches=0.2)

 
    st.image("radar_chart1.png")
    st.write("*Excluding players with no contributing stats.")

    plt.close(fig)

st.divider()
c5, c6 = st.columns([1,1.9])
with c5:
    st.title("Key Passes")
    selected_pos2 = st.multiselect("Select Positions", options=df4["POS"].unique(), default=df4["POS"].unique(), key = "pos2")
    filtered_df4 = df4[(df4['Team'] == selected_team_1) & (df4['POS'].isin(selected_pos2))]
    filtered_df4 = filtered_df4[filtered_df4['A-xAG'] != 0]
   

    positive_assists = ((filtered_df4['A-xAG'] > 0)).sum()
    negative_assists = ((filtered_df4['A-xAG'] < 0)).sum()

    ass_txt_mls = st.write('''Measuring assists-exprected assisted goals may not only reveal a player's ability to deliver key passes, 
             but also may tell a story of their luck (or lack thereof) with strikers' abilities.''')
    
    format_string = ""


    if selected_pos2:
        format_string = f"{', '.join(selected_pos2)}'s"
    else:
        format_string = "No values selected."


    pos_ass_txt_mls = st.metric(label=f"{selected_team_1}'s {format_string} with + A-xAG", value=positive_assists)
    neg_ass_txt_mls = st.metric(label=f"{selected_team_1}'s {format_string} with - A-xAG", value=negative_assists)


with c6:
    fig3_mls = px.bar(filtered_df4, x='Player', y='A-xAG', color='A-xAG',color_continuous_scale=px.colors.sequential.Viridis)

    st.plotly_chart(fig3_mls, use_container_width=True)

    fig3_mls.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)', 
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    font=dict(
        color="white"
    ),
    xaxis=dict(
        showgrid=False 
    )
)






#############################################################
c11, midc, c12 = st.columns((1, 0.3, 1.5))

with c11:
    filtered_players = df4[df4['Team'] == selected_team_1]['Player'].unique()
    selected_player_1 = st.selectbox("Select Player", filtered_players)
    st.write('''**Assists - Expected Assisted Goals** & It's Correlation With Team Success/90' (goals scored while the player
             was on the field - goals allowed while player was off the field.)''')
    
    combined_df2 = pd.merge(df3, df4, on='Player', how='left')
    combined_df2 = combined_df2.rename(columns={'Team Success_+/-': 'Success +/-'})
    filtered_combined_df2 = combined_df2[['Player', 'A-xAG', 'Success +/-', 'POS_x']]
    filtered_combined_df2['Sum'] = filtered_combined_df2[['Success +/-', 'A-xAG']].sum(axis=1)
    filtered_combined_df2['Rank'] = filtered_combined_df2['Sum'].rank(method='max', ascending=False).astype(int)
    filtered_combined_df2 = filtered_combined_df2.nsmallest(10, 'Rank')[['Player', 'A-xAG', 'Success +/-', 'POS_x', 'Rank']]

    st.dataframe(filtered_combined_df2, use_container_width=True, hide_index=True)

with midc:
    st.write()

with c12:
    pizza_columns = ["Total_Cmp", "Total_Att", "Total_Cmp%", "Short_Cmp%", "Medium_Cmp%", "Long_Cmp%"]


    values = df4[df4['Player'] == selected_player_1][pizza_columns].astype(int)

    
    league_averages = df4[pizza_columns].mean().round(0).astype(int)
    values_2 = pd.Series(league_averages, index=pizza_columns)  

  
    min_range = df4[pizza_columns].min().round(0).astype(int)
    max_range = df4[pizza_columns].max().round(0).astype(int)


    baker = PyPizza(
        params=pizza_columns,
        min_range=min_range,        
        max_range=max_range,        
        background_color="#040b16", 
        straight_line_color="#000000",
        last_circle_color="#000000", 
        last_circle_lw=2.5, 
        other_circle_lw=0,
        other_circle_color="#000000", 
        straight_line_lw=1
    )

   
    fig, ax = baker.make_pizza(
        values.values[0],         
        compare_values=values_2,   
        figsize=(8,7),              
        color_blank_space="same",   
        blank_alpha=0.4,         
        param_location=110,        
        kwargs_slices=dict(
            facecolor="#1A78CF", edgecolor="#000000",
            zorder=1, linewidth=1
        ),                          
        kwargs_compare=dict(
            facecolor="#ff9300", edgecolor="#222222", zorder=3, linewidth=1,
        ),                          
        kwargs_params=dict(
            color="#ffffff", fontsize=12, zorder=5,
            va="center"
        ),                          
        kwargs_values=dict(
            color="#ffffff", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="#1A78CF",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          
        kwargs_compare_values=dict(
            color="#ffffff", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="#FF9300",
                boxstyle="round,pad=0.2", lw=1
            )
        )                            
    )

    fig_text(
    0.515, 0.99, f"<{selected_player_1}'s Passing> vs <League Average>", size=17, fig=fig,
    highlight_textprops=[{"color": '#1A78CF'}, {"color": '#EE8900'}],
    ha="center", fontproperties=font_bold.prop, color="#ffffff"
)
 
    with st.spinner("Rendering..."):
        plt.savefig("radar_chart2.png", dpi=90, bbox_inches='tight', pad_inches=0.2)

 
    st.image("radar_chart2.png")


    plt.close(fig)

@st.cache_data(show_spinner=False)
def gen_cache_imgs(fig1_mls, fig2_mls, heatmap, fig3_mls, fig5_mls, fig4_mls):
    image_paths = []
    
    # Save fig1_mls as image
    if fig1_mls:
        fig1_path = save_image_to_tempfile(fig1_mls)
        image_paths.append(fig1_path)
    else:
        st.warning("fig1_mls is None. Skipping.")

    # Save fig2_mls as image
    if fig2_mls:
        fig2_path = save_image_to_tempfile(fig2_mls)
        image_paths.append(fig2_path)
    else:
        st.warning("fig2_mls is None. Skipping.")

    # Save heatmap as image
    if heatmap:
        heatmap_path = save_image_to_tempfile(heatmap)
        image_paths.append(heatmap_path)
    else:
        st.warning("heatmap is None. Skipping.")

    # Save fig3_mls as image
    if fig3_mls:
        fig3_path = save_image_to_tempfile(fig3_mls)
        image_paths.append(fig3_path)
    else:
        st.warning("fig3_mls is None. Skipping.")

    # Save fig5_mls as image
    if fig5_mls:
        fig5_path = save_image_to_tempfile(fig5_mls)
        image_paths.append(fig5_path)
    else:
        st.warning("fig5_mls is None. Skipping.")

    # Save fig4_mls as image
    if fig4_mls:
        fig4_path = save_image_to_tempfile(fig4_mls)
        image_paths.append(fig4_path)
    else:
        st.warning("fig4_mls is None. Skipping.")

    return image_paths

# Example function to save plotly figures as images
def save_image_to_tempfile(fig):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        pio.write_image(fig, tmp_file.name)
        return tmp_file.name

# Custom PDF class
class CustomPDF(FPDF):
    def set_title(self, title):
        self.title = title

    def header(self):
        self.set_fill_color(5, 9, 22)
        self.rect(0, 0, self.w, self.h, style='F')
        
        # Set text color to white
        self.set_text_color(255, 255, 255)
        
        # Add logo to the top right corner
        logo_path = 'fulllogo_nobuffer.png'  # Update with your actual logo path
        self.image(logo_path, self.w - 30, 10, 20)  # Adjust x, y, width as needed

        # Set font for the header
        self.set_font('Arial', 'B', 12)
        
        # Add title text centered in the header
        self.set_xy(0, 10)
        self.cell(self.w, 10, self.title, 0, 0, 'C')
        self.ln(10)

    def footer(self, text=None):
        self.set_y(-33)
        self.set_text_color(200, 200, 200)  
        self.set_font('Arial', 'I', 8)
        if text:
            self.cell(20, 12, text, 0, 0, 'L')
        else:
            self.cell(20, 40, 'Page %s' % self.page_no(), 0, 0, 'C')

    def add_text_block(self, x, y, content, options=None):
        if options:
            family = options.get('family', 'Arial')
            size = options.get('size', 12)
            style = options.get('style', '')
            self.set_font(family, style, size)
        self.set_xy(x, y)
        self.multi_cell(0, 10, content)

    def add_image_with_subhead(self, x, y, image_path, subhead, column_width):
        self.set_font('Arial', 'B', 12)
        line_height = 10  # Height of each line of text
        max_lines = 2  # Maximum lines allowed for subheading

        # Calculate subheading height
        subhead_height = min(len(subhead.split('\n')), max_lines) * line_height

        # Calculate y position for subheading
        self.set_xy(x, y)
        self.multi_cell(column_width, line_height, subhead, 0, 'C')

        # Calculate y position for image
        image_height = 80  # Assuming image height is 80, adjust as necessary
        y += subhead_height + 10  # Adjust 10 for spacing between subhead and image

        # Calculate x position for image
        x_image = x + (column_width - 80) / 2

        # Add image
        self.image(image_path, x_image, y, 80, 0)

        # Update y position after adding image
        y += image_height

        # Set current position to the bottom of the image
        self.set_y(y)

def generate_report(selected_team_1, preference, selected_player_2, stat, selected_action_type):
    pdf = CustomPDF()
    pdf.set_title(f"{selected_team_1} Team Report")  # Set the title using a method or attribute

    pdf.add_page()

    # Set default font and text color
    default_font_family = 'Arial'
    default_font_size = 12
    pdf.set_font(default_font_family, size=default_font_size)
    pdf.set_text_color(255, 255, 255)

    # Define column positions
    left_column_x = 10
    right_column_x = 110
    column_y = 30
    column_width = 80

    pio.write_image(fig1_mls, "fig1_mls.png")
    pio.write_image(fig2_mls, "fig2_mls.png")
    pio.write_image(heatmap, "heatmap.png")
    pio.write_image(fig3_mls, "fig3_mls.png")
    pio.write_image(fig5_mls, "fig5_mls.png")
    pio.write_image(fig4_mls, "fig4_mls.png") 

    image_paths = gen_cache_imgs(fig1_mls, fig2_mls, heatmap, fig3_mls, fig5_mls, fig4_mls)

    # Add images to PDF report
    for image_path in image_paths:
        pdf.add_image_with_subhead(left_column_x, column_y + 5, image_path, "Subheading", column_width)

    pdf.footer('@_FootyUSA')

    # Save PDF to temporary file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        pdf_output_path = tmp_file.name
        pdf.output(pdf_output_path)

    return pdf_output_path

def main():
    # Example parameters for generate_report function
    selected_team_1 = "Team A"
    preference = "Custom Selection (Select players)"
    selected_player_2 = ["Player 1", "Player 2"]
    stat = "Some Stat"
    selected_action_type = "Some Action Type"

    # Button to generate report
    if st.sidebar.button("Generate Report"):
        pdf_output_path = generate_report(selected_team_1, preference, selected_player_2, stat, selected_action_type)
        st.sidebar.markdown(f"Download your report [here]({pdf_output_path})")

if __name__ == "__main__":
    main()