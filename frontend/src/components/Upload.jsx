// components/Upload.jsx
import React from "react";
import { useState } from "react";
import { uploadDocument } from "../services/api";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file");
      return;
    }
    setLoading(true);
    try {
      await uploadDocument(file);
      setMessage("✅ Uploaded successfully!");
      setFile(null);
    } catch (error) {
      setMessage("❌ Upload failed: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: "15px", marginTop: "20px", borderRadius: "5px" }}>
      <h3>Upload Document</h3>
      <input 
        type="file" 
        onChange={(e) => setFile(e.target.files[0])}
        style={{ marginBottom: "10px" }}
      />
      <button 
        onClick={handleUpload} 
        disabled={loading}
        style={{ padding: "8px 15px", cursor: loading ? "not-allowed" : "pointer" }}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
      {message && <p>{message}</p>}
    </div>
  );
}