import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Dashboard from './Dashboard';
import './App.css';


function App() {
const [genre, setGenre] = useState('Fantasy');
const [pages, setPages] = useState(300);
const [difficulty, setDifficulty] = useState(2);
const [result, setResult] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');


const recommend = async () => {
setLoading(true);
setError('');

try {
const res = await fetch('http://127.0.0.1:5000/recommend', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ genre, pages, difficulty })
});

if (!res.ok) {
throw new Error('Failed to fetch recommendations');
}

const data = await res.json();
setResult(data);
} catch (err) {
setError('Could not connect to server. Please check if backend is running.');
} finally {
setLoading(false);
}
};


const genres = [
{ value: 'Fantasy', emoji: '🧙‍♂️', color: '#9b59b6' },
{ value: 'SelfHelp', emoji: '💡', color: '#3498db' },
{ value: 'Education', emoji: '🎓', color: '#e74c3c' },
{ value: 'Mystery', emoji: '🔍', color: '#f39c12' },
{ value: 'Romance', emoji: '💖', color: '#e91e63' },
{ value: 'Science', emoji: '🔬', color: '#00bcd4' }
];


const selectedGenre = genres.find(g => g.value === genre) || genres[0];


return (
<div className="app-container">
{/* Animated Background */}
<div className="bg-animation">
{[...Array(20)].map((_, i) => (
<motion.div
key={i}
className="floating-book"
initial={{ y: -100, x: Math.random() * window.innerWidth }}
animate={{
y: window.innerHeight + 100,
x: Math.random() * window.innerWidth,
rotate: Math.random() * 360
}}
transition={{
duration: Math.random() * 10 + 10,
repeat: Infinity,
ease: 'linear',
delay: Math.random() * 5
}}
>
📚
</motion.div>
))}
</div>


<div className="content-wrapper">
        {/* Header */}
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, type: 'spring' }}
          className="header"
        >
          <motion.h1
            className="title"
            animate={{ scale: [1, 1.02, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            📚 Smart Book Advisor
          </motion.h1>
          <p className="subtitle">Discover your next favorite read with AI-powered recommendations</p>
        </motion.div>

        {/* Input Panel */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="input-panel"
          style={{ borderColor: selectedGenre.color }}
        >
          {/* Genre Selection */}
          <div className="input-section">
            <label className="input-label">
              <span className="label-icon">📖</span> Select Genre
            </label>
            <div className="genre-grid">
              {genres.map((g) => (
                <motion.button
                  key={g.value}
                  onClick={() => setGenre(g.value)}
                  className={`genre-card ${genre === g.value ? 'active' : ''}`}
                  style={{
                    borderColor: genre === g.value ? g.color : 'transparent',
                    backgroundColor: genre === g.value ? `${g.color}20` : 'transparent'
                  }}
                  whileHover={{ scale: 1.05, y: -5 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <span className="genre-emoji">{g.emoji}</span>
                  <span className="genre-name">{g.value}</span>
                </motion.button>
              ))}
            </div>
          </div>


          {/* Pages Slider */}
          <div className="input-section">
            <label className="input-label">
              <span className="label-icon">📄</span> Number of Pages: <strong>{pages}</strong>
            </label>
            <motion.input
              type="range"
              min="50"
              max="1000"
              value={pages}
              onChange={(e) => setPages(e.target.value)}
              className="slider"
              style={{
                background: `linear-gradient(to right, ${selectedGenre.color} 0%, ${selectedGenre.color} ${(pages / 1000) * 100}%, #2a2a2a ${(pages / 1000) * 100}%, #2a2a2a 100%)`
              }}
              whileFocus={{ scale: 1.02 }}
            />
            <div className="slider-labels">
              <span>50</span>
              <span>500</span>
              <span>1000</span>
            </div>
          </div>


          {/* Difficulty Slider */}
          <div className="input-section">
            <label className="input-label">
              <span className="label-icon">⚡</span> Difficulty Level: <strong>{['Easy', 'Medium', 'Hard', 'Expert', 'Master'][difficulty - 1]}</strong>
            </label>
            <motion.input
              type="range"
              min="1"
              max="5"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="slider"
              style={{
                background: `linear-gradient(to right, ${selectedGenre.color} 0%, ${selectedGenre.color} ${(difficulty / 5) * 100}%, #2a2a2a ${(difficulty / 5) * 100}%, #2a2a2a 100%)`
              }}
              whileFocus={{ scale: 1.02 }}
            />
            <div className="difficulty-indicators">
              {[1, 2, 3, 4, 5].map((level) => (
                <span
                  key={level}
                  className={`difficulty-dot ${difficulty >= level ? 'active' : ''}`}
                  style={{ backgroundColor: difficulty >= level ? selectedGenre.color : '#2a2a2a' }}
                />
              ))}
            </div>
          </div>


          {/* Analyze Button */}
          <motion.button
            onClick={recommend}
            disabled={loading}
            className="analyze-btn"
            style={{ backgroundColor: selectedGenre.color }}
            whileHover={{ scale: 1.05, boxShadow: `0 10px 30px ${selectedGenre.color}60` }}
            whileTap={{ scale: 0.95 }}
          >
            {loading ? (
              <>
                <motion.span
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  className="loading-spinner"
                >
                  ⚙️
                </motion.span>
                Analyzing...
              </>
            ) : (
              <>
                <span>🔮</span> Analyze & Recommend
              </>
            )}
          </motion.button>


          {/* Error Message */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="error-message"
              >
                ⚠️ {error}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>


        {/* Dashboard */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 50 }}
              transition={{ duration: 0.5 }}
            >
              <Dashboard result={result} genreColor={selectedGenre.color} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}


export default App;