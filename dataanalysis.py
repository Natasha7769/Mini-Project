import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D


# 0. configure the page
st.set_page_config(
    page_title='Data Science App',
    page_icon='🧊',
    layout='wide',
)
# 1. Load the data
st.title('IPL analytics 2008-2019')
st.cache_data()
def load_data(url):
    df = pd.read_csv(url, encoding='ISO-8859-1')
    return df
# 2. Build the UI
with st.spinner('Loading data...'):
    df= load_data("DATA/matches.csv")
st.info('Matches')
st.dataframe(df,use_container_width=True)   

st.success('Column information of the dataset')
cols = df.columns.tolist()
st.write(f'Total Columns{len(cols)}➡️ {",".join(cols)}')

st.cache_data()

with st.spinner('Loading data...'):
    df1= load_data("Data/Top_100_batsman.csv")
st.info('Top 100 batsmen')
st.dataframe(df1,use_container_width=True)   


st.cache_data()

with st.spinner('Loading data...'):
    df1= load_data("Data/Top_100_bowlers.csv")
st.info('Top 100 bowlers')
st.dataframe(df1,use_container_width=True)

#Batsman insights

batsman=pd.read_csv("DATA/Top_100_batsman.csv",encoding ="ISO-8859-1")
st.title('Batsman KPIs')
Batsman_matches = batsman[batsman['Runs']>3000]  #Min 3000 run criteria
topfive=(Batsman_matches['PLAYER'].iloc[0:5]) #Top five batsmans


df = batsman
fig5 = px.bar(df,x=batsman['PLAYER'],y=batsman['Avg'],color=batsman['SR'])  #batsman KPI'S
st.plotly_chart(fig5)
st.title('Top 5 batsman based on runs')
fig6= go.Figure()
fig6.add_trace(go.Scatter(x=topfive, y=(batsman['Runs'].iloc[0:5]),
                          mode='lines+markers',
                          name='lines+markers'))
st.plotly_chart(fig6)     

# Team insights

Matches = pd.read_csv("DATA/matches.csv",encoding ="ISO-8859-1")
bat = Matches['toss_winner'].loc[Matches['toss_decision']=='bat']
battoss = (bat.value_counts())
st.title('Teams choose batting when they won toss')
data = bat
fig7 = px.bar(data, x= battoss.values, y=battoss.index)
st.plotly_chart(fig7)

field= Matches ['toss_winner'].loc[Matches['toss_decision']=='field']
fieldtoss = (field.value_counts())
data = field
st.title('Teams choose bowling when they won toss')
fig8 = px.bar(data, x=fieldtoss.values, y=fieldtoss.index)
st.plotly_chart(fig8)

st.title('Overall toss mapping')
Overalltosswin = fieldtoss+battoss
pie_col = ["Red","Blue","Yellow","Purple","Black","Indigo","Salmon","Olive","Green","Teal","Aqua","Silver","Navy","White"]
fig9 = px.pie(values= Overalltosswin.values, names= Overalltosswin.index)
st.plotly_chart(fig9)


count = Matches['winner'].value_counts()
st.title('Most successful team based on win count')
pie_col = ["Red","Blue","Yellow","Purple","Black","Indigo","Salmon","Olive","Green","Teal","Aqua","Silver","Navy","White"]
fig = px.pie(values= count.values, names= count.index)
st.plotly_chart(fig)


st.title('Player of the Match award')
count = Matches['player_of_match'].value_counts()
fig1 = go.Figure(data=[go.Scatter(
    x= count.index,y=count.head(5),
    mode='markers',
    marker=dict(
        color=['rgb(93,164,214)','rgb(255,144,14)',
               'rgb(44,160,101)', 'rgb(255,65,54)','yellow'],
        opacity=[1,0.8,0.6,0.4,0.3],
        size=[40,60,80,100,105]       
    )
)])
st.plotly_chart(fig1)


#Bowlers insights

st.plotly_chart(fig1)
st.title('Top 5 Blowers Based on wickets')
Bowlers=pd.read_csv("DATA/Top_100_bowlers.csv",encoding ="ISO-8859-1")
Bowlers_matches = Bowlers[Bowlers['Wkts']>50]
topfive = (Bowlers_matches['PLAYER'].iloc[0:5])
fig2= go.Figure()
fig2.add_trace(go.Scatter(x=topfive, y=(Bowlers['Wkts'].iloc[0:5]),
                          mode='lines+markers',
                          name='lines+markers'))
st.plotly_chart(fig2)

st.title('Bowlers KPI')
df= Bowlers

fig3= px.bar(df, x=Bowlers['PLAYER'], y=Bowlers['Econ'],color=Bowlers['Wkts'])
st.plotly_chart(fig3)

st.title('Bowlers who leaking more runs')
Bowlers_matches = Bowlers[Bowlers['Econ']>=8.50]
Ecobowlers = (Bowlers_matches['PLAYER'])
Economy = Bowlers_matches['Econ']
fig4 = px.pie(values=Economy, names= Ecobowlers)

st.plotly_chart(fig4)


# Load IPL matches dataset
df =pd.read_csv("DATA/matches.csv",encoding ="ISO-8859-1")

t1, t2 =  st.tabs(['Bivariate','Trivariate'])

num_cols = df.columns.tolist()

with t1:
    c1, c2 = st.columns(2)
    col1 = c1.radio('Select the First Column for scatter plot', num_cols)
    col2 = c2.radio('Select the Second Column for scatter plot', num_cols)
    
    fig = px.scatter(df, x=col1, y=col2, title=f'{col1} vs {col2}')
    st.plotly_chart(fig, use_container_width=True)

with t2:
    c1, c2, c3 = st.columns(3)
    col1 = c1.selectbox('Select the First Column for 3d plot', num_cols)
    col2 = c2.selectbox('Select the Second Column for 3d plot', num_cols)
    col3 = c3.selectbox('Select the Third Column for 3d plot', num_cols)
    
    fig_3d = px.scatter_3d(df, x=col1, y=col2, z=col3, title=f'{col1} vs {col2} vs {col3}', height=700)
    st.plotly_chart(fig_3d, use_container_width=True)