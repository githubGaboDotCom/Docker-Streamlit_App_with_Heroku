import streamlit as st
import streamlit.components.v1 as components
from plotnine import *
import pandas as pd
import plotly.graph_objects as go

states = [' ', 'al','ar','az', 'co','ct','dc','de','fl','ga',
          'ia','id','il','in','ks','ky','la','ma','md','me',
          'mi','mn','mo','ms','mt','nc','nd','ne','nh','nj','nm',
          'nv','ny','oh','ok','or','ri','sc','tn','tx',
          'ut','va','vt','wa','wi','wv']


current_page = st.sidebar.selectbox("Select Page", ["Home", "Pyspark Source Code", "Spacial Maps"])

if current_page == "Home":
    st.title("Analytics Deployment App - Final Project DS 460")
    st.subheader("Introduction:")
    st.image("chipotle.jpeg")
    st.write("Chipotle is a large national company with thousands of \
    consumers all over the United States. It has facilities in almost \
    every state, reaching millions of people. Knowing the importance of \
    this company, we have done a study to understand the behavior of Chipotle \
    consumers. Obtaining a database from Safepgraph we have been able to obtain \
    important information about people who have visited Chipotle facilities in the \
    last 4 years. This information is provided in sets of days and months about the \
    number of visitors to these facilities.")
    st.image("customers_shopping.jpeg")
    st.write("Understanding the behavior that drives the masses can help us know how to \
    maximize a business, and help people achieve their goals and provide them with better \
    comfort. For our study we have analyzed the percentage of users who visited Chipotle on \
    a specific day and additionally visited other brands on the same day. We also obtained information \
    on the percentage of those same users who visited Chipotle, and also went to other brands \
    during that same month. Basically we have information on a daily and monthly basis.")
    st.write("Below you can see a summary of the findings of our study.")
    st.write("The following table contains our Chipotle customer behavior dataset along with information \
    about Chipotle facilities in each US state, such as the city, state, and a unique ID for each location. \
    In general, this information begins and ends in a monthly period, in which we have information on each \
    location monthly. We also have related_same_day_brand and related_same_month_brand columns that contain \
    information about the percentage of users who visited a specific Chipotle location and then, on the same \
    day or month, visited other different brands.")

    pandas_dataframe = pd.read_csv("pandas_top4_app_dataset.csv")
    visits_choice = st.sidebar.number_input('Filter by visits number:', step = True)
    states_choice = st.sidebar.selectbox('Filter by region:', states)

    if states_choice == " ":
        pandas_dataframe = pandas_dataframe[pandas_dataframe['raw_visit_counts'] >= visits_choice]
        st.dataframe(pandas_dataframe)
    else:
        pandas_dataframe = pandas_dataframe[pandas_dataframe['raw_visit_counts'] >= visits_choice]
        pandas_dataframe = pandas_dataframe[pandas_dataframe['region'] == states_choice]
        st.dataframe(pandas_dataframe)

    st.write("We provide you with a filter option to modify the table above and display Chipotle locations \
    with more than a certain number of visits. Please go ahead, take a look, and see what discover in this \
    dataset. Our filter option is located in the sidebar of the page.")

    st.write("The last two columns of our dataset (top4_same_day_brand and top4_same_month_brand) contain \
    a summary of the top 4 brands that Chipotle customers visited afterward. You will find the top 4 brands \
    corresponding to each row. This information can quickly help us to know which are those popular brands \
    that Chipotle customers prefer to go to often, either on the same day or in the same month of visiting Chipotle.")
    st.write("We have also prepared a spatial map to help you more accurately visualize the data provided \
    about Chipotle visitors. On the map below you can interactively navigate through it, and see the location \
    of each Chipotle facility distributed by state on a current map of the United States. Feel free to inspect \
    it all you want and discover what amazing insights we can get from this data.")

    st.map(pandas_dataframe)

    st.write("Lastly, we have prepared two charts showing the top 10 brands nationwide that Chipotle Customers \
    like to visit. Companies such as MacDonalds, Walmart, and Starbucks connected in both charts as the 3 companies \
    to be most visited by Chipotle customers in the United States, thus surpassing others in an extraordinary way. \
    This information is crucial to understand the consumer behavior of Chipotle customers, to the point that it can \
    be predicted through a more detailed study, which companies these users will visit on the same day or month if \
    they visit Chipotle. This can certainly lead to future partnerships between brands, increase their revenue, and \
    so help each other to grow in extraordinary ways.")

    top10_most_popular_same_day_table = pd.read_csv("same_day_brand_data.csv")
    same_day_plot = (ggplot(top10_most_popular_same_day_table)
    + geom_col(aes(x='same_day_brand', y ='same_day_numOfTimes_reached_top4'), width = 0.50, fill = '#0080ff')
    + theme(figure_size=(23, 15), text = element_text(size = 20))
    + labs(x='Top 10 Brands that reached Top 4', y='Number of Times the brand reached the top 4', title="Top 10 Companies that most reached the Top 4")
    )
    st.pyplot(ggplot.draw(same_day_plot))

    top10_most_popular_same_month_table = pd.read_csv("same_month_brand_data.csv")


    same_month_plot = (ggplot(top10_most_popular_same_month_table)
    + geom_col(aes(x='same_month_brand', y ='month_day_numOfTimes_reached_top4'), width = 0.50, fill = 'red')
    + theme(figure_size=(33, 20), text = element_text(size = 22))
    + labs(x='Top 10 Brands that reached Top 4 in the month', y='Number of Times the brand reached the top 4', title="Top 10 Companies that most reached the Top 4")
    )
    
    st.pyplot(ggplot.draw(same_month_plot))

    st.write("For more details related to the code implemented to generate these charts, please go to the other \
    page 'Pyspark Source Code'. Thank you!")


elif current_page == "Pyspark Source Code":
    st.title("Analytics Deployment App - Final Project DS 460")
    st.subheader("Pyspark Code:")
    st.write("Please, wait a few seconds while the Pyspark code loads. Thank you!")
    st.write("Description of the data format: The pyspark function to_json() was used to download the full dataset \
    of 30,000 records. Databricks was presenting impediments to download the full dataset since the dataframe, \
    worked up to a certain point, contained columns of StructType which cannot be written as csv format. Solution \
    for this was to transform the StructType columns into JSON format. This solved the problem, and now the csv data \
    is in a format that is easier for Pandas to work with.")

    HtmlFile = open("Analytics_Deployment_App.html")
    source_code = HtmlFile.read() 
    components.html(source_code, height = 500)

elif current_page == "Spacial Maps":
    st.title("Analytics Deployment App - Final Project DS 460")
    st.write("Please, wait about 30 seconds while the spatial maps are loaded. Also when switching from the Spatial Maps page \
    to ther other pages, you are probably going to experience some delay time, about 40 seconds. Don't worry, this is due to \
    the plotly library being used for the spacial maps which doesn't do very well handling very large records. In our case \
    our dataset contains about 30,000 records. This will slow a little the runtime process of our streamlit app, thank you for being \
    so patient!")

    st.write("The Spacial Maps included here display the top 10 brands by their color ranking. Blue for ranking 1, \
    purple for ranking 2, orange for ranking 3, and yellow for ranking 4. This will help us to see what locations in the US \
    were more populated with brands of a specific ranking.")

    plotly_day = pd.read_csv("lat_long_same_day_topBrands.csv")
    plotly_day['text_to_display'] = plotly_day['same_day_brand'] + ' - Raking Top: ' + plotly_day['same_day_top_rank'].astype(str)

    same_day_fig = go.Figure(data=go.Scattergeo(
        lon = plotly_day['longitude'],
        lat = plotly_day['latitude'],
        text = plotly_day['text_to_display'],
        mode = 'markers',
        marker_color = plotly_day['same_day_top_rank'],
        ))

    same_day_fig.update_layout(
        title = 'Top 10 Brands Located by State - Top Same Day',
        geo_scope='usa',
    )

    st.plotly_chart(same_day_fig)

    plotly_month = pd.read_csv("lat_long_month_topBrands.csv")
    plotly_month['text_to_display'] = plotly_month['same_month_brand'] + ' - Raking Top: ' + plotly_month['same_month_top_rank'].astype(str)

    same_month_fig = go.Figure(data=go.Scattergeo(
        lon = plotly_month['longitude'],
        lat = plotly_month['latitude'],
        text = plotly_month['text_to_display'],
        mode = 'markers',
        marker_color = plotly_month['same_month_top_rank'],
        ))

    same_month_fig.update_layout(
        title = 'Top 10 Brands Located by State - Top Same Month',
        geo_scope='usa',
    )

    st.plotly_chart(same_month_fig)
