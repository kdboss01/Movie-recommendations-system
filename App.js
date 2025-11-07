import React, { useState } from "react";
import "./App.css";
import { FaFilm, FaSearch } from "react-icons/fa";

function App() {
  const [movie, setMovie] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");

  const getRecommendations = async () => {
    setErrorMsg("");
    setRecommendations([]);

    if (!movie.trim()) {
      setErrorMsg("Please enter a movie name.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ movie }),
      });

      const data = await response.json();

      if (response.status === 404) {
        setErrorMsg(
          "🎬 Movie not found! Check spelling — this search bar is case sensitive."
        );
      } else if (data.recommendations) {
        setRecommendations(data.recommendations);
      } else {
        setErrorMsg("⚠️ Unexpected response from server.");
      }
    } catch (error) {
      console.error("Backend error:", error);
      setErrorMsg("❌ Server not responding. Check Flask backend.");
    }
  };

  return (
    <div className="App">
      <header className="header">
        <FaFilm className="icon" />
        <h1>MOVIE RECOMMENDATION SYSTEM</h1>
      </header>

      <div className="search-section">
        <input
          type="text"
          placeholder="Enter movie name..."
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
        />
        <button onClick={getRecommendations}>
          <FaSearch /> Get Recommendations
        </button>
      </div>

      {errorMsg && <div className="error-banner">{errorMsg}</div>}

      <div className="results">
        {recommendations.map((title, i) => (
          <div key={i} className="card">
            <div className="card-content">
              <h3>{title}</h3>
              <p>🎥 Recommended Movie #{i + 1}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
