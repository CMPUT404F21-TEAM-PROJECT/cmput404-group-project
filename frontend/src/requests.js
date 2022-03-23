import axios from "axios";
import { BACKEND_URL } from "./constants";

export default axios.create({
  baseURL: "",
  headers: {
    Authorization: localStorage.getItem('token')
    ? 'JWT ' + localStorage.getItem('access_token') : null,
    'Content-Type': 'application/json',
    accept: 'application/json',
  },
});
