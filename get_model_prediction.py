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
from keras.models import load_model

# Initialize Azure Blob Storage client
def download_model(sas_url, download_path):
    # Check if the model file already exists locally
    if not os.path.exists(download_path):
        print("Downloading model...")
        response = requests.get(sas_url)
        if response.status_code == 200:
            # Write the model to the specified download path
            with open(download_path, 'wb') as file:
                file.write(response.content)
            print("Model downloaded successfully.")
        else:
            print(f"Failed to download model: {response.status_code} - {response.text}")
    else:
        print("Model already exists locally.")

# SAS URL of the model in Azure Blob
sas_url = 'https://ncfmodel.blob.core.windows.net/model-for-ncf/best_model_ncf.keras?sp=r&st=2024-09-22T19:12:43Z&se=2024-09-23T03:12:43Z&sv=2022-11-02&sr=b&sig=Emo6p5YlAxl5XGrm4UYc9RTuuCnR0THIbcvFx2eTnvg%3D'
# Local path where the model will be saved
download_path = './best_model_ncf.keras'
# Download the model if it's not already available
download_model(sas_url, download_path)

# Load the model
model = load_model(download_path)
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
