export function setAuthToken(token: string) {
  console.log("Auth Token Set");
  localStorage.setItem("token", token);
}

export function getAuthToken(): string | null {
  return localStorage.getItem("token");
}

export function setSessionToken(session: string) {
  console.log("Session Token Set");
  localStorage.setItem("session", session);
}

export function getSessionToken(): string | null {
  return localStorage.getItem("session");
}
