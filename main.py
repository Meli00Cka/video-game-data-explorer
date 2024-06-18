from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.transform import cumsum
import functions as fu
import streamlit as st
import numpy as np
from model import model
import pandas as pd


def main():

    st.set_page_config(
        layout="wide",page_title="VG Data explorer",page_icon="./img/logo.png",
        initial_sidebar_state="auto",menu_items=None)
    
    fu.local_css("style.css")

    data = fu.load_prepare_csv("./data/vgsales.csv")

    if "mode" not in st.session_state:
        st.session_state.mode = False

    with st.container(height=200, border=False):
        st.write("# Video game\n## Data explorer\n\n")

    with st.sidebar:
        if st.button(label="Switch Mode",use_container_width=True):
            fu.toggle_mode()
        
        if st.session_state.mode:
            with st.expander("More details"):
                st.write("You can edit the dataset, And from the list below choose and analyze any publisher you like.")
        
        fu.mode_stats()
        
        st.write("<hr><br>",unsafe_allow_html=True)
        
        if not st.session_state.mode:
            publisher = "Nintendo"
        else:
            publisher = st.selectbox("Select a publisher",data["Publisher"].unique(),7,help="Select a publisher to analyse on plots")
            st.write("<hr><br>",unsafe_allow_html=True)
        st.write("First plot")
        p_Global = st.toggle("Total worldwide", value=True)
        p_NA = st.toggle("North America", value=True)
        p_EU = st.toggle("Europe", value=True)
        p_JP = st.toggle("Japan", value=True)
        p_Other = st.toggle("Rest of the world", value=True)
        
        st.write("<hr>",unsafe_allow_html=True)
        
        st.write("Second plot")
        p_bestseller = st.toggle("Best seller", value=True)
        p_games = st.toggle("Games", value=True)
        
        st.write("<hr>",unsafe_allow_html=True)
        
        st.write("#### Source code:")
        st.link_button("GitHub", "https://github.com/Meli00Cka/video-game-data-explorer", use_container_width=True)
    
    st.write("<br><br>",unsafe_allow_html=True)
    st.write("### Dataset")
    with st.container(border=True):
        
        data_info="""

        Name -> The games name

        Platform -> Platform of the games release (i.e. PC,PS4, etc.)

        Year -> Year of the game's release

        Genre -> Genre of the game

        Publisher -> Publisher of the game

        NA_Sales -> Sales in North America (in millions)

        EU_Sales -> Sales in Europe (in millions)

        JP_Sales -> Sales in Japan (in millions)

        Other_Sales -> Sales in the rest of the world (in millions)

        Global_Sales -> Total worldwide sales"""

        col1, col2 = st.columns([2, 4])
        with col2:
        
            selected_col = st.multiselect(label="Quick view of the dataset:", options=data.columns, default=list(data.columns), help=data_info)
            if not st.session_state.mode:
                index = st.slider(label="data index", value=8, label_visibility="hidden")
                st.write(data.loc[:index, selected_col])
            else:
                data = st.data_editor(data[selected_col])
        
        with col1:
        
            fu.mode_stats(True)
        
            with st.container(border=True):
                st.write("Feel free to use the plot tools (from the toolbox above them)\n\nOr if you want more control you can use the left side bar\n\nYou can also switch to Playground mode\n\nHave fun exploring around!")
            
            st.write(data.describe())
                
        with st.expander("More details"):
            st.write(f"""
                    <h6>This dataset contains a list of video games with sales greater than 100,000 copies. It was generated by a scrape of vgchartz.com.</h6>
                    <h6>Fields include:</h6>{data_info}""",unsafe_allow_html=True)
            st.link_button("Open dataset source", "https://www.kaggle.com/datasets/gregorut/videogamesales")
        
    st.write("<br><br>",unsafe_allow_html=True)
    st.write("### Analyse")
    with st.container(border=True):
        
        color_palette=["#4CC9F0","#4361EE","#10439F","#874CCC","#F27BBD"]
        
        top_sales ,years = fu.top_sales_of_year(data, publisher)
        publisher_games = data[data["Publisher"] == publisher]
        t15_publisher_games = data[(data["Publisher"] == publisher) & (data["Rank"] <= 15)]
        publisher_g_each_y = fu.games_each_year(data, years, publisher)
        publisher_n_games_in_genre = fu.games_in_each_genre(data,publisher)

        avg_gs = np.average(list(data.loc[2:19, "Global_Sales"]))
        top_g = data.loc[data["Rank"]==1]
        totalg_publisher = publisher_games["Name"].nunique()
        
        genre_c_n = fu.genre_freq(data)

        
        p1 = figure(title="Top 20 Best-Selling Video Games", x_axis_label="Name", y_axis_label="Sales (Millions)", x_range=list(data.loc[:19, "Name"]), tools="box_select,pan,wheel_zoom,reset,save")
        p2 = figure(title=f"{publisher} Games", y_axis_label="Global Sales (Millions)", x_axis_label="Year", tools="crosshair,box_select,pan,wheel_zoom,lasso_select,reset,save")
        p3 = figure(title=f"{publisher} game releases", y_axis_label="Games", x_axis_label="Year", tools="crosshair,pan,wheel_zoom,reset,save")
        p4 = figure(title="Number of game releases in each genre", toolbar_location=None,tools="hover", tooltips="@genre: @games", x_range=(-0.5, 1.0))
        p6 = figure(title="Most frequent genres", toolbar_location=None,tools="hover", tooltips="@Genre: @Frequency", x_range=(-0.5, 1.0))
        
        p1.add_tools(HoverTool(tooltips=[("Name","@Name"),("Global Sales","@Global_Sales"),("Publisher","@Publisher"),("Genre","@Genre"),("Year","@Year"),("Rank","@Rank")]))
        p2.add_tools(HoverTool(tooltips=[("Name","@Name"),("Global Sales","@Global_Sales"),("Publisher","@Publisher"),("Genre","@Genre"),("Year","@Year"),("Platform","@Platform")]))
        p3.add_tools(HoverTool(tooltips=[("Games", "@games"), ("Year", "@year"), ("Genres", "@genres")]))

        p1.toolbar_location, p2.toolbar_location, p3.toolbar_location= "above", "above", "above"


        # p1
        if p_Global:
            p1.vbar(top="Global_Sales",legend_label="Total worldwide", x="Name",source=data, width=0.5, fill_color=color_palette[0])
        if p_NA:
            p1.vbar(top="NA_Sales",legend_label="North America", x="Name",source=data, width=0.5, fill_color=color_palette[1])
        if p_EU:
            p1.vbar(top="EU_Sales",legend_label="Europe", x="Name",source=data, width=0.5, fill_color=color_palette[2])
        if p_JP:
            p1.vbar(top="JP_Sales",legend_label="Japan", x="Name",source=data, width=0.5, fill_color=color_palette[3])
        if p_Other:
            p1.vbar(top="Other_Sales",legend_label="Rest of the world", x="Name",source=data, width=0.5, fill_color=color_palette[4])
        p1.xaxis.major_label_orientation = 3.14/5.5
        
        # p6
        p6.wedge(x=0.06, y=1, radius=0.4, start_angle=cumsum("angle", include_zero=True), end_angle=cumsum("angle"),
                line_color="white", fill_color="color", legend_field="Genre", source=genre_c_n)
        p6.axis.axis_label=None
        p6.axis.visible=False
        p6.grid.grid_line_color = None
            

        # p2
        if p_bestseller:
            p2.line(x=years, y=top_sales, color="#0063d8")
            p2.square(x=years, y=top_sales, fill_color="#b800cf", line_color="#b800cf", size=7, legend_label="Best seller of the year")
        if p_games:
            p2.square(source=publisher_games, x="Year", y="Global_Sales", legend_label=f"{publisher} games")
        if p_bestseller:
            if not st.session_state.mode:
                p2.hex(source=t15_publisher_games, x="Year", y="Global_Sales", size=7, fill_color="#00d7ff", line_color="#000", legend_label="Top 15 by Rank")


        # p3
        p3.vbar(source=publisher_g_each_y, x="year", top="games", width=0.5, fill_color="#ffffff")
        p3.line(source=publisher_g_each_y, x="year", y="games", line_width=3, line_color="#00d7ff", legend_label="Games each year")

        # p4
        p4.wedge(x=0.2, y=1, radius=0.38,start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend_field='genre', source=publisher_n_games_in_genre)
        p4.axis.axis_label, p4.grid.grid_line_color = None, None
        p4.axis.visible = False


        # show plots
        if not st.session_state.mode:
            st.write("First let's see the top 20 best-selling games:")
        
        col_plot1, col_plot6  = st.columns(spec=[5,2.5])
        col_plot1.bokeh_chart(p1, use_container_width=True)
        col_plot6.bokeh_chart(p6, use_container_width=True)
        
        if not st.session_state.mode:
            st.write(f"""
                Ranks from 20 to 2 had an average of __{avg_gs:.2f}M__ Global sales;
                \rBut '__{top_g["Name"][0]}__' had __{top_g["Global_Sales"][0]}M__ Sales!""")
            st.write(f"This chart shows other popular games from {top_g['Publisher'][0]}, {top_g['Name'][0]}'s publisher:")
        
        st.bokeh_chart(p2, use_container_width=True)

        if not st.session_state.mode:
            st.write(f"As you can see between 2005 and 2010, __{top_g['Publisher'][0]}__ did really well and after the release of __{top_g['Name'][0]}__ They entered the top 15 more than before.")
            st.write(f"This publisher has made {totalg_publisher} games in total, so let's see how many games they made each year:")

        col_plot4, col_plot3 = st.columns([2.5,5])
        col_plot3.bokeh_chart(p3, use_container_width=True)
        col_plot4.bokeh_chart(p4, use_container_width=True)

        if not st.session_state.mode:
            st.write(f"According to the plot, __{top_g['Name'][0]}__ released 57 games in 2004, Thats __6.3X__ or __533%__ more games than 2003!")
            st.write(f"And top 3 genres are: {fu.t3_genres(publisher_n_games_in_genre)}")


    st.write("<br><br>",unsafe_allow_html=True)
    st.write("### Predict")
    with st.container(border=True):
        
        dt_model = model(data)
        dt_model.do_all("dt")
        
        genre_names =  dt_model.genre_names
        
        p5 = figure(title="Actual vs Predicted Labels", x_axis_label="Index", y_axis_label="Values",tools="box_select,pan,wheel_zoom,reset,save",height=450)
        p5.circle(x=range(len(dt_model.y_pred)), y=dt_model.y_pred, legend_label="Predicted", color=color_palette[3], alpha=0.5)
        p5.circle(x=range(len(dt_model.y_test)), y=dt_model.y_test, legend_label="Actual Labels", color=color_palette[0], alpha=0.5)
        
        if st.session_state.mode:
            col_f1, col_f2, col_f3, col_f4 , col_f5= st.columns(5)
            with col_f1:
                pr_publisher = st.selectbox("Publisher", data["Publisher"].unique(),index=0)
                pr_publisher = "Publisher_"+pr_publisher
            pr_platform = col_f2.selectbox("Platform", data["Platform"].unique(),index=14)
            pr_genre = col_f3.selectbox("Genre", genre_names, index=3)
            pr_year = col_f4.number_input("Year", min_value=1900, max_value=2100, value=2017)
            with col_f5:
                st.write("<br>",unsafe_allow_html=True)
                predict_stats = st.button("Predict",use_container_width=True)
            
            pr_platform, pr_publisher = fu.convert_inputs(pr_platform, pr_publisher, dt_model.data.columns)
                
            for i,g in enumerate(genre_names):
                if pr_genre == g:
                    pr_genre = i       

        else:
            pr_publisher, pr_platform = "Publisher_Nintendo", "Platform_DS"
            pr_genre, pr_year = 3, 2017
            predict_stats=True
        if predict_stats:
            dt_predict = dt_model.predict(publisher=pr_publisher, platform=pr_platform, genre=pr_genre, year=pr_year)
            
        
        if not st.session_state.mode:
            ### ML
            # inputs
            pub_pr_platform = list(data["Platform"].unique())
            
            for p in pub_pr_platform.copy():
                if "Platform_" + p not in dt_model.data.columns:
                    pub_pr_platform.remove(p)
            pub_pr_platform.append("Other")

            pub_pr_publisher = "Nintendo"
            pub_pr_year = 2017
            # pub_pr_platform
            pub_pr_genre = genre_names.values()

            # preprocess
            pred_df = fu.generate_prediction_data(pub_pr_publisher, pub_pr_year, pub_pr_platform, pub_pr_genre)

            new_df = pd.DataFrame(columns=dt_model.data.columns.drop("Global_Sales"))
            new_records = dt_model.one_hot_encode(pred_df)
            new_df = pd.concat([new_df, new_records], ignore_index=True).fillna(0.0)

            pub_pr_platform = list(data["Platform"].unique())

            for p in pub_pr_platform.copy():
                if "Platform_" + p not in dt_model.data.columns:
                    pub_pr_platform.remove(p)
                    
            pub_pr_platform.append("Other")

            pred_val = dt_model.predict(pub_pr_publisher, pub_pr_platform, pub_pr_genre, pub_pr_year, single_predict=False)

            publisher_predict = dt_model.X_user.assign(Global_Sales=pred_val)

            extra_col = ["Year"] + list(publisher_predict.columns[30:-1])
            publisher_predict = publisher_predict.drop(columns=extra_col, axis=1, inplace=False)

            publisher_predict["Genre"] = dt_model.decode_column(publisher_predict["Genre"],genre_names)

            # predicted value
            publisher_predict = publisher_predict.sort_values(by="Global_Sales",ascending=False)
            
            ####

            st.write(f"If {publisher} plans their next role-playing game for PC in 2017, how much will it sale on global?")
            st.write("To predict and find out, let's train a Desicion Tree model with features: Year, Genre, Platform and Publisher.")
            
        
        with st.container(border=True):
            col_plot5, col3 = st.columns([2,4])
        
            with col_plot5:
                if not st.session_state.mode:
                    st.bokeh_chart(p5,use_container_width=True)
        
            with col3:
                if not st.session_state.mode:
                    st.write(f"The MSE error is: {dt_model.mse_error:.2f} And the predicted value for role-playing game is __{dt_predict[0]:.2f}M__,\n\n So I decided to predict in every possible way to get a better result and find the best genre and platform.\n\nHere is the result:")
        
                    selected_p_col = st.multiselect(label="select",label_visibility="hidden",options=publisher_predict.columns,default=["Genre","Global_Sales"])
                    selected_p_index = st.slider(label="select",label_visibility="hidden",max_value=len(publisher_predict), min_value=1)
        
                    st.write(publisher_predict[selected_p_col].head(selected_p_index))
        
                    st.write(f"{publisher_predict['Genre'].values[0]} seems to be the best genre in {pub_pr_year} for {publisher}, Also platforms don't really make a difference")
            
                    
            if predict_stats and st.session_state.mode:
                st.info(f"The predicted value is:  __{dt_predict[0]:.2f}M__")

if __name__ == "__main__":
    main()