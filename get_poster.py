import requests

TMDB_API_KEY = '3f8934a9cf2abda00378a5be0ae23f71'
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'  # Base URL for images

def get_movie_poster(movie_title):
    url = f'{BASE_URL}/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_title
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            return f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None
    return None
