import { createContext, useContext, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "./useLocalStorage";

export interface AuthContextData {
  token: string;
  login: any;
  logout: any;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider = ({ children }: { children: any }) => {
  const [token, setToken] = useLocalStorage("PROJECT_SKELETON_token", null);
  const navigate = useNavigate();

  const login = (data: string) => {
    setToken(data);
    navigate("/dashboard", { replace: true });
  };

  const logout = () => {
    setToken(null);
    navigate("/", { replace: true });
  };

  const value = useMemo(
    () => ({
      token,
      login,
      logout,
    }),
    [token]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};
