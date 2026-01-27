import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// ✅ PATCH: Suppress benign ResizeObserver error to prevent overlay
const resizeObserverLoopErr = 'ResizeObserver loop completed with undelivered notifications';

window.addEventListener('error', (e) => {
  if (e.message === resizeObserverLoopErr || e.message.includes('ResizeObserver')) {
    e.stopImmediatePropagation();
  }
});

const originalError = console.error;
console.error = (...args) => {
  if (args[0] && typeof args[0] === 'string' && args[0].includes('ResizeObserver')) {
    return;
  }
  originalError.call(console, ...args);
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();