import {
  useEffect,
  useMemo,
  useState,
} from "react";

import { useSearchParams } from "react-router-dom";

import {
  listarEscolas,
  type Escola,
} from "../../services/escolaService";

import "./escolas.css";

export function EscolasPage() {
  const [searchParams] = useSearchParams();

  const dreIdParam = searchParams.get("dre_id");

  const dreId = dreIdParam
    ? Number(dreIdParam)
    : null;

  const [escolas, setEscolas] = useState<Escola[]>([]);

  const [escolaSelecionada, setEscolaSelecionada] =
    useState<Escola | null>(null);

  const [busca, setBusca] = useState("");

  const [carregando, setCarregando] = useState(true);

  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    async function carregarEscolas() {
      try {
        setCarregando(true);
        setErro(null);

        const dados = await listarEscolas();

        setEscolas(dados);
      } catch (error) {
        console.error(
          "Erro ao carregar escolas:",
          error,
        );

        setErro(
          "Não foi possível carregar as escolas.",
        );
      } finally {
        setCarregando(false);
      }
    }

    carregarEscolas();
  }, []);

  const escolasFiltradas = useMemo(() => {
    const termo = busca.toLowerCase().trim();

    return escolas.filter((escola) => {
      const pertenceADre =
        dreId === null ||
        escola.dre_id === dreId;

      const correspondeABusca =
        !termo ||
        escola.nome.toLowerCase().includes(termo) ||
        escola.inep.includes(termo) ||
        escola.municipio.toLowerCase().includes(termo);

      return pertenceADre && correspondeABusca;
    });
  }, [busca, escolas, dreId]);

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
              {escolasFiltradas.map(
                (escola) => (
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
                ),
              )}
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
              <h2>
                {escolaSelecionada.nome}
              </h2>

              <div className="escola-details__meta">
                <span>
                  INEP {escolaSelecionada.inep}
                </span>

                <span>
                  {escolaSelecionada.municipio}
                </span>

                <span>
                  {escolaSelecionada.tipo}
                </span>
              </div>
            </header>

            <section className="escola-details__grid">
              <article className="escola-card">
                <h3>Direção</h3>

                <p>
                  Informações do diretor serão
                  carregadas aqui.
                </p>
              </article>

              <article className="escola-card">
                <h3>CEMEP</h3>

                <p>
                  Informações do CEMEP serão
                  carregadas aqui.
                </p>
              </article>

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
              <h3>Localização Endereço</h3>

              <p>
                {escolaSelecionada.endereco ??
                  "Endereço não informado"}
              </p>
            </section>
          </>
        )}
      </main>
    </div>
  );
}