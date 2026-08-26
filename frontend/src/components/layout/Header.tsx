import { Menu } from "lucide-react";

import logo from "../../images/CIT-logo.webp";

/**
 * Propriedades utilizadas pelo componente Header.
 */
interface HeaderProps {
  /** Função executada quando o usuário solicita a abertura do menu. */
  onMenuClick: () => void;
}

/**
 * Cabeçalho principal da aplicação.
 *
 * Exibe o botão responsável por abrir o menu lateral
 * e as informações básicas do usuário.
 *
 * @param props - Propriedades utilizadas pelo cabeçalho.
 * @returns O cabeçalho principal da aplicação.
 */
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
      <div>
        <img
          src={logo}
          alt="SEDUC Pará"
          className="header__logo"
        />
      </div>  
      <div className="header__title">
        <h1>COORDENADORIA DE INFRAESTRUTURA TECNOLÓGICA</h1>
      </div>

      <div className="header__user">
        Usuário
      </div>
    </header>
  );
}