import { Menu } from "lucide-react";

interface HeaderProps {
  onMenuClick: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="header">
      <div className="header__left">
        <button
          type="button"
          className="header__menu"
          onClick={onMenuClick}
          aria-label="Abrir menu"
        >
          <Menu size={24} />
        </button>

      </div>

      <div className="header__user">
        Usuário
      </div>
    </header>
  );
}