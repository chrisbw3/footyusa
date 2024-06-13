import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title
import plotly.express as px
import plotly.graph_objects as go



import matplotlib.pyplot as plt
from highlight_text import fig_text
from mplsoccer import PyPizza, FontManager


st.set_page_config(page_icon=":soccer_ball:",
                   layout="wide")

font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                          'src/hinted/Roboto-Regular.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                          'src/hinted/Roboto-Italic.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                        'RobotoSlab[wght].ttf')

df = pd.read_csv('/footyusa/data/leagues/MLS/mlf.csv')
df2 = pd.read_csv('/footyusa/data/leagues/MLS/GSC.csv')
df3 = pd.read_csv('/footyusa/data/leagues/MLS/playing_time.csv')
df4 = pd.read_csv('/footyusa/data/leagues/MLS/passing.csv')
df5 = pd.read_csv('/footyusa/data/leagues/MLS/shooting.csv')

df2 = df2.rename(columns={'SCA_SCA90': 'SCA90', 'GCA_GCA90': 'GCA90'})

combined_df = pd.merge(df3, df2, on='Player', how='left')
combined_df = combined_df.fillna(0)


###sidebar section
st.sidebar.info('''Hey! Want to connect?   [**LinkedIn**](https://www.linkedin.com/in/christian-wl-gentry/)
                | [**Twitter**](https://twitter.com/_chocolatejuice?s=11)''')
selected_team_1 = st.sidebar.selectbox("Select Team", options=df["Home Team"].unique(), index=1)
st.sidebar.write(''':orange[DEMO STAGES.]
                 ''')

c1, c2 = st.columns([1,1.9])


with c1:
    st.title("The Weight of Possession")
    
    filtered_df1 = df[df['Home Team'] == selected_team_1]
    most_used_formation = filtered_df1['Formation'].mode().iloc[0]
    count_games = ((filtered_df1['GF'] > filtered_df1['xG']) & (filtered_df1['Poss'] < 50)).sum()
    count_games2 = ((filtered_df1['GF'] < filtered_df1['xG']) & (filtered_df1['Poss'] > 50)).sum()
    possession_txt = st.write('''Sometimes possession isn't always better. Depending on a team's playing style,
            formation, and opponent, a counter-attacking tactic might seal the deal rather than a
             possession-dominant game.''')
    formation_txt = st.metric(label=f"{selected_team_1}'s Most Common Formation", value=most_used_formation)
    poss_s_mls = st.metric(f'''The number of games where {selected_team_1}'s GF > xG and 
              Poss < 50''', value=count_games)
    poss_l_mls = st.metric(f'''The number of games where {selected_team_1}'s GF < xG and 
              Poss > 50''', value=count_games2)


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
    fig1_mls.update_layout(annotations=annotations)
    st.plotly_chart(fig1_mls, use_container_width=True)

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

c3, c4 = st.columns([1,1.9])
with c3:
    st.markdown("<h1 style='text-align: center;'>Shots & Goals</h1>", unsafe_allow_html=True)
    gsc_txt_mls = st.write('''Goal/shot creating actions are two offensive actions directly 
             leading to goals/shots, such as: passes, take-ons, and drawing fouls.''')
    additional_teams1 = st.multiselect("Select additional teams to compare.", combined_df['Team_x'].unique())
    selected_action_type = st.selectbox("Action Type", ['GCA90', 'SCA90'])
    selected_pos1 = st.multiselect("Select Positions", options=combined_df["POS_x"].unique(), default=combined_df["POS_x"].unique(), key = "pos1")
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

    
st.subheader("Additional Shooting Stats")   
with c4:    
    fig2_mls = px.scatter(filtered_combined_df, x='Playing Time_Min', y=selected_action_type, color='Team_x', size='MarkerSize', hover_data=['Player'])
    fig2_mls.update_traces(marker=dict(
                               line=dict(width=2,
                                         color='Coral')),
                  selector=dict(mode='markers'))
    fig2_mls.add_hline(y=filtered_combined_df[selected_action_type].mean(), line_color="Red")
    st.plotly_chart(fig2_mls, use_container_width=True)    





c13, c14 = st.columns(2)

with c13:

    filtered_df5 = df5[df5['Team'] == selected_team_1]
    filtered_df5_2 = df5[df5['Team'] == selected_team_1]
    filtered_players2 = df5[df5['Team'] == selected_team_1]
    selected_player_1 = st.selectbox("Select Player", filtered_players2, key=1)

    additional_teams1 = st.multiselect("Select Additional Teams", df5['Team'].unique(), key=2)


    all_selected_teams = [selected_team_1] + additional_teams1


    filtered_df5 = df5[df5['Team'].isin(all_selected_teams)]

    filtered_df5_2['color'] = 'blue'  # default color
    filtered_df5_2.loc[filtered_df5_2['Player'] == selected_player_1, 'color'] = 'red'

    fig4 = px.scatter(filtered_df5, x='Standard_Sh', y='Standard_SoT', color='Team',
                 hover_data=["Player", "Standard_Gls"],size='Standard_Gls')
    st.plotly_chart(fig4, use_container_width=True)
with c14:
    
    pizza_columns = df5[["Standard_Gls", "Standard_Dist", "Expected_np:G-xG"]].columns.tolist()

    values = filtered_df5_2[filtered_df5_2['Player'] == selected_player_1][pizza_columns].astype(int)

    
   # Filter out zeros and non-finite values
    filtered_df5_no_zeros = df5.replace(0, pd.NA).dropna()  
    filtered_df5_no_zeros = filtered_df5_no_zeros.dropna(subset=pizza_columns, how='all')

    # Convert NaN values to zeros
    filtered_df5_no_zeros[pizza_columns] = filtered_df5_no_zeros[pizza_columns].fillna(0)

    # Calculate league averages
    league_averages = filtered_df5_no_zeros[pizza_columns].mean().round().astype(int)
    values_2 = pd.Series(league_averages, index=pizza_columns)

  
    min_range = filtered_df5_2[pizza_columns].min().round(0).astype(int)
    max_range = filtered_df5_2[pizza_columns].max().round(0).astype(int)


    baker = PyPizza(
        params=pizza_columns,
        min_range=min_range,        
        max_range=max_range,        
        background_color="#ECE4AE", 
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
            color="#000000", fontsize=12, zorder=5,
            va="center"
        ),                          
        kwargs_values=dict(
            color="#000000", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="#1A78CF",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          
        kwargs_compare_values=dict(
            color="#000000", fontsize=12,
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
    ha="center", fontproperties=font_bold.prop, color="#000000"
)
 
    with st.spinner("Rendering..."):
        plt.savefig("radar_chart.png", dpi=90, bbox_inches='tight', pad_inches=0.2)

 
    st.image("radar_chart.png")


    plt.close(fig)


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
    neg_ass_txt_mls = st.metric(label=f"{selected_team_1}'s {format_string} with  A-xAG", value=negative_assists)


with c6:
    fig3_mls = px.bar(filtered_df4, x='Player', y='A-xAG', color='A-xAG',color_continuous_scale=px.colors.sequential.Viridis)

    st.plotly_chart(fig3_mls, use_container_width=True)




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
        background_color="#ECE4AE", 
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
            color="#000000", fontsize=12, zorder=5,
            va="center"
        ),                          
        kwargs_values=dict(
            color="#000000", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="#1A78CF",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          
        kwargs_compare_values=dict(
            color="#000000", fontsize=12,
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
    ha="center", fontproperties=font_bold.prop, color="#000000"
)
 
    with st.spinner("Rendering..."):
        plt.savefig("radar_chart.png", dpi=90, bbox_inches='tight', pad_inches=0.2)

 
    st.image("radar_chart.png")


    plt.close(fig)
