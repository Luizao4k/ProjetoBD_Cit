import { AlertCircle, RotateCcw } from "lucide-react";

/**
 * Propriedades utilizadas pela TelaErro.
 */
interface TelaErroProps {
  /**
   * Mensagem de erro apresentada ao usuário.
   */
  mensagem: string;

  /**
   * Função executada quando o usuário solicita uma nova tentativa.
   */
  onTentarNovamente: () => void;
}

/**
 * Apresenta a tela de erro de uma importação.
 *
 * Responsabilidades:
 * - apresentar a mensagem de erro;
 * - permitir que o usuário tente novamente.
 *
 * Este componente não realiza chamadas à API
 * e não controla o estado da importação.
 */
export function TelaErro({
  mensagem,
  onTentarNovamente,
}: TelaErroProps) {
  return (
    <div className="importacao-card">
      <div className="importacao-card__header">
        <h2>Erro na importação</h2>
        <p>
          Não foi possível concluir a importação.
        </p>
      </div>

      <div className="importacao-card__body">
        <div className="importacao-erro">
          <AlertCircle size={40} />

          <p>{mensagem}</p>

          <button
            type="button"
            className="importacao-button"
            onClick={onTentarNovamente}
          >
            <RotateCcw size={18} />
            Tentar novamente
          </button>
        </div>
      </div>
    </div>
  );
}