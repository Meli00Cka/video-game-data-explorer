from bokeh.palettes import Set3
from itertools import product
import streamlit as st
import pandas as pd
from math import pi
import time



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


def toggle_mode():
    # toggle between True and False
    st.session_state.mode = not st.session_state.mode
    
    
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.3)
        
        
def mode_stats(cool_text=False):
    mode_label = "Data Playground" if st.session_state.mode else "Story Mode"
    text = f"Current Mode: {mode_label}"
    if cool_text:
        st.info((text))
    else:
        st.write(text)


def genre_freq(data):
    genre_counts = data["Genre"].value_counts().values
    genre_names = data["Genre"].value_counts().index
    data = pd.DataFrame({"Genre": genre_names, "Frequency": genre_counts})

    data['angle'] = data['Frequency']/data['Frequency'].sum() * 2*pi
    data['color'] = Set3[len(data)]
    
    return data


def generate_prediction_data(publisher, year, platform, genre):    
    columns = ["Publisher", "Year", "Platform", "Genre"]  
    data = list(product([publisher], [year], platform, genre)) # combine the values
    return pd.DataFrame(data, columns=columns)


def convert_inputs(pr_platform, pr_publisher, model_data_columns):
    if "Platform_"+pr_platform not in model_data_columns:
        pr_platform = "Platform_Other"
    else:
        pr_platform = "Platform_"+pr_platform

    if pr_publisher not in model_data_columns:
        pr_publisher = "Other"
    
    return pr_platform, pr_publisher