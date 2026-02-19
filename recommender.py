import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load dataset
data = pd.read_csv("data/courses.csv")

# Combine fields
data["combined"] = (
    data["Course Name"].astype(str) + " " +
    data["Category"].astype(str) + " " +
    data["Level"].astype(str) + " " +
    data["Description"].astype(str) + " " +
    data["Skills"].astype(str)
)

# Create TF-IDF model (LIGHTWEIGHT)
vectorizer = TfidfVectorizer(stop_words="english")

course_vectors = vectorizer.fit_transform(data["combined"])


def recommend_courses(user_input, top_n=5):

    user_vector = vectorizer.transform([user_input])

    similarity = cosine_similarity(user_vector, course_vectors)[0]

    top_indices = similarity.argsort()[::-1][:top_n]

    recommendations = []

    for idx in top_indices:

        recommendations.append({
            "Course Name": data.iloc[idx]["Course Name"],
            "Category": data.iloc[idx]["Category"],
            "Level": data.iloc[idx]["Level"],
            "Duration": data.iloc[idx]["Duration"],
            "Price": data.iloc[idx]["Price"],
            "Rating": data.iloc[idx]["Rating"],
            "Image": data.iloc[idx]["Image"]
        })

    return recommendations
