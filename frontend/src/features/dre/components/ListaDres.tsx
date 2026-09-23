import { Pencil } from "lucide-react";

import type { Dre } from "../types/dre";

/**
 * Propriedades utilizadas pelo componente ListaDres.
 */
interface ListaDresProps {
  /**
   * DREs que devem ser exibidas na tabela.
   */
  dres: Dre[];

  /**
   * Indica se os dados ainda estão sendo carregados.
   */
  carregando: boolean;

  /**
   * Mensagem de erro ocorrida durante o carregamento.
   *
   * Quando não existe erro, o valor é null.
   */
  erro: string | null;

  /**
   * Informa à página que o usuário selecionou uma DRE.
   */
  onSelecionarDre: (dre: Dre) => void;

  /**
   * Informa à página que o usuário deseja editar uma DRE.
   */
  onEditarDre: (dre: Dre) => void;
}

/**
 * Lista as Diretorias Regionais de Ensino em formato de tabela.
 *
 * Responsabilidades:
 * - apresentar os estados de carregamento e erro;
 * - apresentar a mensagem quando não existem DREs;
 * - renderizar a tabela de DREs;
 * - informar à página quando uma DRE é selecionada;
 * - informar à página quando uma DRE deve ser editada.
 *
 * Este componente não realiza chamadas à API e não controla
 * o estado das DREs.
 */
export function ListaDres({
  dres,
  carregando,
  erro,
  onSelecionarDre,
  onEditarDre,
}: ListaDresProps) {
  /**
   * Trata o clique no botão de edição.
   *
   * Impede que o evento também seja propagado para a linha
   * da tabela, evitando a navegação para a página de escolas.
   */
  function handleEditarDre(
    event: React.MouseEvent<HTMLButtonElement>,
    dre: Dre,
  ) {
    event.stopPropagation();
    onEditarDre(dre);
  }

  if (carregando) {
    return (
      <section className="dre-page__content">
        <div className="dre-page__message">
          Carregando DREs...
        </div>
      </section>
    );
  }

  if (erro) {
    return (
      <section className="dre-page__content">
        <div className="dre-page__message dre-page__message--error">
          {erro}
        </div>
      </section>
    );
  }

  if (dres.length === 0) {
    return (
      <section className="dre-page__content">
        <div className="dre-page__message">
          Nenhuma DRE cadastrada.
        </div>
      </section>
    );
  }

  return (
    <section className="dre-page__content">
      <div className="dre-table-wrapper">
        <table className="dre-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Telefone</th>
              <th>Ações</th>
            </tr>
          </thead>

          <tbody>
            {dres.map((dre) => (
              <tr
                key={dre.id}
                className="dre-table__row"
                onClick={() => onSelecionarDre(dre)}
              >
                <td>{dre.id}</td>

                <td>{dre.nome}</td>

                <td>
                  {dre.telefone ?? "—"}
                </td>

                <td>
                  <button
                    type="button"
                    className="dre-table__edit-button"
                    onClick={(event) =>
                      handleEditarDre(event, dre)
                    }
                    aria-label={`Editar ${dre.nome}`}
                  >
                    <Pencil size={17} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}