import {
  AlertCircle,
  CheckCircle2,
  Download,
  RotateCcw,
} from "lucide-react";

interface ResultadoImportacaoProps {
  sucessos: number;
  erros: number;
  taxaSucesso: number;
  resumo?: string;
  onBaixarFalhas?: () => void;
  onNovaImportacao: () => void;
}

/**
 * Exibe o resultado de uma importação.
 */
export function ResultadoImportacao({
  sucessos,
  erros,
  taxaSucesso,
  resumo,
  onBaixarFalhas,
  onNovaImportacao,
}: ResultadoImportacaoProps) {
  const possuiErros = erros > 0;

  return (
    <section className="resultado-importacao">
      <header className="resultado-importacao__header">
        <div className="resultado-importacao__icon">
          <CheckCircle2 size={28} />
        </div>

        <div>
          <h2>Importação concluída</h2>

          <p>
            O processamento do arquivo foi finalizado.
          </p>
        </div>
      </header>

      <div className="resultado-importacao__stats">
        <article className="resultado-importacao__stat">
          <CheckCircle2 size={20} />

          <div>
            <span>Sucessos</span>
            <strong>{sucessos}</strong>
          </div>
        </article>

        <article className="resultado-importacao__stat">
          <AlertCircle size={20} />

          <div>
            <span>Erros</span>
            <strong>{erros}</strong>
          </div>
        </article>

        <article className="resultado-importacao__stat">
          <div className="resultado-importacao__stat-percent">
            %
          </div>

          <div>
            <span>Taxa de sucesso</span>
            <strong>{taxaSucesso.toFixed(1)}%</strong>
          </div>
        </article>
      </div>

      {resumo && (
        <div className="resultado-importacao__resumo">
          <h3>Resumo</h3>
          <p>{resumo}</p>
        </div>
      )}

      {possuiErros && onBaixarFalhas && (
        <div className="resultado-importacao__falhas">
          <div>
            <h3>Existem registros com erro</h3>

            <p>
              Você pode baixar o arquivo com os registros que
              não foram importados, corrigir os dados e realizar
              uma nova importação.
            </p>
          </div>

          <button
            type="button"
            className="resultado-importacao__download"
            onClick={onBaixarFalhas}
          >
            <Download size={17} />
            Baixar CSV de falhas
          </button>
        </div>
      )}

      <footer className="resultado-importacao__footer">
        <button
          type="button"
          className="resultado-importacao__new"
          onClick={onNovaImportacao}
        >
          <RotateCcw size={17} />
          Nova importação
        </button>
      </footer>
    </section>
  );
}