// pages/Home.jsx
import React from "react";
import Upload from "../components/Upload";
import DocumentList from "../components/DocumentList";
import Search from "../components/Search";
import AskQuestion from "../components/AskQuestion";
import Dashboard from "../components/Dashboard";

export default function Home() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ color: "#333" }}>📄 Document AI Platform</h1>
      <Upload />
      <Dashboard />
      <DocumentList />
      <Search />
      <AskQuestion />
    </div>
  );
}
