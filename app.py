import pickle
import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=bca1675900a670b621254ea43c744516&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]].id))

    return recommended_movies, recommended_movies_poster

st.title("Movie Recommendation System")

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open("similarity.pkl",'rb'))

selected_movie_name = st.selectbox(
    "Search Movies Here!",
    (movies['title'].values)
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], caption=names[i], use_column_width=True)

    cols = st.columns(5)
    for i in range(5, 10):
        with cols[i-5]:
            st.image(posters[i], caption=names[i], use_column_width=True)


