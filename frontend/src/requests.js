import axios from "axios";
import { BACKEND_PORT, BACKEND_URL } from "./constants";

// UNCOMMENT THIS URL FOR DEVELOPMENT ON LOCAL
// const url = process.env.REACT_APP_BACKEND_URL ? process.env.REACT_APP_BACKEND_URL : `http://${BACKEND_URL}:${BACKEND_PORT}/`;

// FOR PRODUCTION
const url = "https://deployservertest.herokuapp.com/";

export default axios.create({
  baseURL: url,
  headers: {
    Authorization: localStorage.getItem('token')
    ? 'JWT ' + localStorage.getItem('access_token') : null,
    'Content-Type': 'application/json',
    accept: 'application/json',
  },
});