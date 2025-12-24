import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your AI assistant for the Physical AI textbook. Ask me anything about the book!",
      sender: "bot",
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSend = async () => {
    if (inputValue.trim() === '' || isLoading) return;

    // Add user message
    const newUserMessage = {
      id: Date.now(),
      text: inputValue,
      sender: "user",
      timestamp: new Date()
    };

    setMessages(prevMessages => [...prevMessages, newUserMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Hardcoded API URL for hackathon to eliminate env var complexity
      const API_URL = 'http://localhost:8000/rag/ask';

      // Make API call to backend
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputValue }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add bot response with sources
      const botResponse = {
        id: Date.now() + 1,
        text: data.answer || "I don't have an answer for that question.",
        sender: "bot",
        sources: data.sources || [],
        timestamp: new Date()
      };

      setMessages(prevMessages => [...prevMessages, botResponse]);
    } catch (error) {
      // Enhanced error logging for debugging
      console.error("❌ RAG Connection Error:", error);
      console.error("Attempted URL:", 'http://localhost:8000/rag/ask');

      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting to the brain right now. Please try again.",
        sender: "bot",
        sources: [],
        timestamp: new Date()
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={styles.chatContainer}>
      {isOpen && (
        <div className={`${styles.chatWindow} ${!isOpen ? styles.hidden : ''}`}>
          <div className={styles.header}>
            RAG Chat Assistant
          </div>
          <div className={styles.messagesArea}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${message.sender === 'user' ? styles.user : styles.bot}`}
              >
                {message.text}
                {message.sources && message.sources.length > 0 && (
                  <div className={styles.sourcesContainer}>
                    <div className={styles.sourceTitle}>Sources:</div>
                    <ul className={styles.sourceList}>
                      {message.sources.map((source, index) => (
                        <li key={index} className={styles.sourceItem}>
                          [{source.chapter_id}: {source.title}]
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                <div className={styles.srOnly}>
                  {message.sender === 'user' ? 'You said:' : 'Assistant said:'} {message.text}
                  {message.sources && message.sources.length > 0 && ` Sources: ${message.sources.map(s => s.title).join(', ')}`}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className={styles.message}>
                <div className={styles.loadingIndicator}>
                  Thinking<span className={styles.srOnly}>...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className={styles.inputArea}>
            <input
              ref={inputRef}
              type="text"
              className={styles.messageInput}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the textbook..."
              aria-label="Enter your question about the textbook"
              disabled={isLoading}
            />
            <button
              className={styles.sendButton}
              onClick={handleSend}
              disabled={isLoading || inputValue.trim() === ''}
              aria-label="Send message"
            >
              Send
            </button>
          </div>
        </div>
      )}
      <button
        className={styles.toggleButton}
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat assistant" : "Open chat assistant"}
        aria-expanded={isOpen}
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
};

export default ChatWidget;