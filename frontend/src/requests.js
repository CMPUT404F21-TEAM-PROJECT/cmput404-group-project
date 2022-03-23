import axios from "axios";
import { BACKEND_URL } from "./constants";

// UNCOMMENT THIS URL FOR DEVELOPMENT ON LOCAL
const url = process.env.REACT_APP_BACKEND_URL ? process.env.REACT_APP_BACKEND_URL : `${BACKEND_URL}/`;

// FOR PRODUCTION
// const url = "";

export default axios.create({
  baseURL: "",
  headers: {
    Authorization: localStorage.getItem('token')
    ? 'JWT ' + localStorage.getItem('access_token') : null,
    'Content-Type': 'application/json',
    accept: 'application/json',
  },
});
