import type { LucideIcon } from "lucide-react";

import { Home, Building2, School } from "lucide-react";

/**
 * Define a configuração de um item de navegação.
 */
export interface NavigationItem {
  /** Nome exibido para o item de navegação. */
  label: string;

  /** Caminho da rota associada ao item. */
  path: string;

  /** Ícone exibido junto ao nome do item. */
  icon: LucideIcon;

  /**
   * Indica se a rota deve ser considerada ativa somente
   * quando houver correspondência exata com o caminho.
   */
  end?: boolean;
}

/**
 * Define um grupo de itens de navegação.
 *
 * Um grupo pode possuir um título opcional e uma lista
 * de itens relacionados.
 */
export interface NavigationGroup {
  /** Título opcional exibido acima dos itens do grupo. */
  label?: string;

  /** Itens de navegação pertencentes ao grupo. */
  items: NavigationItem[];
}

/**
 * Configuração dos grupos e itens de navegação da aplicação.
 *
 * Essa configuração é utilizada pelo Sidebar para construir
 * dinamicamente o menu lateral.
 */
export const navigation: NavigationGroup[] = [
  {
    items: [
      {
        label: "Início",
        path: "/",
        icon: Home,
        end: true,
      },
      {
        label: "DRE",
        path: "/dre",
        icon: Building2,
      },
      {
        label: "Escolas",
        path: "/escolas",
        icon: School,
      },
    ],
  },
];