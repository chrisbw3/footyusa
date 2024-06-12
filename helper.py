import pandas as pd
import schedule
import time


def retrieve_play_time_24_MLS(urls, team_names):
    all_data = []

    for url, team_name in zip(urls, team_names):
        df = pd.read_html(url, attrs = {"id":"stats_playing_time_22"})[0]
        time.sleep(3)
        #flatten multiindex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() for col in df.columns.values]
        else:
            df.columns = df.columns
        df.rename(columns={'Unnamed: 0_level_0_Player': 'Player', 'Unnamed: 1_level_0_Nation': 'Nation',
                           'Unnamed: 2_level_0_Pos': 'POS', 'Unnamed: 3_level_0_Age': 'Age', 'Unnamed: 4_level_0_90s': '90s',
                           'Unnamed: 4_level_0_MP': 'MP'}, inplace=True)
        df['Nation'] = df['Nation'].str.slice(3)

        df = df[~df['Player'].isin(['Squad Total', 'Opponent Total'])]
        df['POS'] = df['POS'].str.slice(0, 2)
        df['Age'] = df['Age'].str.slice(0, 2)
        df['Team'] = team_name
        all_data.append(df)
        df.drop('Unnamed: 26_level_0_Matches', axis=1, inplace=True)
        
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('playing_time.csv', index=False)


urls = [
     'https://fbref.com/en/squads/cb8b86a2/Inter-Miami-Stats',
    'https://fbref.com/en/squads/e9ea41b2/FC-Cincinnati-Stats',
    'https://fbref.com/en/squads/64e81410/New-York-City-FC-Stats',
    'https://fbref.com/en/squads/529ba333/Columbus-Crew-Stats',
    'https://fbref.com/en/squads/69a0fb10/New-York-Red-Bulls-Stats',
    'https://fbref.com/en/squads/130f43fa/Toronto-FC-Stats',
    'https://fbref.com/en/squads/eb57545a/Charlotte-FC-Stats',
    'https://fbref.com/en/squads/46024eeb/Philadelphia-Union-Stats',
    'https://fbref.com/en/squads/44117292/DC-United-Stats',
    'https://fbref.com/en/squads/46ef01d0/Orlando-City-Stats',
    'https://fbref.com/en/squads/35f1b818/Nashville-SC-Stats',
    'https://fbref.com/en/squads/1ebc1a5b/Atlanta-United-Stats',
    'https://fbref.com/en/squads/fc22273c/CF-Montreal-Stats',
    'https://fbref.com/en/squads/f9940243/Chicago-Fire-Stats',
    'https://fbref.com/en/squads/3c079def/New-England-Revolution-Stats',
    'https://fbref.com/en/squads/f7d86a43/Real-Salt-Lake-Stats',
    'https://fbref.com/en/squads/81d817a3/Los-Angeles-FC-Stats',
    'https://fbref.com/en/squads/99ea75a6/Minnesota-United-Stats',
    'https://fbref.com/en/squads/d8b46897/LA-Galaxy-Stats',
    'https://fbref.com/en/squads/ab41cb90/Vancouver-Whitecaps-FC-Stats',
    'https://fbref.com/en/squads/b918956d/Austin-FC-Stats',
    'https://fbref.com/en/squads/0d885416/Houston-Dynamo-Stats',
    'https://fbref.com/en/squads/415b4465/Colorado-Rapids-Stats',
    'https://fbref.com/en/squads/d076914e/Portland-Timbers-Stats',
    'https://fbref.com/en/squads/6218ebd4/Seattle-Sounders-FC-Stats',
    'https://fbref.com/en/squads/bd97ac1f/St-Louis-City-Stats',
    'https://fbref.com/en/squads/ca460650/San-Jose-Earthquakes-Stats',
    'https://fbref.com/en/squads/4acb0537/Sporting-Kansas-City-Stats'

]

team_names = [
    'Inter Miami',
    'FC Cincinnati',
    'New York City FC',
    'Columbus Crew',
    'New York Red Bulls',
    'Toronto FC',
    'Charlotte FC',
    'Philadelphia Union',
    'DC United',
    'Orlando City',
    'Nashville SC',
    'Atlanta United',
    'CF Montréal',
    'Chicago Fire',
    'New England Revolution',
    'Real Salt Lake',
    'Los Angeles FC',
    'Minnesota United',
    'LA Galaxy',
    'Vancouver Whitecaps',
    'Austin FC',
    'Houston Dynamo',
    'Colorado Rapids',
    'Portland Timbers',
    'Seattle Sounders',
    'St Louis City',
    'San Jose Earthquakes',
    'Sporting Kansas City'
    
]

retrieve_play_time_24_MLS(urls, team_names)

def retrieve_gsc_24_MLS(urls, team_names):
    all_data = []

    for url, team_name in zip(urls, team_names):
        df = pd.read_html(url, attrs = {"id":"stats_gca_22"})[0]
        time.sleep(3)
        #flatten multiindex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() for col in df.columns.values]
        else:
            df.columns = df.columns
        df.rename(columns={'Unnamed: 0_level_0_Player': 'Player', 'Unnamed: 1_level_0_Nation': 'Nation',
                           'Unnamed: 2_level_0_Pos': 'POS', 'Unnamed: 3_level_0_Age': 'Age', 'Unnamed: 4_level_0_90s': '90s'}, inplace=True)
        df['Nation'] = df['Nation'].str.slice(3)

        df = df[~df['Player'].isin(['Squad Total', 'Opponent Total'])]
        df['POS'] = df['POS'].str.slice(0, 2)
        df['Age'] = df['Age'].str.slice(0, 2)
        df['Team'] = team_name
        all_data.append(df)
        df.drop('Unnamed: 21_level_0_Matches', axis=1, inplace=True)
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('GSC.csv', index=False)


urls = [
    'https://fbref.com/en/squads/cb8b86a2/Inter-Miami-Stats',
    'https://fbref.com/en/squads/e9ea41b2/FC-Cincinnati-Stats',
    'https://fbref.com/en/squads/64e81410/New-York-City-FC-Stats',
    'https://fbref.com/en/squads/529ba333/Columbus-Crew-Stats',
    'https://fbref.com/en/squads/69a0fb10/New-York-Red-Bulls-Stats',
    'https://fbref.com/en/squads/130f43fa/Toronto-FC-Stats',
    'https://fbref.com/en/squads/eb57545a/Charlotte-FC-Stats',
    'https://fbref.com/en/squads/46024eeb/Philadelphia-Union-Stats',
    'https://fbref.com/en/squads/44117292/DC-United-Stats',
    'https://fbref.com/en/squads/46ef01d0/Orlando-City-Stats',
    'https://fbref.com/en/squads/35f1b818/Nashville-SC-Stats',
    'https://fbref.com/en/squads/1ebc1a5b/Atlanta-United-Stats',
    'https://fbref.com/en/squads/fc22273c/CF-Montreal-Stats',
    'https://fbref.com/en/squads/f9940243/Chicago-Fire-Stats',
    'https://fbref.com/en/squads/3c079def/New-England-Revolution-Stats',
    'https://fbref.com/en/squads/f7d86a43/Real-Salt-Lake-Stats',
    'https://fbref.com/en/squads/81d817a3/Los-Angeles-FC-Stats',
    'https://fbref.com/en/squads/99ea75a6/Minnesota-United-Stats',
    'https://fbref.com/en/squads/d8b46897/LA-Galaxy-Stats',
    'https://fbref.com/en/squads/ab41cb90/Vancouver-Whitecaps-FC-Stats',
    'https://fbref.com/en/squads/b918956d/Austin-FC-Stats',
    'https://fbref.com/en/squads/0d885416/Houston-Dynamo-Stats',
    'https://fbref.com/en/squads/415b4465/Colorado-Rapids-Stats',
    'https://fbref.com/en/squads/d076914e/Portland-Timbers-Stats',
    'https://fbref.com/en/squads/6218ebd4/Seattle-Sounders-FC-Stats',
    'https://fbref.com/en/squads/bd97ac1f/St-Louis-City-Stats',
    'https://fbref.com/en/squads/ca460650/San-Jose-Earthquakes-Stats',
    'https://fbref.com/en/squads/4acb0537/Sporting-Kansas-City-Stats'
]

team_names = [
    'Inter Miami',
    'FC Cincinnati',
    'New York City FC',
    'Columbus Crew',
    'New York Red Bulls',
    'Toronto FC',
    'Charlotte FC',
    'Philadelphia Union',
    'DC United',
    'Orlando City',
    'Nashville SC',
    'Atlanta United',
    'CF Montréal',
    'Chicago Fire',
    'New England Revolution',
    'Real Salt Lake',
    'Los Angeles FC',
    'Minnesota United',
    'LA Galaxy',
    'Vancouver Whitecaps',
    'Austin FC',
    'Houston Dynamo',
    'Colorado Rapids',
    'Portland Timbers',
    'Seattle Sounders',
    'St Louis City',
    'San Jose Earthquakes',
    'Sporting Kansas City'
]


retrieve_gsc_24_MLS(urls, team_names)



def retrieve_mlf_24_MLS(urls, team_names):
    all_data = []

    for url, team_name in zip(urls, team_names):
        df = pd.read_html(url, attrs = {"id":"matchlogs_for"})[0]

        df['Time'] = df['Time'].str.slice(0, 5)
        df = df[df['Result'].notna() & (df['Result'] != '')]
        df['Team'] = team_name
        df.rename(columns={'Team': 'Home Team'}, inplace=True)
        all_data.append(df)
    df.drop(['Match Report', 'Notes'], axis=1, inplace=True)
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('mlf.csv', index=False)


urls = [
    'https://fbref.com/en/squads/cb8b86a2/Inter-Miami-Stats',
    'https://fbref.com/en/squads/e9ea41b2/FC-Cincinnati-Stats',
    'https://fbref.com/en/squads/64e81410/New-York-City-FC-Stats',
    'https://fbref.com/en/squads/529ba333/Columbus-Crew-Stats',
    'https://fbref.com/en/squads/69a0fb10/New-York-Red-Bulls-Stats',
    'https://fbref.com/en/squads/130f43fa/Toronto-FC-Stats',
    'https://fbref.com/en/squads/eb57545a/Charlotte-FC-Stats',
    'https://fbref.com/en/squads/46024eeb/Philadelphia-Union-Stats',
    'https://fbref.com/en/squads/44117292/DC-United-Stats',
    'https://fbref.com/en/squads/46ef01d0/Orlando-City-Stats',
    'https://fbref.com/en/squads/35f1b818/Nashville-SC-Stats',
    'https://fbref.com/en/squads/1ebc1a5b/Atlanta-United-Stats',
    'https://fbref.com/en/squads/fc22273c/CF-Montreal-Stats',
    'https://fbref.com/en/squads/f9940243/Chicago-Fire-Stats',
    'https://fbref.com/en/squads/3c079def/New-England-Revolution-Stats',
    'https://fbref.com/en/squads/f7d86a43/Real-Salt-Lake-Stats',
    'https://fbref.com/en/squads/81d817a3/Los-Angeles-FC-Stats',
    'https://fbref.com/en/squads/99ea75a6/Minnesota-United-Stats',
    'https://fbref.com/en/squads/d8b46897/LA-Galaxy-Stats',
    'https://fbref.com/en/squads/ab41cb90/Vancouver-Whitecaps-FC-Stats',
    'https://fbref.com/en/squads/b918956d/Austin-FC-Stats',
    'https://fbref.com/en/squads/0d885416/Houston-Dynamo-Stats',
    'https://fbref.com/en/squads/415b4465/Colorado-Rapids-Stats',
    'https://fbref.com/en/squads/d076914e/Portland-Timbers-Stats',
    'https://fbref.com/en/squads/6218ebd4/Seattle-Sounders-FC-Stats',
    'https://fbref.com/en/squads/bd97ac1f/St-Louis-City-Stats',
    'https://fbref.com/en/squads/ca460650/San-Jose-Earthquakes-Stats',
    'https://fbref.com/en/squads/4acb0537/Sporting-Kansas-City-Stats'
]

team_names = [
    'Inter Miami',
    'FC Cincinnati',
    'New York City FC',
    'Columbus Crew',
    'New York Red Bulls',
    'Toronto FC',
    'Charlotte FC',
    'Philadelphia Union',
    'DC United',
    'Orlando City',
    'Nashville SC',
    'Atlanta United',
    'CF Montréal',
    'Chicago Fire',
    'New England Revolution',
    'Real Salt Lake',
    'Los Angeles FC',
    'Minnesota United',
    'LA Galaxy',
    'Vancouver Whitecaps',
    'Austin FC',
    'Houston Dynamo',
    'Colorado Rapids',
    'Portland Timbers',
    'Seattle Sounders',
    'St Louis City',
    'San Jose Earthquakes',
    'Sporting Kansas City'
]

retrieve_mlf_24_MLS(urls, team_names)


def retrieve_passing_24_MLS(urls, team_names):
    all_data = []

    for url, team_name in zip(urls, team_names):
        df = pd.read_html(url, attrs = {"id":"stats_passing_22"})[0]
        
        #flatten multiindex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() for col in df.columns.values]
        else:
            df.columns = df.columns
        df.rename(columns={'Unnamed: 0_level_0_Player': 'Player', 'Unnamed: 1_level_0_Nation': 'Nation',
                           'Unnamed: 2_level_0_Pos': 'POS', 'Unnamed: 3_level_0_Age': 'Age', 'Unnamed: 4_level_0_90s': '90s',
                           'Unnamed: 19_level_0_Ast': 'AST', 'Unnamed: 20_level_0_xAG': 'xAG', 'Expected_xA': 'xA', 'Expected_A-xAG': 'A-xAG', 
                           'Unnamed: 23_level_0_KP': 'KP', 'Unnamed: 24_level_0_1/3': '1/3', 'Unnamed: 25_level_0_PPA': 'PPA',
                           'Unnamed: 26_level_0_CrsPA': 'CrsPA', 'Unnamed: 27_level_0_PrgP': 'PrgP'}, inplace=True)
        df['Nation'] = df['Nation'].str.slice(3)

        df = df[~df['Player'].isin(['Squad Total', 'Opponent Total'])]
        df['POS'] = df['POS'].str.slice(0, 2)
        df['Age'] = df['Age'].str.slice(0, 2)
        df['Team'] = team_name
        all_data.append(df)
        df.drop('Unnamed: 28_level_0_Matches', axis=1, inplace=True)
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('passing.csv', index=False)


urls = [
    'https://fbref.com/en/squads/cb8b86a2/Inter-Miami-Stats',
    'https://fbref.com/en/squads/e9ea41b2/FC-Cincinnati-Stats',
    'https://fbref.com/en/squads/64e81410/New-York-City-FC-Stats',
    'https://fbref.com/en/squads/529ba333/Columbus-Crew-Stats',
    'https://fbref.com/en/squads/69a0fb10/New-York-Red-Bulls-Stats',
    'https://fbref.com/en/squads/130f43fa/Toronto-FC-Stats',
    'https://fbref.com/en/squads/eb57545a/Charlotte-FC-Stats',
    'https://fbref.com/en/squads/46024eeb/Philadelphia-Union-Stats',
    'https://fbref.com/en/squads/44117292/DC-United-Stats',
    'https://fbref.com/en/squads/46ef01d0/Orlando-City-Stats',
    'https://fbref.com/en/squads/35f1b818/Nashville-SC-Stats',
    'https://fbref.com/en/squads/1ebc1a5b/Atlanta-United-Stats',
    'https://fbref.com/en/squads/fc22273c/CF-Montreal-Stats',
    'https://fbref.com/en/squads/f9940243/Chicago-Fire-Stats',
    'https://fbref.com/en/squads/3c079def/New-England-Revolution-Stats',
    'https://fbref.com/en/squads/f7d86a43/Real-Salt-Lake-Stats',
    'https://fbref.com/en/squads/81d817a3/Los-Angeles-FC-Stats',
    'https://fbref.com/en/squads/99ea75a6/Minnesota-United-Stats',
    'https://fbref.com/en/squads/d8b46897/LA-Galaxy-Stats',
    'https://fbref.com/en/squads/ab41cb90/Vancouver-Whitecaps-FC-Stats',
    'https://fbref.com/en/squads/b918956d/Austin-FC-Stats',
    'https://fbref.com/en/squads/0d885416/Houston-Dynamo-Stats',
    'https://fbref.com/en/squads/415b4465/Colorado-Rapids-Stats',
    'https://fbref.com/en/squads/d076914e/Portland-Timbers-Stats',
    'https://fbref.com/en/squads/6218ebd4/Seattle-Sounders-FC-Stats',
    'https://fbref.com/en/squads/bd97ac1f/St-Louis-City-Stats',
    'https://fbref.com/en/squads/ca460650/San-Jose-Earthquakes-Stats',
    'https://fbref.com/en/squads/4acb0537/Sporting-Kansas-City-Stats'
]

team_names = [
    'Inter Miami',
    'FC Cincinnati',
    'New York City FC',
    'Columbus Crew',
    'New York Red Bulls',
    'Toronto FC',
    'Charlotte FC',
    'Philadelphia Union',
    'DC United',
    'Orlando City',
    'Nashville SC',
    'Atlanta United',
    'CF Montréal',
    'Chicago Fire',
    'New England Revolution',
    'Real Salt Lake',
    'Los Angeles FC',
    'Minnesota United',
    'LA Galaxy',
    'Vancouver Whitecaps',
    'Austin FC',
    'Houston Dynamo',
    'Colorado Rapids',
    'Portland Timbers',
    'Seattle Sounders',
    'St Louis City',
    'San Jose Earthquakes',
    'Sporting Kansas City'
]

retrieve_passing_24_MLS(urls, team_names)





def retrieve_shooting_24_MLS(urls, team_names):
    all_data = []

    for url, team_name in zip(urls, team_names):
        df = pd.read_html(url, attrs = {"id":"stats_shooting_22"})[0]
        time.sleep(3)
        #flatten multiindex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() for col in df.columns.values]
        else:
            df.columns = df.columns
        df.rename(columns={'Unnamed: 0_level_0_Player': 'Player', 'Unnamed: 1_level_0_Nation': 'Nation',
                           'Unnamed: 2_level_0_Pos': 'POS', 'Unnamed: 3_level_0_Age': 'Age', 'Unnamed: 4_level_0_90s': '90s'}, inplace=True)
        df['Nation'] = df['Nation'].str.slice(3)

        df = df[~df['Player'].isin(['Squad Total', 'Opponent Total'])]
        df['POS'] = df['POS'].str.slice(0, 2)
        df['Age'] = df['Age'].str.slice(0, 2)
        df['Team'] = team_name
        all_data.append(df)
        df.drop('Unnamed: 22_level_0_Matches', axis=1, inplace=True)
        
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('shooting.csv', index=False)


urls = [
     'https://fbref.com/en/squads/cb8b86a2/Inter-Miami-Stats',
    'https://fbref.com/en/squads/e9ea41b2/FC-Cincinnati-Stats',
    'https://fbref.com/en/squads/64e81410/New-York-City-FC-Stats',
    'https://fbref.com/en/squads/529ba333/Columbus-Crew-Stats',
    'https://fbref.com/en/squads/69a0fb10/New-York-Red-Bulls-Stats',
    'https://fbref.com/en/squads/130f43fa/Toronto-FC-Stats',
    'https://fbref.com/en/squads/eb57545a/Charlotte-FC-Stats',
    'https://fbref.com/en/squads/46024eeb/Philadelphia-Union-Stats',
    'https://fbref.com/en/squads/44117292/DC-United-Stats',
    'https://fbref.com/en/squads/46ef01d0/Orlando-City-Stats',
    'https://fbref.com/en/squads/35f1b818/Nashville-SC-Stats',
    'https://fbref.com/en/squads/1ebc1a5b/Atlanta-United-Stats',
    'https://fbref.com/en/squads/fc22273c/CF-Montreal-Stats',
    'https://fbref.com/en/squads/f9940243/Chicago-Fire-Stats',
    'https://fbref.com/en/squads/3c079def/New-England-Revolution-Stats',
    'https://fbref.com/en/squads/f7d86a43/Real-Salt-Lake-Stats',
    'https://fbref.com/en/squads/81d817a3/Los-Angeles-FC-Stats',
    'https://fbref.com/en/squads/99ea75a6/Minnesota-United-Stats',
    'https://fbref.com/en/squads/d8b46897/LA-Galaxy-Stats',
    'https://fbref.com/en/squads/ab41cb90/Vancouver-Whitecaps-FC-Stats',
    'https://fbref.com/en/squads/b918956d/Austin-FC-Stats',
    'https://fbref.com/en/squads/0d885416/Houston-Dynamo-Stats',
    'https://fbref.com/en/squads/415b4465/Colorado-Rapids-Stats',
    'https://fbref.com/en/squads/d076914e/Portland-Timbers-Stats',
    'https://fbref.com/en/squads/6218ebd4/Seattle-Sounders-FC-Stats',
    'https://fbref.com/en/squads/bd97ac1f/St-Louis-City-Stats',
    'https://fbref.com/en/squads/ca460650/San-Jose-Earthquakes-Stats',
    'https://fbref.com/en/squads/4acb0537/Sporting-Kansas-City-Stats'

]

team_names = [
    'Inter Miami',
    'FC Cincinnati',
    'New York City FC',
    'Columbus Crew',
    'New York Red Bulls',
    'Toronto FC',
    'Charlotte FC',
    'Philadelphia Union',
    'DC United',
    'Orlando City',
    'Nashville SC',
    'Atlanta United',
    'CF Montréal',
    'Chicago Fire',
    'New England Revolution',
    'Real Salt Lake',
    'Los Angeles FC',
    'Minnesota United',
    'LA Galaxy',
    'Vancouver Whitecaps',
    'Austin FC',
    'Houston Dynamo',
    'Colorado Rapids',
    'Portland Timbers',
    'Seattle Sounders',
    'St Louis City',
    'San Jose Earthquakes',
    'Sporting Kansas City'
    
]

retrieve_shooting_24_MLS(urls, team_names)


################ USL SECTION #################### 



def retrieve_shooting_24_USLC(urls, team_names):
    all_data = []

    for url, team_name in zip(urls, team_names):
        df = pd.read_html(url, attrs = {"id":"stats_shooting_73"})[0]
        
        #flatten multiindex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() for col in df.columns.values]
        else:
            df.columns = df.columns
        df.rename(columns={'Unnamed: 0_level_0_Player': 'Player', 'Unnamed: 1_level_0_Nation': 'Nation',
                           'Unnamed: 2_level_0_Pos': 'POS', 'Unnamed: 3_level_0_Age': 'Age', 'Unnamed: 4_level_0_90s': '90s'}, inplace=True)
        df['Nation'] = df['Nation'].str.slice(3)

        df = df[~df['Player'].isin(['Squad Total', 'Opponent Total'])]
        df['POS'] = df['POS'].str.slice(0, 2)
        df['Age'] = df['Age'].str.slice(0, 2)
        df['Team'] = team_name
        all_data.append(df)
        df.drop('Unnamed: 16_level_0_Matches', axis=1, inplace=True)
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('shooting.csv', index=False)


urls = [
    'https://fbref.com/en/squads/43e28cc5/Louisville-City-Stats',
    'https://fbref.com/en/squads/91aa83f9/Charleston-Battery-Stats',
    'https://fbref.com/en/squads/28dabcec/Tampa-Bay-Rowdies-Stats',
    'https://fbref.com/en/squads/3fdc81dd/Indy-Eleven-Stats',
    'https://fbref.com/en/squads/a2e0ad49/Detroit-City-Stats',
    'https://fbref.com/en/squads/448d7865/Birmingham-Legion-Stats',
    'https://fbref.com/en/squads/f70f4c6e/Loudoun-United-Stats',
    'https://fbref.com/en/squads/c650f805/Hartford-Athletic-Stats',
    'https://fbref.com/en/squads/822b124d/North-Carolina-FC-Stats',
    'https://fbref.com/en/squads/1a1aef59/Pittsburgh-Riverhounds-Stats',
    'https://fbref.com/en/squads/a568f421/Rhode-Island-FC-Stats',
    'https://fbref.com/en/squads/a0a57b76/Miami-FC-Stats',
    'https://fbref.com/en/squads/87389b8b/New-Mexico-United-Stats',
    'https://fbref.com/en/squads/d1903ffe/Sacramento-Republic-Stats',
    'https://fbref.com/en/squads/7d8a4e62/Orange-County-SC-Stats',
    'https://fbref.com/en/squads/e5e323aa/Colorado-Springs-Switchbacks-Stats',
    'https://fbref.com/en/squads/42cc5a38/San-Antonio-FC-Stats',
    'https://fbref.com/en/squads/41736050/Memphis-901-Stats',
    'https://fbref.com/en/squads/ed74064b/Monterey-Bay-Stats',
    'https://fbref.com/en/squads/3b2880c1/Phoenix-Rising-Stats',
    'https://fbref.com/en/squads/a0b3d640/Oakland-Roots-Stats',
    'https://fbref.com/en/squads/baec986d/Las-Vegas-Lights-FC-Stats',
    'https://fbref.com/en/squads/6d0be563/FC-Tulsa-Stats',
    'https://fbref.com/en/squads/8ed09812/El-Paso-Locomotive-Stats'

]

team_names = [
    'Louisville City',
    'Charleston Battery',
    'Tampa Bay Rowdies',
    'Indy Eleven',
    'Detroit City',
    'Birmingham Legion',
    'Loudoun United',
    'Hartford Athletic',
    'North Carolina FC',
    'Pittsburgh Riverhounds',
    'Rhode Island FC',
    'Miami FC',
    'New Mexico United',
    'Sacramento Republic',
    'Orange County SC',
    'Colorado Springs Switchbacks',
    'San Antonio FC',
    'Memphis 901',
    'Monterey Bay',
    'Phoenix Rising',
    'Oakland Roots',
    'Las Vegas Lights',
    'FC Tulsa',
    'El Paso Locomotive'
]

retrieve_shooting_24_USLC(urls, team_names)