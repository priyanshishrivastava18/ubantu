// components/Dashboard.jsx
import React from "react";
import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState({ total_documents: 0, total_queries: 0 });
  const [error, setError] = useState(null);

  useEffect(() => {
    getDashboard()
      .then((res) => setData(res.data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div style={{ border: "1px solid #ddd", padding: "15px", marginTop: "20px", borderRadius: "5px", backgroundColor: "#f9f9f9" }}>
      <h3>Dashboard</h3>
      {error ? (
        <p style={{ color: "red" }}>Error loading dashboard</p>
      ) : (
        <>
          <p>📊 Total Documents: <strong>{data.total_documents}</strong></p>
          <p>🔍 Total Queries: <strong>{data.total_queries}</strong></p>
        </>
      )}
    </div>
  );
}