import { Navigate, Route, Routes } from "react-router-dom";

import { Dashboard } from "./components/Dashboard";
import { navigationSections } from "./data/navigation";
import { resourceByPath, sectionByPath } from "./data/resources";
import { AppShell } from "./layouts/AppShell";
import { LoginPage } from "./pages/LoginPage";
import { PlaceholderPage } from "./pages/PlaceholderPage";
import { ResourcePage } from "./pages/ResourcePage";
import { PagamentoAlunosPage } from "./pages/PagamentoAlunosPage";
import { SectionPage } from "./pages/SectionPage";

const flatNavigation = navigationSections.flatMap((section) => section.items);

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<AppShell />}>
        <Route path="/" element={<Dashboard />} />
        {flatNavigation
          .filter((item) => item.path !== "/")
          .map((item) => {
            if (item.path === "/pagamentos-alunos") {
              return (
                <Route
                  key={item.path}
                  path={item.path}
                  element={<PagamentoAlunosPage />}
                />
              );
            }
            const resourceConfig = resourceByPath[item.path];
            if (resourceConfig) {
              return (
                <Route
                  key={item.path}
                  path={item.path}
                  element={<ResourcePage config={resourceConfig} />}
                />
              );
            }
            const sectionConfig = sectionByPath[item.path];
            if (sectionConfig) {
              return (
                <Route
                  key={item.path}
                  path={item.path}
                  element={<SectionPage config={sectionConfig} />}
                />
              );
            }
            return (
              <Route
                key={item.path}
                path={item.path}
                element={<PlaceholderPage title={item.label} />}
              />
            );
          })}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
