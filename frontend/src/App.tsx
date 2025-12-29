import { Navigate, Route, Routes } from "react-router-dom";

import { useAuth } from "./state/auth";
import { resources } from "./resources";
import Dashboard from "./routes/Dashboard";
import Login from "./routes/Login";
import Shell from "./components/Shell";
import ResourcePage from "./components/ResourcePage";

function RequireAuth({ children }: { children: JSX.Element }) {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div className="screen-center">
        <div className="spinner" />
        <p>Carregando...</p>
      </div>
    );
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        element={
          <RequireAuth>
            <Shell />
          </RequireAuth>
        }
      >
        <Route index element={<Dashboard />} />
        {resources.map((resource) => (
          <Route
            key={resource.key}
            path={resource.path}
            element={<ResourcePage resource={resource} />}
          />
        ))}
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
