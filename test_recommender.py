import pickle
import pandas as pd

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    if movie not in movies['title'].values:
        return "❌ Movie not found in dataset."
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    print(f"\n🎬 Movies similar to '{movie}':")
    for i in distances[1:6]:
        print(f"➡️ {movies.iloc[i[0]].title}")

# Test example
recommend('Avatar')
