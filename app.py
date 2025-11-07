from flask import Flask, jsonify, request
import pickle
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the saved data
movies = pickle.load(open('model/movies.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

@app.route('/')
def home():
    return "🎬 Movie Recommendation API Running!"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movie_name = data.get('movie', '').strip()

    if not movie_name:
        return jsonify({"error": "Movie name cannot be empty"}), 400

    # Validate movie exists
    if movie_name not in movies['title'].values:
        return jsonify({"error": "Movie not found"}), 404

    # Find similar movies
    index = movies[movies['title'] == movie_name].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    # Get top 5 recommendations
    recommended_titles = [movies.iloc[i[0]].title for i in distances[1:6]]

    # Directly return titles only — no poster fetching
    return jsonify({
        "recommendations": recommended_titles
    })

if __name__ == '__main__':
    app.run(debug=True)
