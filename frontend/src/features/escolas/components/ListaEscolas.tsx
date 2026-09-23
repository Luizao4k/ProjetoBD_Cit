import type { Escola } from "../types/escola"
/**
 * Propriedades utilizadas pelo componente ListaEscolas.
 */

interface ListaEscolaProps {
    /** 
    Escolas que devem ser exibidas na lista.
    */

    escolas : Escola[];

    /**
     * Escola atualmente selecionada pelo usuário.
     *
     * É utilizada para destacar visualmente o item
     * correspondente na lista.
     */
    escolaSelecionada: Escola | null;
    /**
    * Texto atualmente digitado no campo de busca.
    */
    busca: string;
    /**
    * Indica se os dados das escolas ainda estão sendo carregados.
    */
    carregando: boolean;
    /**
    * Mensagem de erro ocorrida durante o carregamento dos dados.
    *
    * Quando não existe erro, o valor é null.
    */
    erro: string | null;
    /**
    * Atualiza o texto utilizado na busca das escolas.
    *
    * A lógica da busca permanece fora deste componente,
    * no hook useBuscaEscolas.
    */
    onBuscaChange: (valor: string) => void;
    /**
    * Informa à página qual escola foi selecionada pelo usuário.
    */
    onSelecionarEscola: (escola: Escola) => void;
}
/**
 * Lista lateral de escolas.
 *
 * Responsável por apresentar:
 * - o título da lista;
 * - a quantidade de registros encontrados;
 * - o campo de busca;
 * - mensagens de carregamento e erro;
 * - a lista de escolas encontradas.
 *
 * Este componente não controla o estado da busca nem
 * realiza chamadas à API. Essas responsabilidades pertencem
 * à página e aos hooks utilizados por ela.
 */
export function ListaEscolas({
  escolas,
  escolaSelecionada,
  busca,
  carregando,
  erro,
  onBuscaChange,
  onSelecionarEscola,
}: ListaEscolaProps){
  return (
    <aside className="escolas-page__list">
      <div className="escolas-page__list-header">
        <div>
          <h1>Escolas</h1>
          <p>Base cadastral da rede de ensino</p>
        </div>

        <span className="escolas-page__count">
          {escolas.length} registros
        </span>
      </div>

      <div className="escolas-page__search">
        <input
          type="text"
          placeholder="Buscar escola, INEP ou município..."
          value={busca}
          onChange={(event) =>
            onBuscaChange(event.target.value)
          }
        />
      </div>

      {carregando && (
        <div className="escolas-page__message">
          Carregando escolas...
        </div>
      )}

      {erro && (
        <div className="escolas-page__message escolas-page__message--error">
          {erro}
        </div>
      )}

      {!carregando &&
        !erro &&
        escolas.length === 0 && (
          <div className="escolas-page__message">
            Nenhuma escola encontrada.
          </div>
        )}

      {!carregando &&
        !erro &&
        escolas.length > 0 && (
          <div className="escolas-list">
            {escolas.map((escola) => (
              <button
                key={escola.id}
                type="button"
                className={`escola-list-item ${
                  escolaSelecionada?.id === escola.id
                    ? "escola-list-item--active"
                    : ""
                }`}
                onClick={() =>
                  onSelecionarEscola(escola)
                }
              >
                <strong>{escola.nome}</strong>

                <div className="escola-list-item__meta">
                  <span>{escola.inep}</span>
                  <span>{escola.municipio}</span>
                </div>

                <span className="escola-list-item__type">
                  {escola.tipo}
                </span>
              </button>
            ))}
          </div>
        )}
    </aside>
  );
}