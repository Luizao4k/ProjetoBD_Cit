import { NavLink } from "react-router-dom";

import logo from "../../images/seduc-pa.webp";

import { navigation } from "../../config/navigation";

/**
 * Propriedades utilizadas pelo componente Sidebar.
 */
interface SidebarProps {
  /** Define se a barra lateral está aberta. */
  isOpen: boolean;

  /** Função executada para fechar a barra lateral. */
  onClose: () => void;
}

/**
 * Barra lateral de navegação da aplicação.
 *
 * Renderiza os grupos e itens de navegação definidos na configuração
 * centralizada de rotas, utilizando o NavLink para identificar
 * automaticamente a página atualmente ativa.
 *
 * A barra lateral pode ser aberta ou fechada através da propriedade
 * isOpen e é fechada após a seleção de um item de navegação.
 *
 * @param props - Propriedades utilizadas para controlar a barra lateral.
 * @returns A barra lateral contendo os itens de navegação da aplicação.
 */
export function Sidebar({
  isOpen,
  onClose,
}: SidebarProps) {
  return (
    <aside
      className={`sidebar ${
        isOpen ? "sidebar--open" : ""
      }`}
    >
      <div className="sidebar__brand">
        <img
          src={logo}
          alt="SEDUC Pará"
          className="sidebar__logo"
        />
      </div>

      <nav className="sidebar__nav">
        {navigation.map((group, groupIndex) => (
          <div
            className="sidebar__group"
            key={group.label ?? groupIndex}
          >
            {group.label && (
              <span className="sidebar__group-label">
                {group.label}
              </span>
            )}

            <div className="sidebar__items">
              {group.items.map((item) => {
                const Icon = item.icon;

                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    end={item.end}
                    onClick={onClose}
                    className={({ isActive }) =>
                      `sidebar__item ${
                        isActive
                          ? "sidebar__item--active"
                          : ""
                      }`
                    }
                  >
                    <Icon size={18} />
                    <span>{item.label}</span>
                  </NavLink>
                );
              })}
            </div>
          </div>
        ))}
      </nav>
    </aside>
  );
}