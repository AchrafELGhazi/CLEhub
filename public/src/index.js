// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';  // Importing global styles
import App from './App.jsx';  // Import App.jsx instead of App.js

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')  // This links to the div with id 'root' in index.html
);
