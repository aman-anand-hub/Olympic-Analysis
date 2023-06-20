import numpy as np
def fetch_medal_tally(df,year,country):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        temp_df=medal_tally
    if year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_tally[medal_tally['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_tally[medal_tally['Year']==int(year)]
    if year!='Overall' and country!='Overall':
        temp_df=medal_tally[(medal_tally['Year']==year) & (medal_tally['region']==country)]

    if flag==1:
        temp_df=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        temp_df=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    temp_df['Total']=temp_df['Gold']+temp_df['Silver']+temp_df['Bronze']

    #temp_df['Gold'] = temp_df['Gold'].astype('int')
    #temp_df['Silver'] = temp_df['Silver'].astype('int')
    #temp_df['Bronze'] = temp_df['Bronze'].astype('int')

    return temp_df

def country_year_list(df):
    years= df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    return  years,country

def data_over_time(df,col):
    df=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    # inside my dataframe -> {Year, count}
    return  df

def heatmap_dataframe(df):
    hm_df= df
    hm_df= hm_df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = hm_df.groupby(['Sport', 'Year'])['Event'].count().unstack()
    return heatmap_data

def most_successful(df, sport):
    temp_df= df.dropna(subset=['Medal'])
    if sport!='Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    x= temp_df['Name'].value_counts().reset_index().merge(df,on='Name', how='left')[['Name','count', 'Sport', 'region']]
    x=x.drop_duplicates(['Name'])
    x=x.rename(columns={'count':'Medals'})
    return x

def yearwise_medaltally(df, country):
    df_new = df.dropna(subset=['Medal'])
    df_new = df_new.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    df_new = df_new[df['region'] == country]
    final_df = df_new.groupby(['Year']).count()['Medal']
    final_df.reset_index()
    final_df = final_df.to_frame()
    return final_df

def country_event_heatmap(df, country):
    df_new = df.dropna(subset=['Medal'])
    df_new = df_new.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    df_new = df_new[df['region'] == country]
    return df_new

def sport_wise_performance(df, country):
    df_new = df.dropna(subset=['Medal'])
    df_new = df_new.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    dff = df_new[df['region'] == country]
    return dff

def country_NumOfEvent_heatmap(df, country):
    df_new = df.dropna(subset=['Medal'])
    df_new = df_new.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    dff = df_new[df['region'] == country]
    pi_tab=dff.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0)
    return pi_tab

def most_successful_athletes_countrywise(df, country):
    temp_df= df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region']==country]
    x= temp_df['Name'].value_counts().reset_index().merge(df,on='Name', how='left')[['Name','count', 'Sport', 'region']]
    x=x.drop_duplicates(['Name'])
    x=x.rename(columns={'count':'Medals'})
    return x

def weight_vs_height(df, sport):
    athlete_df= df.drop_duplicates(['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace =True)
    if sport!='Overall':
        temp_df= athlete_df[athlete_df['Sport']== sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df= df.drop_duplicates(['Name','region'])
    men= athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women= athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    final= men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x':'Male', 'Name_y':'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final