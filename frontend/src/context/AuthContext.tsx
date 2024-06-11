import { createContext, ReactNode, useEffect, useState } from "react";
import { getUserByToken } from "../services/auth-service.ts";
import { getAuthToken, getSessionToken } from "../services/user-service.ts";

type Props = {
  children?: ReactNode;
};

export type User = {
  id: number;
  username: string;
  email: string;
};

type AuthContext = {
  authenticated: boolean;
  user?: User;
  setUser: (user: User | undefined) => void;
};

const fakeUser = {
  id: 2,
  email: "fake@email.com",
  username: "fake_user",
}

const initialValue: AuthContext = {
  authenticated: false,
  user: undefined,
  setUser: () => { },
};

const AuthContext = createContext<AuthContext>(initialValue);

function AuthProvider({ children }: Props) {
  const [user, setUser] = useState<User | undefined>(initialValue.user);

  useEffect(() => {
    const session = getSessionToken();
    const token = getAuthToken();
    if (session && token) {
      getUserByToken(token, session)
        .then((user) => {
          setUser(user);
        })
        .catch(() => {
          // Clear tokens if unable to authenticate
          localStorage.removeItem("token");
          localStorage.removeItem("session");
        });
    }
  }, []);

  const authenticated = user ? true : false;

  return (
    <AuthContext.Provider value={{ authenticated, user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export { AuthContext, AuthProvider };
