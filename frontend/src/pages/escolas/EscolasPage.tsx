import {
  useEffect,
  useMemo,
  useState,
} from "react";

import { Pencil } from "lucide-react";

import { useSearchParams } from "react-router-dom";

import {
  listarEscolas,
  type Escola,
} from "../../features/escolas/services/escolaService";

import {
  listarDiretores,
  type Diretor,
} from"../../features/diretor/services/diretorService"

import { EditarEscolaModal } from "../../features/escolas/components/EditarEscolaModal";
import { EditarDiretorModal } from "../../features/diretor/components/EditarDiretorModal";

import { formatarTelefone } from "../../utils/formatar"

import "./escolas.css";

export function EscolasPage() {
  const [searchParams] = useSearchParams();

  const dreIdParam = searchParams.get("dre_id");

  const dreId = dreIdParam
    ? Number(dreIdParam)
    : null;

  const [escolas, setEscolas] = useState<Escola[]>(
    [],
  );

  const [diretores, setDiretores] = useState<Diretor[]>([]);

  const [escolaSelecionada, setEscolaSelecionada] =
    useState<Escola | null>(null);

  const [escolaEmEdicao, setEscolaEmEdicao] =
    useState<Escola | null>(null);

  const [busca, setBusca] = useState("");

  const [carregando, setCarregando] =
    useState(true);

  const [erro, setErro] = useState<string | null>(
    null,
  );

  const [diretorEmEdicao, setDiretorEmEdicao] =
  useState<Diretor | null>(null);

  useEffect(() => {
    async function carregarDados() {
      try {
        setCarregando(true);
        setErro(null);

        const [escolasDados, diretoresDados] =
          await Promise.all([
            listarEscolas(),
            listarDiretores(),
          ]);

        setEscolas(escolasDados);
        setDiretores(diretoresDados);
      } catch (error) {
        console.error(
          "Erro ao carregar dados:",
          error,
        );

        setErro(
          "Não foi possível carregar os dados.",
        );
      } finally {
        setCarregando(false);
      }
    }

    carregarDados();
  }, []);

  const escolasFiltradas = useMemo(() => {
    const termo = busca.toLowerCase().trim();

    return escolas.filter((escola) => {
      const pertenceADre =
        dreId === null ||
        escola.dre_id === dreId;

      const correspondeABusca =
        !termo ||
        escola.nome
          .toLowerCase()
          .includes(termo) ||
        escola.inep.includes(termo) ||
        escola.municipio
          .toLowerCase()
          .includes(termo);

      return (
        pertenceADre &&
        correspondeABusca
      );
    });
  }, [busca, escolas, dreId]);

  const diretorDaEscola = escolaSelecionada
    ? diretores.find(
        (diretor) =>
          diretor.escola_id ===
          escolaSelecionada.id,
      )
    : undefined;

  useEffect(() => {
    if (escolasFiltradas.length === 0) {
      setEscolaSelecionada(null);
      return;
    }

    const escolaSelecionadaAindaVisivel =
      escolaSelecionada !== null &&
      escolasFiltradas.some(
        (escola) =>
          escola.id === escolaSelecionada.id,
      );

    if (!escolaSelecionadaAindaVisivel) {
      setEscolaSelecionada(
        escolasFiltradas[0],
      );
    }
  }, [
    escolasFiltradas,
    escolaSelecionada,
  ]);

  /**
   * Atualiza a escola modificada dentro da lista
   * e também atualiza a escola atualmente selecionada.
   */
  function handleEscolaAtualizada(
    escolaAtualizada: Escola,
  ) {
    setEscolas((escolasAtuais) =>
      escolasAtuais.map((escola) =>
        escola.id === escolaAtualizada.id
          ? escolaAtualizada
          : escola,
      ),
    );

    setEscolaSelecionada(escolaAtualizada);

    setEscolaEmEdicao(null);
  }
  function handleDiretorAtualizado(
    diretorAtualizado: Diretor,
  ) {
    setDiretores((diretoresAtuais) =>
      diretoresAtuais.map((diretor) =>
        diretor.id === diretorAtualizado.id
          ? diretorAtualizado
          : diretor,
      ),
    );

    setDiretorEmEdicao(null);
  }

  return (
    <div className="escolas-page">
      <aside className="escolas-page__list">
        <div className="escolas-page__list-header">
          <div>
            <h1>Escolas</h1>

            <p>
              Base cadastral da rede de ensino
            </p>
          </div>

          <span className="escolas-page__count">
            {escolasFiltradas.length} registros
          </span>
        </div>

        <div className="escolas-page__search">
          <input
            type="text"
            placeholder="Buscar escola, INEP ou município..."
            value={busca}
            onChange={(event) =>
              setBusca(event.target.value)
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
          escolasFiltradas.length === 0 && (
            <div className="escolas-page__message">
              Nenhuma escola encontrada.
            </div>
          )}

        {!carregando &&
          !erro &&
          escolasFiltradas.length > 0 && (
            <div className="escolas-list">
              {escolasFiltradas.map((escola) => (
                <button
                  key={escola.id}
                  type="button"
                  className={`escola-list-item ${
                    escolaSelecionada?.id ===
                    escola.id
                      ? "escola-list-item--active"
                      : ""
                  }`}
                  onClick={() =>
                    setEscolaSelecionada(escola)
                  }
                >
                  <strong>
                    {escola.nome}
                  </strong>

                  <div className="escola-list-item__meta">
                    <span>
                      {escola.inep}
                    </span>

                    <span>
                      {escola.municipio}
                    </span>
                  </div>

                  <span className="escola-list-item__type">
                    {escola.tipo}
                  </span>
                </button>
              ))}
            </div>
          )}
      </aside>

      <main className="escolas-page__details">
        {!escolaSelecionada &&
          !carregando && (
            <div className="escolas-page__empty">
              Selecione uma escola para
              visualizar os detalhes.
            </div>
          )}

        {escolaSelecionada && (
          <>
            <header className="escola-details__header">
              <div>
                <h2>
                  {escolaSelecionada.nome}
                </h2>

                <div className="escola-details__meta">
                  <span>
                    {" "}
                    {escolaSelecionada.dre?.nome}
                  </span>

                  <span>
                    INEP{" "}
                    {escolaSelecionada.inep}
                  </span>

                  <span>
                    {escolaSelecionada.municipio}
                  </span>

                  <span>
                    {escolaSelecionada.tipo}
                  </span>
                </div>
              </div>

              <button
                type="button"
                className="escola-details__edit-button"
                onClick={() =>
                  setEscolaEmEdicao(
                    escolaSelecionada,
                  )
                }
              >
                <Pencil size={16} />
                Editar
              </button>
            </header>

            <section className="escola-details__grid">

              <article className="escola-card">
                <h3>Chromebooks</h3>

                <p>
                  Informações dos dispositivos
                  serão carregadas aqui.
                </p>
              </article>

              <article className="escola-card">
                <h3>Starlink</h3>

                <p>
                  Informações da conectividade
                  serão carregadas aqui.
                </p>
              </article>
            </section>
            
            <section className="escola-details__cadastro">
                 <div className="escola-card__header">
                    <h3>Direção</h3>

                    {diretorDaEscola && (
                      <button
                        type="button"
                        className="escola-card__edit-button"
                        onClick={() =>
                          setDiretorEmEdicao(diretorDaEscola)
                        }
                        aria-label="Editar diretor"
                      >
                        <Pencil size={16} />
                        Editar
                      </button>
                    )}
                  </div>

                {diretorDaEscola ? (
                  <>
                    <p>
                      <strong>
                        {diretorDaEscola.nome}
                      </strong>
                    </p>

                    {diretorDaEscola.telefone && (
                      <p>
                        Tel:{" "}
                        {formatarTelefone(diretorDaEscola.telefone)}
                      </p>
                    )}

                    {diretorDaEscola.email && (
                      <p>
                        E-mail:{" "}
                        {diretorDaEscola.email}
                      </p>
                    )}
                  </>
                ) : (
                  <p>Sem informações</p>
                )}
            </section>
              
            <section className="escola-details__cadastro">
              <h3>
                Localização / Endereço
              </h3>

              <p>
                {escolaSelecionada.endereco ??
                  "Endereço não informado"}
              </p>
            </section>
          </>
        )}
      </main>

      {escolaEmEdicao && (
        <EditarEscolaModal
          escola={escolaEmEdicao}
          onClose={() =>
            setEscolaEmEdicao(null)
          }
          onSuccess={
            handleEscolaAtualizada
          }
        />
      )}
      
      {diretorEmEdicao && (
        <EditarDiretorModal
          diretor={diretorEmEdicao}
          onClose={() =>
            setDiretorEmEdicao(null)
          }
          onSuccess={handleDiretorAtualizado}
        />
      )}
    </div>
  );
}