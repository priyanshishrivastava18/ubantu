// src/services/api.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://172.24.61.12:5051",
});
export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post("/upload", formData);
};

export const getDocuments = () => API.get("/documents");

export const getSummary = (id) => API.get(`/summary/${id}`);

export const searchDocs = (query) =>
  API.post("/search", { query });

export const askQuestion = (question) =>
  API.post("/ask", { question });

export const getDashboard = () => API.get("/dashboard");