import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Plus } from "lucide-react";

import {
  listarDres,
  type Dre
} from "../../services/dreService";

import "./dre.css";

/**
 * Página responsável pelo gerenciamento das Diretorias Regionais de Ensino.
 *
 * Realiza a consulta das DREs cadastradas através da API e controla
 * os estados de carregamento, erro e ausência de registros para exibição
 * adequada da interface.
 *
 * @returns Página de listagem e gerenciamento das DREs.
 */
export function DrePage() {

  const navigate = useNavigate();

  const [dres, setDres] = useState<Dre[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    /**
     * Carrega as Diretorias Regionais de Ensino utilizando o serviço da API.
     *
     * Atualiza os estados da página conforme o resultado da operação,
     * preenchendo a lista de DREs em caso de sucesso ou registrando
     * uma mensagem de erro caso a consulta falhe.
     *
     * @returns Promessa concluída após o carregamento dos dados.
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

  return (
    <div className="dre-page">
      <header className="dre-page__header">
        <div>
          <h1>DRE</h1>
          <p>
            Gerencie as Diretorias Regionais de Ensino.
          </p>
        </div>

        <button className="dre-page__new-button">
          <Plus size={18} />
          Nova DRE
        </button>
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
                </tr>
              </thead>

              <tbody>
                {dres.map((dre) => (
                  /* click na linha */
                    <tr
                      key={dre.id}
                      className="dre-table__row"
                      onClick={() => navigate(`/escolas?dre_id=${dre.id}`)}
                    >

                    <td>{dre.id}</td>
                    <td>{dre.nome}</td>
                    <td>{dre.telefone ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}