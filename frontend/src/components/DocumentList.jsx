// components/DocumentList.jsx

import React from "react";
import { useEffect, useState } from "react";
import { getDocuments } from "../services/api";

export default function DocumentList() {
  const [docs, setDocs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getDocuments()
      .then((res) => setDocs(res.data || []))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div style={{ border: "1px solid #ddd", padding: "15px", marginTop: "20px", borderRadius: "5px" }}>
      <h3>Documents</h3>
      {error ? (
        <p style={{ color: "red" }}>Error loading documents</p>
      ) : docs.length === 0 ? (
        <p style={{ color: "#999" }}>No documents uploaded yet</p>
      ) : (
        <ul>
          {docs.map((doc) => (
            <li key={doc.id || doc.filename}>
              {doc.filename}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}