import { User } from "../context/AuthContext";
import api from "./api";
import { getAuthToken, getSessionToken } from "./user-service.ts";

interface AuthResponse {
  token: string;
  user: User;
}

export async function login(username: string, password: string) {
  const res = await api.post<AuthResponse>("/auth/login", {
    username,
    password,
  });
  return res.data;
}

export async function register(username: string, email: string, password: string) {
  const res = await api.post<AuthResponse>("/auth/createUser", {
    username,
    email,
    password,
  });
  return res.data;
}

export async function getUserByToken(token: string, session: string) {
  const res = await api.get<{ user: User }>("/auth/getUserByToken", {
    headers: {
      Authorization: `Token ${token}`,
      Session: `Token ${session}`,
    },
  });
  return res.data.user;
}

export async function requestCode(token: string) {
  const res = await api.post(
    "/auth/send_em",
    {},
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );
  return res.data;
}

export async function sendEmailCode(code: string) {
  const res = await api.post(
    "/auth/verify",
    { code },
    {
      headers: {
        Authorization: `Token ${getAuthToken()}`,
      },
    }
  );
  return res.data;
}

export async function updateMyInfo(data) {
  const res = await api.post("/auth/updateUser", data);
  console.log("Updating user result " + res.data);
  return res.data;
}

export async function createUser(data) {
  const res = await api.post("/auth/createUser", data, {
    headers: {
      Authorization: `Token ${getAuthToken()}`,
      Session: `Token ${getSessionToken()}`,
    },
  });
  return res.data;
}
