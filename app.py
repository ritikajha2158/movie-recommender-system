import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    api_key = 'ab622df36475b63f4c8134685d20480a'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()


    # Check if 'poster_path' exists in the response
    if 'poster_path' in data and data['poster_path']:
        return "http://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"  # Placeholder image URL


def recommend(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movie_list.iloc[i[0]].id
        recommended_movies.append(movie_list.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


# Load data
movie_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

# Select movie
selected_movie_name = st.selectbox('Enter a movie', movie_list['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
