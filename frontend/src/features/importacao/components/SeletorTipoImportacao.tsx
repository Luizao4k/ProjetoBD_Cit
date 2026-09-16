import type { TipoImportacao } from "../types/importacao";
import { OPCOES_IMPORTACAO } from "../types/opcoesImportacao";

interface SeletorTipoImportacaoProps {
  valor: TipoImportacao;
  onChange: (tipo: TipoImportacao) => void;
}

/**
 * Permite selecionar o tipo de dado que será importado.
 */
export function SeletorTipoImportacao({
  valor,
  onChange,
}: SeletorTipoImportacaoProps) {
  return (
    <div className="importacao-field">
      <label htmlFor="tipo-importacao">
        Tipo de importação
      </label>

      <select
        id="tipo-importacao"
        value={valor}
        onChange={(event) =>
          onChange(event.target.value as TipoImportacao)
        }
      >
        {OPCOES_IMPORTACAO.map((opcao) => (
          <option key={opcao.tipo} value={opcao.tipo}>
            {opcao.nome}
          </option>
        ))}
      </select>
    </div>
  );
}