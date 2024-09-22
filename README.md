# Personalised Recommendation system using Neural Collaborative Filtering


### Step 1: Train NCF Model on Movie Ratings
**Objective**: Use hard sampling to improve the model.

- **Interaction Matrix**: Created a matrix of users and items (movies).
- **Labels**: 
  - Positive interaction: labeled as 1.
    - **Hard Positive**: Rating ≥ 4.
    - **Soft Positive**: Rating ≥ 3.
  - Negative interaction: labeled as 0.
    - **Hard Negative**: Rating ≤ 1.
    - **Soft Negative**: 2 ≤ Rating < 3.

- **Sampling**: For each positive interaction, 4 negative interactions were sampled for the same user. 
- **Final Dataset Format**: 
  - `index | userid | movieid | interaction | rating`.

**Outcome**: Trained the NCF model on this data.

---

### Step 2: Prepare User, Movie, and Genre Embeddings
1. **User Embedding**:
   - Movies with positive interactions were selected (interaction = 1).
   - Used the movie description metadata and computed embeddings using the Lamini model on Hugging Face.
   - **User embedding**: Calculated as the mean of all positive movie embeddings for that user.
   - **Reasoning**: This dense vector represents the user's preferences, which can then be compared with movie embeddings to predict future likes.

2. **Genre Embedding**:
   - Movies were grouped by genres (a movie can belong to multiple genres).
   - **Genre embedding**: Calculated as the mean of all movies belonging to that genre.
     - Example: Embedding of "Comedy" = Mean of all comedy movie embeddings.
   - **User-Genre Similarity**: Compared the user embedding with genre embeddings to find genres the user is likely to enjoy.
   - **Genre-Genre Similarity Matrix**: A 17x17 matrix was computed to determine similarities between different genres. This helps in recommending genres related to ones the user already likes.

---

### Step 3: Calculate User Embeddings for All Users and Compute Median Similarity Scores
- Repeated the embedding process for all users.
- Calculated user-genre similarity for every user and stored results in a nested dictionary (dict of DataFrames).
- **Median Similarity Score**: Computed for each user.
  - Genres with similarity scores higher than the median were classified as positive genres for the user.
  - Genres with similarity scores lower than the median were classified as negative genres for the user.

---

### Step 4: Identify Actual Positive and Negative Genres for Each User
- **Actual Positive Genres**: 
  - Intersection of genres where the similarity score is higher than the median and the user has interacted positively with the genre.
  - Example: If a user has high similarity with "Action" but low similarity with "Animation," the model would only mark "Action" as a positive genre.

- **Actual Negative Genres**:
  - Genres where the similarity score is lower than the median and the user hasn't interacted with them.

- **Final Dataset**:
  - Maintained a 1:3 ratio of positive to negative genres.
  - `userid | movieid | interaction | genre | movie title`.

---

### Step 5: Fine-Tune NCF Model on New Data
- Fine-tuned the previously trained NCF model on this new dataset.
- **Final Metrics**:
  - Precision@k: 0.4
  - Recall@k: 0.2-0.3
  - NDCG@10: 0.302 (varies by user).
  - **Genre NDCG@10**: 0.84, indicating that most suggested movies belonged to similar or related genres.

---

### Step 6: Frontend Development
- Created a frontend for the model using Flask, Spline.js, HTML, and CSS.
- Deployed the app as a web service using Azure App Service.
- **User Interface**: Users can hover over movie posters, select them, and view 10 recommended movie posters based on the model's predictions.


