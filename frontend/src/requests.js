import axios from "axios";
import { BACKEND_PORT, BACKEND_URL } from "./constants";

export default axios.create({
  baseURL: `http://${BACKEND_URL}:${BACKEND_PORT}/`,
  params: {},
});