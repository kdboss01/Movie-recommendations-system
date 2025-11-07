import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv('movies.csv')

# Some columns are lists in string form, so we need to convert them
def convert(obj):
    try:
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return " ".join(L)
    except:
        return ""

movies['cast'] = movies['cast'].apply(convert)
movies['crew'] = movies['crew'].apply(convert)

# Combine text features
movies['tags'] = movies['cast'] + ' ' + movies['crew']

# Vectorize text data
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = tfidf.fit_transform(movies['tags'])

# Compute similarity matrix
similarity = cosine_similarity(vectors)

# Save for later use
pickle.dump(movies, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("✅ movies.pkl and similarity.pkl created successfully!")
