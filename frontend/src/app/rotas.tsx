import { createBrowserRouter } from "react-router-dom";

import { AppLayout } from "../components/layout/AppLayout";
import { InicioPage } from "../pages/inicio/InicioPage";
import { DrePage } from "../pages/dre/DrePage";

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
    ],
  },
]);