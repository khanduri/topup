import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useOutlet,
} from "react-router-dom";

import LoginPage from "pages/public/login";
import DashboardPage from "pages/protected/dashboard";
import SettingsPage from "pages/protected/settings";
import NoMatchPage from "pages/generic/no_match";

import "./App.css";
import { useAuth, AuthProvider } from "components/hooks/useAuth";
import { GoogleOAuthProvider } from "@react-oauth/google";

const HomeLayout = () => {
  const { token } = useAuth();
  const outlet = useOutlet();

  if (token) {
    return <Navigate to="/" replace />;
  }

  return <div>{outlet}</div>;
};

const ProtectedLayout = () => {
  const { token } = useAuth();
  const outlet = useOutlet();

  if (!token) {
    return <Navigate to="/login" />;
  }

  return <div>{outlet}</div>;
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <GoogleOAuthProvider
          clientId={process.env.REACT_APP_SOCIAL_AUTH_GOOGLE_APP_ID || ""}
        >
          <Routes>
            <Route element={<HomeLayout />}>
              {/* <Route path="/" element={<HomePage />} /> */}
              <Route path="/login" element={<LoginPage />} />
            </Route>

            <Route path="/" element={<ProtectedLayout />}>
              <Route path="" element={<DashboardPage />} />
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="settings" element={<SettingsPage />} />
            </Route>

            {/* <Route
          path="/create"
          render={() => (hasStoredToken() ? <CreatePage /> : <LoginPage />)}
        />
        <Route
          path="/analytics"
          render={() => (hasStoredToken() ? <AnalyticsPage /> : <LoginPage />)}
        />
        <Route
          path="/settings"
          render={() => (hasStoredToken() ? <SettingsPage /> : <LoginPage />)}
        />

        <Route
          path="/support"
          render={() => (hasStoredToken() ? <SupportPage /> : <SupportPage />)}
        /> */}

            {/* <Route
          path="/topbar"
          render={() =>
            hasStoredToken() ? (
              <DashboardTopPage />
            ) : (
              <Redirect to={"/?dest=" + window.location.pathname} />
            )
          }
        />
        <Route
          path="/sidebar"
          render={() =>
            hasStoredToken() ? (
              <DashboardSidePage />
            ) : (
              <Redirect to={"/?dest=" + window.location.pathname} />
            )
          }
        /> */}
            {/* <Route
          path="/"
          element={
            hasStoredToken() ? <DashboardPage /> : <Navigate to="/login" />
          }
        />

        <Route
          path="/login"
          element={hasStoredToken() ? <Navigate to="/" /> : <LoginPage />}
        /> */}

            {/* This has to be at the end of the list */}
            <Route path="*" element={<NoMatchPage />} />
          </Routes>
        </GoogleOAuthProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
