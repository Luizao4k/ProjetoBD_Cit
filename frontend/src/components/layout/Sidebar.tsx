import { NavLink } from "react-router-dom";
import { navigation } from "../../config/navigation";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

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
        <strong>CIT - SEDUC</strong>
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