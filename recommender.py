import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
data = pd.read_csv("data/courses.csv")

# Combine text columns
data["combined"] = (
    data["Course Name"].astype(str) + " " +
    data["Category"].astype(str) + " " +
    data["Description"].astype(str) + " " +
    data["Skills"].astype(str)
)

# Load AI model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
course_embeddings = model.encode(data["combined"])


def recommend_courses(user_interest):

    # ✅ FIX: define recommendations list
    recommendations = []

    # Convert user input to embedding
    user_embedding = model.encode([user_interest])

    similarity = cosine_similarity(user_embedding, course_embeddings)

    scores = similarity[0]

    top_indices = scores.argsort()[::-1][:5]

    for index in top_indices:

        recommendations.append({
            "Course Name": data.iloc[index]["Course Name"],
            "Category": data.iloc[index]["Category"],
            "Level": data.iloc[index]["Level"],
            "Image": data.iloc[index]["Image"]
        })

    return recommendations
