import axios from "axios";
import { getAuthToken, getSessionToken } from "./user-service";
import { djangoServerPort, ipAddress } from "../config.ts";

const ENDPOINT = "http://" + ipAddress + ":" + djangoServerPort;

const api = axios.create({
  baseURL: ENDPOINT,
  headers: {
    Authorization: `Token ${getAuthToken()}`,
    Session: `Token ${getSessionToken()}`,
  },
});

export default api;
