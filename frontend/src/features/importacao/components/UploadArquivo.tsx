import { FileText, Upload, X } from "lucide-react";

interface UploadArquivoProps {
  arquivo: File | null;
  onChange: (arquivo: File | null) => void;
  disabled?: boolean;
}

/**
 * Componente responsável pela seleção do arquivo CSV.
 */
export function UploadArquivo({
  arquivo,
  onChange,
  disabled = false,
}: UploadArquivoProps) {
  function handleArquivoSelecionado(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const arquivoSelecionado = event.target.files?.[0];

    if (!arquivoSelecionado) {
      return;
    }

    onChange(arquivoSelecionado);

    // Permite selecionar novamente o mesmo arquivo depois.
    event.target.value = "";
  }

  function removerArquivo() {
    onChange(null);
  }

  return (
    <div className="importacao-field">
      <label htmlFor="arquivo-importacao">
        Arquivo CSV
      </label>

      {!arquivo ? (
        <label
          htmlFor="arquivo-importacao"
          className={`importacao-upload ${
            disabled ? "importacao-upload--disabled" : ""
          }`}
        >
          <Upload size={28} />

          <span className="importacao-upload__title">
            Selecione um arquivo CSV
          </span>

          <span className="importacao-upload__description">
            Clique para selecionar o arquivo que deseja importar.
          </span>

          <input
            id="arquivo-importacao"
            type="file"
            accept=".csv,text/csv"
            onChange={handleArquivoSelecionado}
            disabled={disabled}
            hidden
          />
        </label>
      ) : (
        <div className="importacao-arquivo">
          <div className="importacao-arquivo__info">
            <FileText size={24} />

            <div>
              <strong>{arquivo.name}</strong>

              <span>
                {(arquivo.size / 1024).toFixed(1)} KB
              </span>
            </div>
          </div>

          <button
            type="button"
            className="importacao-arquivo__remove"
            onClick={removerArquivo}
            disabled={disabled}
            aria-label="Remover arquivo"
            title="Remover arquivo"
          >
            <X size={18} />
          </button>
        </div>
      )}
    </div>
  );
}