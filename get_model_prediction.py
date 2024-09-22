import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Flatten, concatenate, Dense
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
import numpy as np
from keras.layers import Input, Embedding, Flatten, concatenate, Dense, Dropout
from keras.models import Model
from keras.callbacks import EarlyStopping
from keras.regularizers import l2
import pandas as pd
import os
import random
from keras.models import load_model

# Load the pre-trained model through azure blob storage
from azure.storage.blob import BlobServiceClient


Your_Connection_String = "DefaultEndpointsProtocol=https;AccountName=ncfmodel;AccountKey=agKsxKVtG5JrWhS4XSyzoW5huV5kjwgyf54KldtHC4GlWxdHoCufkmrKQb8qgndvqoRdtMT/xHN++AStio3RZA==;EndpointSuffix=core.windows.net"

def download_model_from_blob(container_name, blob_name, download_path):
    blob_service_client = BlobServiceClient.from_connection_string("Your_Connection_String")
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(download_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

# Call this function before loading the model
download_model_from_blob("model-for-ncf", "best_model_ncf.keras", "best_model_ncf.keras")

# Load the model
model = load_model("best_model_ncf.keras")
# model = load_model('best_model_ncf.keras')


def model_prediction(movie_id, session):
    final_df = pd.read_csv('final_merged_df_for_model.csv')

    # Initialize the session storage if it doesn't exist
    if 'recommended_movies' not in session:
        session['recommended_movies'] = []

    # Generate all movie IDs
    all_movie_ids = final_df['movieId'].values

    # Use the movie_id passed to the function to generate predictions
    user_id = 1  # Optionally use a fixed user_id or one related to the session
    liked_movie_id = np.array([movie_id])  # Focus on the clicked movie_id

    # Predict probabilities for the user and all movies
    user_ids = np.array([user_id] * len(all_movie_ids))
    predictions = model.predict([user_ids, all_movie_ids])

    # Create a DataFrame with model predictions
    predictions_df = pd.DataFrame({'movieId': all_movie_ids, 'predicted_rating': predictions.flatten()})

    # Sort predictions by predicted rating
    new_df = predictions_df.sort_values(by = 'predicted_rating', ascending=False)

    # Drop the 'predicted_rating' column and set 'movieId' as the index
    new_df = new_df.drop("predicted_rating", axis=1)
    new_df = new_df.reset_index(drop=True)

    # Merge with final_df to get movie titles
    new_df = new_df.merge(final_df[['movieId', 'title']], on='movieId', how='left')

    # Remove duplicates based on title
    unique_df = new_df.drop_duplicates(subset=['title', 'movieId'])

    # Exclude the currently clicked movie from recommendations
    unique_df = unique_df[unique_df['movieId'] != movie_id]

    # Filter out movies that have already been recommended in this session
    already_recommended = session['recommended_movies']
    unique_df = unique_df[~unique_df['movieId'].isin(already_recommended)]

    # Get top 10 recommended movies
    recommended_movies = unique_df.head(10)

    # Update the session with these newly recommended movies
    session['recommended_movies'].extend(recommended_movies['movieId'].tolist())

    return recommended_movies
