// src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = document.getElementById("root");
if (!root) {
  document.body.innerHTML = "<h1>ERROR: Root element not found</h1>";
} else {
  try {
    ReactDOM.createRoot(root).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  } catch (error) {
    document.body.innerHTML = `<h1>React Error</h1><p>${error.message}</p><pre>${error.stack}</pre>`;
  }
}