// components/Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{ 
      backgroundColor: "#333", 
      color: "white", 
      padding: "15px", 
      marginBottom: "20px",
      borderRadius: "5px"
    }}>
      <h2 style={{ margin: "0" }}>📄 Doc AI Platform</h2>
      <Link to="/" style={{ color: "white", textDecoration: "none", marginRight: "15px" }}>Home</Link>
    </nav>
  );
}