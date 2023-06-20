import streamlit as st
import pandas as pd
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.express as px

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu=st.sidebar.radio('Analysis Basis:',
                 ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete-Wise Analysis')
)

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Tally')
    if selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Tally in '+str(selected_year)+" Olympics")
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country+' Overall performance')
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country+" performance in "+str(selected_year)+" Olympics")
    st.table(medal_tally)

if user_menu=='Overall Analysis':
    editions= df['Year'].unique().shape[0]-1 # as per documentation one olympics was discarded (1906) year olympics
    cities= df['City'].unique().shape[0]  # shape=(rows, cols)-> rows= shape[0]
    sports= df['Sport'].unique().shape[0]
    events= df['Event'].unique().shape[0]
    athletes= df['Name'].unique().shape[0]
    nations= df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    st.title('Nations over time')
    nations_over_time= helper.data_over_time(df,'region')
    x1 = nations_over_time['Year']
    y1 = nations_over_time['count']
    fig1, ax1 = plt.subplots()
    ax1.plot(x1, y1)
    ax1.set_xlabel('Editions')
    ax1.set_ylabel('No. of countries')
    st.pyplot(fig1)

    st.title('Events over time')
    events_over_time=helper.data_over_time(df,'Event')
    x2 = events_over_time['Year']
    y2 = events_over_time['count']
    fig2, ax2 = plt.subplots()
    ax2.plot(x2, y2)
    ax2.set_xlabel('Editions')
    ax2.set_ylabel('No. of events')
    st.pyplot(fig2)

    st.title('Athletes over time')
    athletes_over_time= helper.data_over_time(df,'Name')
    x3 = events_over_time['Year']
    y3 = events_over_time['count']
    fig3, ax3 = plt.subplots()
    ax3.plot(x2, y2)
    ax3.set_xlabel('Editions')
    ax3.set_ylabel('No. of Athletes')
    st.pyplot(fig3)

    st.title('Frequency of events')
    heatmap_data=helper.heatmap_dataframe(df)
    plt.figure(figsize=(20,20))
    sns.heatmap(heatmap_data,annot=True, fmt='g', cmap='YlGnBu')
    plt.xlabel('Edition')
    plt.ylabel('Sport')
    st.pyplot(plt.gcf()) #plt.gcf() -> current figure in matplotlib

    st.title('Top athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    sport_selected=st.selectbox('Select a sport', sports_list)
    x=helper.most_successful(df,sport_selected)
    st.table(x.head(15))

if user_menu=='Country-Wise Analysis':
    st.sidebar.title('Country-Wise Analysis')
    country_df=df['region'].dropna().unique().tolist()
    country_df.sort()
    country_selected_dropdown=st.sidebar.selectbox('Select a country',country_df)

    final_df=helper.yearwise_medaltally(df,country_selected_dropdown)
    st.title(country_selected_dropdown+' medal tally over the years')
    x = final_df.index
    y = final_df['Medal']
    plt.plot(x,y)
    plt.xlabel('Edition')
    plt.ylabel('Medals won')
    st.pyplot(plt)


    st.title(country_selected_dropdown+' excels in')
    country_excel_sports=helper.sport_wise_performance(df,country_selected_dropdown)
    pivot_table=country_excel_sports.pivot_table(index='Sport', columns='Year', values='Medal',aggfunc='count').fillna(0)
    plt.figure(figsize=(20,20))
    sns.heatmap(pivot_table,annot=True)
    st.pyplot(plt.gcf())

    st.title('Top 10 Successful Athletes')
    dataframe_top10_athletes_countrywise=helper.most_successful_athletes_countrywise(df,country_selected_dropdown)
    st.table(dataframe_top10_athletes_countrywise.head(10))

if user_menu=='Athlete-Wise Analysis':
    st.title('Distribution of Age')
    athlete_df = df.drop_duplicates(['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig1 = ff.create_distplot([x1, x2, x3, x4],
                              ['Overall age parameter', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                              show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig1)

    st.title('Distribution of Age wrt Sports(Gold Medalist)')
    x= []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig_plot = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig_plot.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig_plot)


    st.title('Height vs Weight')
    Sport_List= df['Sport'].unique().tolist()
    Sport_List.sort()
    Sport_List.insert(0,'Overall')
    Selected_Sport= st.selectbox('Select a Sport', Sport_List)
    temp_DF= helper.weight_vs_height(df, Selected_Sport)

    FIG, ax= plt.subplots()
    ax = sns.scatterplot(data=temp_DF, x='Weight', y='Height', hue='Medal', style='Sex', s=60)
    st.pyplot(FIG)

    st.title('Men vs Women Participation over the years')
    final_DF= helper.men_vs_women(df)
    FIG1= px.line(final_DF, x='Year', y=['Male', 'Female'])
    FIG1.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(FIG1)