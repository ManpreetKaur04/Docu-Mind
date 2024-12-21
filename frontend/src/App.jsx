// src/App.jsx
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <ChatInterface />
      </div>
    </Router>
  );
}

export default App;