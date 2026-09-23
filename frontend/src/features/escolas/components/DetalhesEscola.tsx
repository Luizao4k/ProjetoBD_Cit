import { Pencil, Trash } from "lucide-react";

import type { Escola } from "../types/escola";
import type { Diretor } from "../../diretor/types/diretor";
import type { Starlink } from "../../starlink/types/starlink";

import { formatarTelefone } from "../../../utils/formatar";

/**
 * Propriedades utilizadas pelo componente DetalhesEscola.
 */
interface DetalhesEscolaProps {
  /**
   * Escola atualmente selecionada pelo usuário.
   *
   * Quando null, significa que nenhuma escola foi selecionada.
   */
  escola: Escola | null;

  /**
   * Diretor vinculado à escola selecionada.
   *
   * Quando undefined, significa que a escola não possui
   * um diretor cadastrado.
   */
  diretor: Diretor | undefined;

  /**
   * Lista de Starlinks vinculadas à escola selecionada.
   */
  starlinks: Starlink[];

  /**
   * Informa à página que o usuário deseja editar a escola.
   *
   * A página é responsável por abrir o modal de edição.
   */
  onEditarEscola: (escola: Escola) => void;

  /**
   * Informa à página que o usuário deseja editar o diretor.
   *
   * A página é responsável por abrir o modal de edição.
   */
  onEditarDiretor: (diretor: Diretor) => void;

  /**
   * Informa à página que o usuário deseja editar uma Starlink.
   *
   * A página é responsável por abrir o modal de edição.
   */
  onEditarStarlink: (starlink: Starlink) => void;

  /**
   * Solicita a exclusão de uma Starlink.
   *
   * A página é responsável por executar a exclusão
   * e atualizar os dados após a operação.
   */
  onExcluirStarlink: (starlink: Starlink) => void;
}

/**
 * Exibe os detalhes da escola atualmente selecionada.
 *
 * Responsabilidades deste componente:
 * - apresentar os dados básicos da escola;
 * - apresentar informações sobre Chromebooks;
 * - apresentar as Starlinks vinculadas;
 * - apresentar informações da direção;
 * - apresentar o endereço da escola;
 * - informar à página quando o usuário solicita alguma ação.
 *
 * Este componente não possui estado próprio relacionado aos dados
 * da escola e não realiza chamadas à API.
 *
 * A página responsável por este componente mantém os estados
 * e executa as operações solicitadas através das funções recebidas
 * pelas props.
 */
export function DetalhesEscola({
  escola,
  diretor,
  starlinks,
  onEditarEscola,
  onEditarDiretor,
  onEditarStarlink,
  onExcluirStarlink,
}: DetalhesEscolaProps) {
  /**
   * Quando nenhuma escola está selecionada, apresenta uma
   * mensagem orientando o usuário a selecionar uma escola.
   */
  if (!escola) {
    return (
      <main className="escolas-page__details">
        <div className="escolas-page__empty">
          Selecione uma escola para visualizar os detalhes.
        </div>
      </main>
    );
  }

  return (
    <main className="escolas-page__details">
      <header className="escola-details__header">
        <div>
          <h2>{escola.nome}</h2>

          <div className="escola-details__meta">
            <span>{escola.dre?.nome}</span>

            <span>
              INEP {escola.inep}
            </span>

            <span>{escola.municipio}</span>

            <span>{escola.tipo}</span>
          </div>
        </div>

        <button
          type="button"
          className="escola-details__edit-button"
          onClick={() => onEditarEscola(escola)}
        >
          <Pencil size={16} />
          Editar
        </button>
      </header>

      <section className="escola-details__grid">
        <article className="escola-card">
          <h3>Chromebooks</h3>

          <p>
            Informações dos dispositivos serão carregadas aqui.
          </p>
        </article>

        <article className="escola-card">
          <div className="escola-card__header">
            <h3>Starlink</h3>
          </div>

          {starlinks.length > 0 ? (
            <div className="escola-card__actions">
              {starlinks.map((starlink) => (
                <div key={starlink.id}>
                  <div className="escola-card__header">
                    <strong>{starlink.designacao}</strong>

                    <button
                      type="button"
                      className="escola-card__edit-button"
                      onClick={() =>
                        onEditarStarlink(starlink)
                      }
                      aria-label="Editar Starlink"
                    >
                      <Pencil size={16} />
                    </button>

                    <button
                      type="button"
                      className="escola-card__delete-button"
                      onClick={() =>
                        onExcluirStarlink(starlink)
                      }
                      aria-label={`Excluir Starlink ${starlink.designacao}`}
                      title="Excluir Starlink"
                    >
                      <Trash size={16} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>Sem informações</p>
          )}
        </article>
      </section>

      <section className="escola-details__cadastro">
        <div className="escola-card__header">
          <h3>Direção</h3>

          {diretor && (
            <button
              type="button"
              className="escola-card__edit-button"
              onClick={() => onEditarDiretor(diretor)}
              aria-label="Editar diretor"
            >
              <Pencil size={16} />
              Editar
            </button>
          )}
        </div>

        {diretor ? (
          <>
            <p>
              <strong>{diretor.nome}</strong>
            </p>

            {diretor.telefone && (
              <p>
                Tel: {formatarTelefone(diretor.telefone)}
              </p>
            )}

            {diretor.email && (
              <p>
                E-mail: {diretor.email}
              </p>
            )}
          </>
        ) : (
          <p>Sem informações</p>
        )}
      </section>

      <section className="escola-details__cadastro">
        <h3>Localização / Endereço</h3>

        <p>
          {escola.endereco ?? "Endereço não informado"}
        </p>
      </section>
    </main>
  );
}