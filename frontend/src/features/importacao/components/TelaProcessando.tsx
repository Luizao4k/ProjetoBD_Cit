/**
 * Tela apresentada enquanto uma importação está sendo processada.
 *
 * Este componente possui apenas responsabilidade de apresentação.
 * O processamento da importação é realizado pela página.
 */
export function TelaProcessando() {
  return (
    <div className="importacao-card">
      <div className="importacao-card__header">
        <h2>Processando importação</h2>
        <p>
          Aguarde enquanto os dados estão sendo processados.
        </p>
      </div>

      <div className="importacao-card__body">
        <div className="importacao-loading">
          <div className="importacao-loading__spinner" />

          <p>
            Processando importação...
          </p>
        </div>
      </div>
    </div>
  );
}