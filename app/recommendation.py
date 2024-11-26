from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_jobs(reviews, target_user, top_n=5):
    df = pd.DataFrame(reviews)
    
    df['normalized_score'] = 0.5 * (df['rating'] / 5) + 0.5 * (df['recommendation'] / 10)
    
    # Create a user-job matrix
    user_job_matrix = df.pivot_table(
        index='author', columns='_id', values='normalized_score'
    )
    
    # Fill NaN values with 0 (unrated jobs)
    user_job_matrix = user_job_matrix.fillna(0)
    
    # Compute cosine similarity between users
    user_similarity = cosine_similarity(user_job_matrix)
    user_similarity_df = pd.DataFrame(
        user_similarity, index=user_job_matrix.index, columns=user_job_matrix.index
    )
    
    # Find similar users to the target user
    similar_users = user_similarity_df[target_user].sort_values(ascending=False)
    # Get jobs rated by similar users that the target user hasn't rated
    target_user_ratings = user_job_matrix.loc[target_user]
    unrated_jobs = target_user_ratings[target_user_ratings == 0].index
    
    # Calculate predicted scores for unrated jobs
    job_scores = {}
    for job in unrated_jobs:
        weighted_score = 0
        similarity_sum = 0
        
        for similar_user, similarity in similar_users.items():
            if similar_user != target_user:  # Skip the target user
                similar_user_rating = user_job_matrix.loc[similar_user, job]
                if similar_user_rating > 0:  # Only consider jobs they rated
                    weighted_score += similarity * similar_user_rating
                    similarity_sum += similarity
        
        # Avoid division by zero
        if similarity_sum > 0:
            job_scores[job] = weighted_score / similarity_sum
    
    # Sort jobs by predicted score and get top N
    recommended_job_ids = sorted(job_scores, key=job_scores.get, reverse=True)[:top_n]
    
    # Return the full job dicts for the recommended job IDs
    recommended_jobs = [
        review for review in reviews if review['_id'] in recommended_job_ids
    ]
    
    return recommended_jobs

# Example usage
reviews = [
    {'author': 1, '_id': 'A', 'rating': 4, 'recommendation': 8},
    {'author': 1, '_id': 'B', 'rating': 5, 'recommendation': 9},
    {'author': 2, '_id': 'A', 'rating': 3, 'recommendation': 7},
    {'author': 2, '_id': 'C', 'rating': 4, 'recommendation': 6},
    {'author': 3, '_id': 'B', 'rating': 4, 'recommendation': 9},
    {'author': 3, '_id': 'C', 'rating': 5, 'recommendation': 10},
    {'author': 3, '_id': 'D', 'rating': 3, 'recommendation': 6},
]

target_user = 1
top_n = 2

recommended_jobs = recommend_jobs(reviews, target_user, top_n)
print("Recommended jobs for user", target_user, ":", recommended_jobs)
