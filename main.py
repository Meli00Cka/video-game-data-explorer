import matplotlib.pyplot as plt
from bokeh.plotting import figure
import functions as function
import streamlit as st
import pandas as pd
import numpy as np

# def main():

    
# streamlit config
st.set_page_config(
    layout="wide",
    page_title="VG Explorer", 
    page_icon="./img/logo.png",
    initial_sidebar_state="auto", 
    menu_items=None
)
# load local css
function.local_css("style.css")

# load and prepare data
data = pd.read_csv("./data/vgsales.csv")
data.dropna(how="any", inplace=True)
data.Year = data.Year.astype(int)



# app header
with st.container(height=200, border=False):
    st.write("# Video game\n## Data explorer")


# showing raw data
with st.container(border=True):
    
    selected_col = st.multiselect(label="Quick view of the dataset:", options=data.columns, default=list(data.columns))
    # index = st.slider(label="index", min_value=1, max_value=len(data), label_visibility="hidden", step=50) index-1
    with st.container(height=250, border=False):
        st.write(data.loc[:5, selected_col])




# plot
with st.container(border=True):
    
    st.write("")
    p = figure(y_axis_label="Year", x_axis_label="Global Sales")
    p.circle(source=data, x="Year", y="Global_Sales")
    st.bokeh_chart(p, use_container_width=True)









# sidebar
with st.sidebar:
    
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    
    add_selectbox = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
    )
    
    x = st.slider("slider",1,100,30)











# if __name__ == "__main__":
    # main()