import { Outlet } from "react-router-dom";
import { useState } from 'react';

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

export function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(false);

  function toggleSidebar() {
    setSidebarOpen((current: boolean) => !current);
  }

  function closeSidebar() {
    setSidebarOpen(false);
  }

  return (
    <div className="app-layout">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={closeSidebar}
      />

      <div className="app-layout__main">
        <Header
          onMenuClick={toggleSidebar}
        />

        <main className="app-layout__content">
          <Outlet />
        </main>
      </div>

      {sidebarOpen && (
        <button
          className="sidebar-overlay"
          onClick={closeSidebar}
          aria-label="Fechar menu"
        />
      )}
    </div>
  );
}