import type { ResultadoImportacaoApi } from "../services/importacaoService";

/**
 * Propriedades utilizadas pelo componente TelaResultado.
 */
interface TelaResultadoProps {
  /**
   * Resultado retornado pela API após a conclusão da importação.
   */
  resultado: ResultadoImportacaoApi;

  /**
   * Função executada quando o usuário solicita o download das falhas.
   */
  onBaixarFalhas: () => void;
}

/**
 * Apresenta o resultado de uma importação concluída.
 *
 * Responsabilidades:
 * - apresentar o resumo da importação;
 * - apresentar a quantidade de registros processados;
 * - apresentar a quantidade de registros importados com sucesso;
 * - apresentar a quantidade de registros que apresentaram erro;
 * - apresentar a taxa de sucesso;
 * - permitir o download das falhas, quando existirem.
 *
 * Este componente não realiza chamadas à API
 * e não controla o estado da importação.
 */
export function TelaResultado({
  resultado,
  onBaixarFalhas,
}: TelaResultadoProps) {
  return (
    <div className="importacao-card">
      <div className="importacao-card__header">
        <h2>Importação concluída</h2>

        <p>{resultado.resumo}</p>
      </div>

      <div className="importacao-card__body">
        <div className="importacao-resultado">
          <div className="importacao-resultado__item">
            <span>Total processado</span>
            <strong>{resultado.total_processado}</strong>
          </div>

          <div className="importacao-resultado__item">
            <span>Sucessos</span>
            <strong>{resultado.sucessos}</strong>
          </div>

          <div className="importacao-resultado__item">
            <span>Erros</span>
            <strong>{resultado.erros}</strong>
          </div>

          <div className="importacao-resultado__item">
            <span>Taxa de sucesso</span>
            <strong>
              {resultado.taxa_sucesso.toFixed(2)}%
            </strong>
          </div>
        </div>

        {resultado.falhas.length > 0 && (
          <button
            type="button"
            className="importacao-button"
            onClick={onBaixarFalhas}
          >
            Baixar falhas
          </button>
        )}
      </div>
    </div>
  );
}