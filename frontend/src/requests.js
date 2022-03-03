import axios from "axios";
import { BACKEND_PORT, BACKEND_URL } from "./constants";

export default axios.create({
  baseURL: `http://${BACKEND_URL}:${BACKEND_PORT}/`,
  headers: {
    Authorization: localStorage.getItem('token')
    ? 'JWT ' + localStorage.getItem('access_token') : null,
    'Content-Type': 'application/json',
    accept: 'application/json',
  },
});