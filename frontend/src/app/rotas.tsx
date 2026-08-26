import { createBrowserRouter } from "react-router-dom";

import { AppLayout } from "../components/layout/AppLayout";

import { InicioPage } from "../pages/inicio/InicioPage";

import { DrePage } from "../pages/dre/DrePage";

import { EscolasPage } from "../pages/escolas/EscolasPage";

/**
 * Configuração principal de rotas da aplicação.
 *
 * Define o layout compartilhado e as páginas disponíveis
 * através do sistema de roteamento do React Router.
 *
 * Rotas:
 * - `/` → Página inicial.
 * - `/dre` → Página de DRE.
 * -`/escolas`→ Página de Escolas
 *
 * O AppLayout funciona como layout raiz e renderiza as
 * páginas filhas através do Outlet.
 */
export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <InicioPage />,
      },
      {
        path: "dre",
        element: <DrePage />,
      },
      {
        path: "escolas",
        element: <EscolasPage />,
      },
    ],
  },
]);