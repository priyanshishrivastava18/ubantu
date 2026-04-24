// components/Search.jsx
import React from "react";
import { useState } from "react";
import { searchDocs } from "../services/api";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await searchDocs(query);
      setResults(res.data.results || res.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: "15px", marginTop: "20px", borderRadius: "5px" }}>
      <h3>Semantic Search</h3>
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Search documents..."
        style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
      />
      <button 
        onClick={handleSearch} 
        disabled={loading}
        style={{ padding: "8px 15px", cursor: loading ? "not-allowed" : "pointer" }}
      >
        {loading ? "Searching..." : "Search"}
      </button>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {results.length > 0 && (
        <div>
          <h4>Results:</h4>
          {results.map((r, i) => (
            <p key={i} style={{ backgroundColor: "#f5f5f5", padding: "10px", marginTop: "10px", borderRadius: "3px" }}>
              {r.text || JSON.stringify(r)}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}