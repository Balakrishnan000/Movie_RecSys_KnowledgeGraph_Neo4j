from datetime import datetime
from enum import auto
from py2neo import Graph

import streamlit as st
import pickle 
import pandas as pd
import requests
import streamlit.components.v1 as components
from PIL import Image

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""


user = "neo4j"
pswd = "0asNuYzn5LVJTyWfb3pJzbqwnkAT3x7HIIWF3WmbDi8"

# Make sure the database is started first, otherwise attempt to connect will fail
try:
    graph = Graph('neo4j+s://fea93aac.databases.neo4j.io', auth=(user, pswd))
    print('SUCCESS: Connected to the Neo4j Database.')
except Exception as e:
    print('ERROR: Could not connect to the Neo4j Database. See console for details.')
    raise SystemExit(e)

my_api_key = '4051077e7188c536fc7feb16b656bbd0'

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id,my_api_key))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']


movie_dict = pickle.load(open('movie_dict.pkl','rb'))
#new df is now here via the file - as dict
movies = pd.DataFrame(movie_dict)



st.title('Movie Recommender System - Based on Knowledge Graph')
selected_movie_name = st.selectbox(
     'Select and click Recommend Me ',
     movies['title'].values)
st.write('You selected:', selected_movie_name)



if st.button('Recommend Me'):
    with st.spinner("Loading..."):
        query = """MATCH (:Movie {title:\""""+ selected_movie_name +"""\"})<-[:Directed|Acted_in]-(p)-[:Directed|Acted_in]->(m) RETURN distinct(m)"""
        print(query)
        movies = graph.run(query).data()
        ctr = 1
    
        for mv in movies:
            st.write(str(ctr)+".  "+mv['m']['title'])
            st.write("Main Actor = "+mv['m']['actor1']+", Director = "+mv['m']['director'])
            st.image(fetch_poster(mv['m']['movie_id']),width=140)
            ctr+=1



#Removing the made by 
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
