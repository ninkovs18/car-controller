import axios from "axios";
import { auth } from "./firebase";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: BASE_URL,
});
api.interceptors.request.use(async (config) => {
  const u = auth.currentUser;
  if (u) {
    const token = await u.getIdToken();
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export { api };
