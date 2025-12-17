import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaRobot, FaPaperPlane, FaTimes } from 'react-icons/fa';

function Chatbot({ genreColor }) {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;
    setMessage('');
    setChat([...chat, { user: userMessage, bot: null }]);
    setIsTyping(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await response.json();
      setIsTyping(false);
      setChat(prev => [...prev.slice(0, -1), { user: userMessage, bot: data.reply }]);
    } catch (error) {
      setIsTyping(false);
      setChat(prev => [...prev.slice(0, -1), { user: userMessage, bot: 'Sorry, I could not connect to the server.' }]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <motion.button
        className="chat-toggle-btn"
        onClick={() => setIsOpen(!isOpen)}
        style={{ backgroundColor: genreColor }}
        whileHover={{ scale: 1.1, rotate: 360 }}
        whileTap={{ scale: 0.9 }}
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.span
              key="close"
              initial={{ rotate: -180, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 180, opacity: 0 }}
            >
              <FaTimes />
            </motion.span>
          ) : (
            <motion.span
              key="open"
              initial={{ rotate: 180, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -180, opacity: 0 }}
            >
              <FaRobot />
            </motion.span>
          )}
        </AnimatePresence>
      </motion.button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="chatbot-container"
            initial={{ opacity: 0, y: 50, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.8 }}
            transition={{ type: 'spring', stiffness: 300, damping: 25 }}
          >
            <div className="chatbot-header" style={{ backgroundColor: genreColor }}>
              <FaRobot className="chatbot-icon" />
              <div>
                <h3>Book Assistant</h3>
                <span className="status">
                  <span className="status-dot"></span> Online
                </span>
              </div>
            </div>

            <div className="chatbot-messages">
              {chat.length === 0 && (
                <motion.div
                  className="welcome-message"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <FaRobot size={40} style={{ color: genreColor }} />
                  <p>Hi! I'm your book assistant. Ask me anything about books!</p>
                </motion.div>
              )}

              {chat.map((c, i) => (
                <div key={i}>
                  <motion.div
                    className="message user-message"
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                  >
                    <div className="message-content">
                      {c.user}
                    </div>
                  </motion.div>

                  {c.bot && (
                    <motion.div
                      className="message bot-message"
                      initial={{ opacity: 0, x: -50 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.3 }}
                    >
                      <FaRobot className="bot-avatar" style={{ color: genreColor }} />
                      <div className="message-content">
                        {c.bot}
                      </div>
                    </motion.div>
                  )}
                </div>
              ))}

              {isTyping && (
                <motion.div
                  className="message bot-message"
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                >
                  <FaRobot className="bot-avatar" style={{ color: genreColor }} />
                  <div className="message-content typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </motion.div>
              )}

              <div ref={chatEndRef} />
            </div>

            <div className="chatbot-input">
              <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me about books..."
                disabled={isTyping}
              />
              <motion.button
                onClick={sendMessage}
                disabled={isTyping || !message.trim()}
                style={{
                  backgroundColor: message.trim() ? genreColor : '#444',
                  cursor: message.trim() && !isTyping ? 'pointer' : 'not-allowed'
                }}
                whileHover={message.trim() && !isTyping ? { scale: 1.1 } : {}}
                whileTap={message.trim() && !isTyping ? { scale: 0.9 } : {}}
              >
                <FaPaperPlane />
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

export default Chatbot;