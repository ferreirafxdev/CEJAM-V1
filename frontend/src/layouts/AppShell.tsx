import { useState, type ReactNode } from "react";
import { Outlet } from "react-router-dom";

import { Header } from "../components/Header";
import { Sidebar } from "../components/Sidebar";
import { useMe } from "../hooks/useMe";

type AppShellProps = {
  children?: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const { user, status } = useMe();

  const sidebarOffset = collapsed ? "lg:ml-20" : "lg:ml-64";

  return (
    <div className="min-h-screen">
      <Sidebar
        collapsed={collapsed}
        onToggleCollapse={() => setCollapsed((prev) => !prev)}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />
      <div className={`min-h-screen transition-all ${sidebarOffset}`}>
        <Header
          user={user}
          status={status}
          onOpenSidebar={() => setMobileOpen(true)}
        />
        <main className="px-6 pb-10 pt-6 sm:px-8">
          {children ?? <Outlet />}
        </main>
      </div>
    </div>
  );
}
