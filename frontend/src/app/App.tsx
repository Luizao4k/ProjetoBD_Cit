import { RouterProvider } from "react-router-dom";

import { router } from "./rotas";

/**
 * Componente raiz da aplicação.
 *
 * Responsável por disponibilizar o sistema de rotas da aplicação
 * através do RouterProvider.
 *
 * @returns {JSX.Element} Componente responsável pelo roteamento da aplicação.
 */
function App() {
  return <RouterProvider router={router} />;
}

export default App;