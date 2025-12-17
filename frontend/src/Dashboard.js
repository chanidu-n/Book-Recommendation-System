import React from 'react';
import { motion } from 'framer-motion';
import { FaStar, FaBook, FaChartLine } from 'react-icons/fa';
import Chatbot from './Chatbot';

function Dashboard({ result, genreColor }) {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { duration: 0.5 }
    }
  };

  return (
    <motion.div
      className="dashboard-container"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <div className="dashboard-grid">
        {/* Rating Card */}
        <motion.div
          className="dashboard-card rating-card"
          variants={itemVariants}
          whileHover={{ scale: 1.02, y: -5 }}
        >
          <div className="card-header">
            <FaStar className="card-icon" style={{ color: genreColor }} />
            <h3>Predicted Rating</h3>
          </div>
          <motion.div
            className="rating-display"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.5, type: 'spring', stiffness: 200 }}
          >
            <motion.span
              className="rating-number"
              style={{ color: genreColor }}
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 1, repeat: Infinity, repeatDelay: 2 }}
            >
              {result.predicted_rating}
            </motion.span>
            <span className="rating-max">/ 5.0</span>
          </motion.div>
          
          {/* Star Rating Visual */}
          <div className="stars">
            {[...Array(5)].map((_, i) => (
              <motion.span
                key={i}
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.7 + i * 0.1 }}
              >
                <FaStar
                  className={i < Math.round(result.predicted_rating) ? 'star filled' : 'star'}
                  style={{ color: i < Math.round(result.predicted_rating) ? genreColor : '#444' }}
                />
              </motion.span>
            ))}
          </div>
        </motion.div>

        {/* Recommended Books Card */}
        <motion.div
          className="dashboard-card books-card"
          variants={itemVariants}
          whileHover={{ scale: 1.02, y: -5 }}
        >
          <div className="card-header">
            <FaBook className="card-icon" style={{ color: genreColor }} />
            <h3>Top Recommendations</h3>
          </div>
          <div className="books-list">
            {result.recommended_books.map((book, i) => (
              <motion.div
                key={i}
                className="book-item"
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.8 + i * 0.2 }}
                whileHover={{
                  x: 10,
                  backgroundColor: `${genreColor}15`,
                  borderLeftColor: genreColor
                }}
              >
                <span className="book-number" style={{ backgroundColor: genreColor }}>
                  {i + 1}
                </span>
                <span className="book-title">{book}</span>
                <motion.span
                  className="book-arrow"
                  whileHover={{ x: 5 }}
                >
                  →
                </motion.span>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Statistics Card */}
        <motion.div
          className="dashboard-card stats-card"
          variants={itemVariants}
          whileHover={{ scale: 1.02, y: -5 }}
        >
          <div className="card-header">
            <FaChartLine className="card-icon" style={{ color: genreColor }} />
            <h3>Analysis Insights</h3>
          </div>
          <div className="stats-grid">
            <motion.div
              className="stat-item"
              whileHover={{ scale: 1.05 }}
            >
              <span className="stat-label">Quality Score</span>
              <motion.div
                className="stat-bar"
                initial={{ width: 0 }}
                animate={{ width: `${(result.predicted_rating / 5) * 100}%` }}
                transition={{ delay: 1, duration: 1 }}
                style={{ backgroundColor: genreColor }}
              />
              <span className="stat-value">{((result.predicted_rating / 5) * 100).toFixed(0)}%</span>
            </motion.div>
            
            <motion.div
              className="stat-item"
              whileHover={{ scale: 1.05 }}
            >
              <span className="stat-label">Match Confidence</span>
              <motion.div
                className="stat-bar"
                initial={{ width: 0 }}
                animate={{ width: '92%' }}
                transition={{ delay: 1.2, duration: 1 }}
                style={{ backgroundColor: genreColor }}
              />
              <span className="stat-value">92%</span>
            </motion.div>

            <motion.div
              className="stat-item"
              whileHover={{ scale: 1.05 }}
            >
              <span className="stat-label">Popularity Index</span>
              <motion.div
                className="stat-bar"
                initial={{ width: 0 }}
                animate={{ width: '85%' }}
                transition={{ delay: 1.4, duration: 1 }}
                style={{ backgroundColor: genreColor }}
              />
              <span className="stat-value">85%</span>
            </motion.div>
          </div>
        </motion.div>

        {/* Chatbot */}
        <motion.div variants={itemVariants} className="chatbot-wrapper">
          <Chatbot genreColor={genreColor} />
        </motion.div>
      </div>
    </motion.div>
  );
}

export default Dashboard;