import { useState } from "react";
import { Outlet } from "react-router-dom";

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

/**
 * Layout principal da aplicação.
 *
 * Responsável por estruturar a interface principal, integrando
 * o cabeçalho, a barra lateral e o conteúdo das rotas.
 *
 * Também controla a abertura e o fechamento da barra lateral
 * e disponibiliza o conteúdo das páginas através do Outlet.
 *
 * @returns O layout principal da aplicação.
 */
export function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(false);

  /**
   * Alterna o estado de abertura da barra lateral.
   */
  function toggleSidebar() {
    setSidebarOpen((current: boolean) => !current);
  }

  /**
   * Fecha a barra lateral.
   */
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