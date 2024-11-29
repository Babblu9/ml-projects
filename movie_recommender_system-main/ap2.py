import streamlit as st
import pickle
import requests

# Set fullscreen layout
st.set_page_config(layout="wide", page_title="Movie Recommender System")

# Custom CSS for a modern, fullscreen UI
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .stButton button {
        background-color: #E50914;
        color: white;
        font-weight: bold;
        font-size: 16px;
        border-radius: 8px;
        padding: 0.5em 1em;
        margin-top: 1em;
    }
    .stButton button:hover {
        background-color: #ff1e1e;
        color: white;
    }
    .movie-container {
        padding: 1em;
        background-color: #1e1e1e;
        border-radius: 10px;
        margin: 0.5em;
        text-align: center;
    }
    .movie-title {
        color: #E50914;
        font-weight: bold;
        font-size: 18px;
        margin-top: 0.5em;
    }
    .movie-overview {
        font-size: 14px;
        margin-top: 0.5em;
        color: #cccccc;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}", data.get("vote_average"), data.get("overview")
        else:
            return "https://via.placeholder.com/500", None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500", None, None

# Load movie data and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Header and introduction
st.title("🎬 Movie Recommender System")
st.write("Find your next favorite movie by selecting one from the dropdown below!")

# Image Carousel (Example images for the carousel)
import streamlit.components.v1 as components
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# Display example images in the carousel
imageUrls = [
    fetch_poster(1632)[0],
    fetch_poster(299536)[0],
    fetch_poster(17455)[0],
    fetch_poster(2830)[0],
    fetch_poster(429422)[0],
]
imageCarouselComponent(imageUrls=imageUrls, height=300)

# Movie selection dropdown
selectvalue = st.selectbox("Select a movie:", movies_list)

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movies = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        title = movies.iloc[i[0]].title
        poster, rating, overview = fetch_poster(movie_id)
        recommend_movies.append({"title": title, "poster": poster, "rating": rating, "overview": overview})
    return recommend_movies

# Display recommendations when the button is clicked
if st.button("Show Recommendations"):
    recommendations = recommend(selectvalue)
    
    # Display recommendations in a responsive grid
    cols = st.columns(5)  # Create 5 columns for the grid layout
    for index, movie in enumerate(recommendations):
        with cols[index % 5]:  # Rotate through columns for each movie
            st.markdown(f"""
                <div class="movie-container">
                    <img src="{movie['poster']}" width="100%" style="border-radius:10px;"/>
                    <div class="movie-title">{movie['title']}</div>
                    <div>⭐ Rating: {movie['rating'] if movie['rating'] else 'N/A'}</div>
                    <div class="movie-overview">{movie['overview'][:100] + '...' if movie['overview'] else 'No overview available.'}</div>
                </div>
            """, unsafe_allow_html=True)
