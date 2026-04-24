// components/AskQuestion.jsx
import React from "react";
import { useState } from "react";
import { askQuestion } from "../services/api";

export default function AskQuestion() {
  const [q, setQ] = useState("");
  const [ans, setAns] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!q.trim()) return;
    setLoading(true);
    try {
      const res = await askQuestion(q);
      setAns(res.data.answer || "No answer received");
    } catch (error) {
      setAns("Error: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: "15px", marginTop: "20px", borderRadius: "5px" }}>
      <h3>Ask Question</h3>
      <input 
        value={q}
        onChange={(e) => setQ(e.target.value)} 
        placeholder="Enter your question..."
        style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
      />
      <button 
        onClick={handleAsk} 
        disabled={loading}
        style={{ padding: "8px 15px", cursor: loading ? "not-allowed" : "pointer" }}
      >
        {loading ? "Loading..." : "Ask"}
      </button>

      {ans && <p><b>Answer:</b> {ans}</p>}
    </div>
  );
}