import streamlit as st
import pandas as pd
from bokeh.palettes import Set3
from math import pi


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
        
def t3_genres(df):
    genres = df['genre'][-3:].values
    return ', '.join(genres)


def load_prepare_csv(data_path:str):
    df = pd.read_csv("./data/vgsales.csv")
    df.dropna(how="any", inplace=True)
    df = df.astype({"Year": 'int'})
    df = df.reset_index(drop=True)
    return df


def top_sales_of_year(data,publisher):
    """
    Returns:
        top_sales
        
        years
    """
    years = sorted(data["Year"].unique())
    
    top_sales = []
    for y in years:
        filtered_data = data.loc[(data["Year"] == y) & (data["Publisher"] == publisher)]
        max_global_sales = filtered_data["Global_Sales"].max()
        top_sales.append(max_global_sales)
        
    return top_sales, years


def games_each_year(data, years, publisher):
    n_genres, n_games = [],[]
    publisher_games = data[data["Publisher"] == publisher]
    for y in years:
        selected_year = publisher_games.loc[data["Year"]==y]
        n_games.append(selected_year["Name"].nunique())
        n_genres.append(selected_year["Genre"].nunique())
            
    return pd.DataFrame({"year":years,"games":n_games, "genres":n_genres})


def games_in_each_genre(data,publisher):
    publisher_games = data[data["Publisher"] == publisher]
    game_counts = []
    for g in data["Genre"].unique():
        game_counts.append({"genre": g, "games": publisher_games[publisher_games["Genre"]==g]["Name"].nunique()})
    df = pd.DataFrame(game_counts)
    df.sort_values('games', inplace=True)
    df['angle'] = df['games']/df['games'].sum() * 2*pi
    df['color'] = Set3[len(df)]
    
    return df