import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || "/api";

export async function getBooks() {
  const response = await axios.get(`${API_BASE}/books/`);
  return response.data;
}

export async function askQuestion(question) {
  const response = await axios.post(`${API_BASE}/ask/`, { question });
  return response.data;
}

export async function getBookSummary(bookId) {
  const response = await axios.get(`${API_BASE}/books/${bookId}/summary/`);
  return response.data;
}

export async function getBookRecommendations(bookId) {
  const response = await axios.get(`${API_BASE}/books/${bookId}/recommendations/`);
  return response.data;
}
