import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load dataset fresh every time
def load_data():
    data = pd.read_csv("data/courses.csv")

    # Create strong combined text
    data["combined"] = data.apply(
    lambda row: (
        f"Course: {row['Course Name']}. "
        f"Category: {row['Category']}. "
        f"Level: {row['Level']}. "
        f"Description: {row['Description']}. "
        f"Skills: {row['Skills']}."
    ),
    axis=1
)


    return data


# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# Recommendation function
def recommend_courses(user_input, top_n=5):

    data = load_data()

    # Generate embeddings for courses
    course_embeddings = model.encode(
        data["combined"].tolist(),
        normalize_embeddings=True
    )

    # Generate embedding for user input
    user_embedding = model.encode(
        [user_input],
        normalize_embeddings=True
    )

    # Calculate similarity
    similarity_scores = cosine_similarity(
        user_embedding,
        course_embeddings
    )[0]

    # Get top results
    top_indices = similarity_scores.argsort()[::-1][:top_n]

    recommendations = []

    for idx in top_indices:

        recommendations.append({
            "Course Name": data.iloc[idx]["Course Name"],
            "Category": data.iloc[idx]["Category"],
            "Level": data.iloc[idx]["Level"],
            "Duration": data.iloc[idx]["Duration"],
            "Price": data.iloc[idx]["Price"],
            "Rating": data.iloc[idx]["Rating"],
            "Image": data.iloc[idx]["Image"],
            "Score": float(similarity_scores[idx])
        })

    return recommendations
