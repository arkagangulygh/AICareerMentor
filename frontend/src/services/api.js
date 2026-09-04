import axios from "axios";

const api = axios.create({
  baseURL: "https://aicareermentor-1.onrender.com",
});

export default api;