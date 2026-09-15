import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Pencil } from "lucide-react";

import {
  listarDres,
  type Dre,
} from "../../features/dre/services/dreService";

import { EditarDreModal } from "../../features/dre/components/EditarDreModal";

import "./dre.css";

/**
 * Página responsável pelo gerenciamento das Diretorias Regionais de Ensino.
 *
 * Realiza a consulta das DREs cadastradas através da API e controla
 * os estados de carregamento, erro e edição dos registros.
 *
 * @returns Página de listagem e gerenciamento das DREs.
 */
export function DrePage() {
  const navigate = useNavigate();

  const [dres, setDres] = useState<Dre[]>([]);
  const [dreEmEdicao, setDreEmEdicao] = useState<Dre | null>(null);

  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    /**
     * Carrega as DREs através da API.
     */
    async function carregarDres() {
      try {
        setCarregando(true);
        setErro(null);

        const dados = await listarDres();

        setDres(dados);
      } catch (error) {
        console.error("Erro ao carregar DREs:", error);

        setErro("Não foi possível carregar as DREs.");
      } finally {
        setCarregando(false);
      }
    }

    carregarDres();
  }, []);

  /**
   * Atualiza a DRE modificada dentro da lista local.
   *
   * Não é necessário fazer uma nova requisição para listar
   * todas as DREs após uma edição bem-sucedida.
   */
  function handleDreAtualizada(dreAtualizada: Dre) {
    setDres((dresAtuais) =>
      dresAtuais.map((dre) =>
        dre.id === dreAtualizada.id
          ? dreAtualizada
          : dre,
      ),
    );

    setDreEmEdicao(null);
  }

  /**
   * Abre o modal para edição de uma DRE.
   */
  function handleEditarDre(
    event: React.MouseEvent<HTMLButtonElement>,
    dre: Dre,
  ) {
    /*
     * Impede que o clique no botão de edição
     * também execute o clique da linha.
     */
    event.stopPropagation();

    setDreEmEdicao(dre);
  }

  /**
   * Navega para a página de escolas da DRE selecionada.
   */
  function handleSelecionarDre(dre: Dre) {
    navigate(`/escolas?dre_id=${dre.id}`);
  }

  return (
    <div className="dre-page">
      <header className="dre-page__header">
        <div>
          <h1>DRE</h1>

          <p>
            Gerencie as Diretorias Regionais de Ensino.
          </p>
        </div>
      </header>

      <section className="dre-page__content">
        {carregando && (
          <div className="dre-page__message">
            Carregando DREs...
          </div>
        )}

        {erro && (
          <div className="dre-page__message dre-page__message--error">
            {erro}
          </div>
        )}

        {!carregando && !erro && dres.length === 0 && (
          <div className="dre-page__message">
            Nenhuma DRE cadastrada.
          </div>
        )}

        {!carregando && !erro && dres.length > 0 && (
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
                    onClick={() =>
                      handleSelecionarDre(dre)
                    }
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
        )}
      </section>

      {dreEmEdicao && (
        <EditarDreModal
          dre={dreEmEdicao}
          onClose={() => setDreEmEdicao(null)}
          onSuccess={handleDreAtualizada}
        />
      )}
    </div>
  );
}
