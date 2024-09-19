from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import random
from get_poster import get_movie_poster
import pandas as pd
from get_model_prediction import model_prediction

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# Optional: Configuring session to server-side session (memory storage)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)  # Initialize the session with the app

# Load movie data
movie_id_title_df = pd.read_csv('final_merged_df_for_model.csv')
movie_id_title_dict = {movie_id_title_df['title'][i]: int(movie_id_title_df['movieId'][i]) for i in range(len(movie_id_title_df))}
MOVIES_PER_BATCH = 10

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')  # Render the new home page

@app.route('/select_movie')
def show_movie_posters():
    page = int(request.args.get('page', 1))  # Get page number from request
    start = (page - 1) * MOVIES_PER_BATCH
    end = start + MOVIES_PER_BATCH
    movie_titles = list(movie_id_title_dict.keys())[start:end]  # Get a batch of movie titles

    posters = []
    for movie_title in movie_titles:
        poster_url = get_movie_poster(movie_title)
        if poster_url:
            posters.append({'title': movie_title, 'poster_url': poster_url})

    return render_template('movies.html', posters=posters, page=page)

# When a user clicks on a movie poster, it will recommend similar movies
@app.route('/movie/<title>')
def get_movie_id_and_recommend(title):
    movie_id = movie_id_title_dict.get(title)
    if movie_id:
        # Get movie recommendations based on the model prediction
        prediction = model_prediction(movie_id, session)
        similar_movies = []
        
        # For each recommended movie title, fetch the poster
        for similar_movie_title in prediction['title']:
            poster_url = get_movie_poster(similar_movie_title)
            if poster_url:
                similar_movies.append({'title': similar_movie_title, 'poster_url': poster_url})

        return render_template('prediction.html', posters=similar_movies, movie_title=title)
    return jsonify({'error': 'Movie not found'}), 404

# Predict route for JSON-based prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    posters = []
    movie_id = data.get('movie_id')
    prediction = model_prediction(movie_id, session)
    for movie_title in prediction['title']:
        poster_url = get_movie_poster(movie_title)
        if poster_url:
            posters.append({'title': movie_title, 'poster_url': poster_url})

    return render_template('prediction.html', posters=posters)


@app.route('/movies')
def load_more_movies():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', MOVIES_PER_BATCH))
    movie_titles = list(movie_id_title_dict.keys())[offset:offset + limit]

    posters = []
    for movie_title in movie_titles:
        poster_url = get_movie_poster(movie_title)
        if poster_url:
            posters.append({'title': movie_title, 'poster_url': poster_url})

    return jsonify({'movies': posters})




if __name__ == '__main__':
    app.run(debug=True)
