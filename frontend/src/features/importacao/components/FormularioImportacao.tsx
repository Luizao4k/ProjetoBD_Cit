import { useEffect, useState } from "react";

import type { TipoImportacao } from "../types/importacao";
import type { Escola } from "../../escolas/types/escola";

import { listarEscolas } from "../../escolas/services/escolaService";

interface FormularioImportacaoProps {
  tipo: TipoImportacao;
  onImportar: (
    dados: Record<string, string>,
  ) => Promise<void>;
}

type EtapaFormulario =
  | "preenchimento"
  | "confirmacao";

export function FormularioImportacao({
  tipo,
  onImportar,
}: FormularioImportacaoProps) {
  const [escolaId, setEscolaId] = useState("");
  const [buscaEscola, setBuscaEscola] = useState("");
  const [designacao, setDesignacao] = useState("");

  const [escolas, setEscolas] = useState<Escola[]>([]);
  const [carregandoEscolas, setCarregandoEscolas] =
    useState(false);

  const [erro, setErro] = useState<string | null>(
    null,
  );

  const [etapa, setEtapa] =
    useState<EtapaFormulario>("preenchimento");

  useEffect(() => {
    if (tipo !== "starlinks") {
      return;
    }

    async function carregarEscolas() {
      setCarregandoEscolas(true);
      setErro(null);

      try {
        const resposta = await listarEscolas();
        setEscolas(resposta);
      } catch (error) {
        console.error(
          "Erro ao carregar escolas:",
          error,
        );

        setErro(
          error instanceof Error
            ? error.message
            : "Não foi possível carregar as escolas.",
        );
      } finally {
        setCarregandoEscolas(false);
      }
    }

    carregarEscolas();
  }, [tipo]);

  const escolasFiltradas = escolas.filter(
    (escola) => {
      const termo = buscaEscola
        .trim()
        .toLowerCase();

      if (!termo) {
        return false;
      }

      return (
        escola.nome.toLowerCase().includes(termo) ||
        escola.inep.includes(termo)
      );
    },
  );

  const escolaSelecionada = escolas.find(
    (escola) =>
      String(escola.id) === escolaId,
  );

  function handleSelecionarEscola(
    escola: Escola,
  ) {
    setEscolaId(String(escola.id));
    setBuscaEscola(escola.nome);
    setErro(null);
  }

  function handleAlterarEscola() {
    setEscolaId("");
    setBuscaEscola("");
    setErro(null);
  }

  function handleRevisar() {
    if (!escolaId) {
      setErro("Selecione uma escola.");
      return;
    }

    if (!designacao.trim()) {
      setErro("Informe a designação.");
      return;
    }

    setErro(null);
    setEtapa("confirmacao");
  }

  function handleVoltar() {
    setErro(null);
    setEtapa("preenchimento");
  }

  async function handleConfirmar() {
    setErro(null);

    await onImportar({
      escola_id: escolaId,
      designacao: designacao.trim(),
    });
  }

  function obterNomeEscola(): string {
    return (
      escolaSelecionada?.nome ??
      "Escola não encontrada"
    );
  }

  if (tipo !== "starlinks") {
    return (
      <div className="importacao-formulario">
        <p>
          Formulário para este tipo de dado ainda
          não está disponível.
        </p>
      </div>
    );
  }

  if (etapa === "confirmacao") {
    return (
      <div className="importacao-formulario">
        <div className="importacao-formulario__header">
          <h3>Confirmar dados</h3>

          <p>
            Confira as informações antes de salvar
            no banco de dados.
          </p>
        </div>

        <div className="importacao-confirmacao">
          <div className="importacao-confirmacao__campo">
            <span>Escola</span>

            <strong>
              {obterNomeEscola()}
            </strong>

            {escolaSelecionada && (
              <small>
                INEP: {escolaSelecionada.inep}
              </small>
            )}
          </div>

          <div className="importacao-confirmacao__campo">
            <span>Designação</span>

            <strong>
              {designacao.trim()}
            </strong>
          </div>
        </div>

        {erro && (
          <p className="importacao-formulario__erro">
            {erro}
          </p>
        )}

        <div className="importacao-formulario__footer">
          <button
            type="button"
            className="importacao-button importacao-button--secundario"
            onClick={handleVoltar}
          >
            Voltar e editar
          </button>

          <button
            type="button"
            className="importacao-button"
            onClick={handleConfirmar}
          >
            Confirmar e salvar
          </button>
        </div>
      </div>
    );
  }

  return (
    <form
      className="importacao-formulario"
      onSubmit={(evento) => {
        evento.preventDefault();
        handleRevisar();
      }}
    >
      <div className="importacao-formulario__header">
        <h3>Adicionar Starlink</h3>

        <p>
          Preencha os dados para adicionar uma
          Starlink ao sistema.
        </p>
      </div>

      <div className="importacao-formulario__campo">
        <label htmlFor="busca-escola">
          Escola
        </label>

        <input
          id="busca-escola"
          type="text"
          value={buscaEscola}
          onChange={(evento) => {
            setBuscaEscola(
              evento.target.value,
            );
            setEscolaId("");
            setErro(null);
          }}
          placeholder="Pesquise por nome ou INEP"
          disabled={carregandoEscolas}
          autoComplete="off"
        />

        {carregandoEscolas && (
          <p className="importacao-formulario__ajuda">
            Carregando escolas...
          </p>
        )}

        {!carregandoEscolas &&
          buscaEscola.trim() &&
          !escolaSelecionada && (
            <div className="importacao-escolas__resultados">
              {escolasFiltradas.length > 0 ? (
                escolasFiltradas.map((escola) => (
                  <button
                    key={escola.id}
                    type="button"
                    className="importacao-escola__resultado"
                    onClick={() =>
                      handleSelecionarEscola(
                        escola,
                      )
                    }
                  >
                    <strong>
                      {escola.nome}
                    </strong>

                    <span>
                      INEP: {escola.inep}
                    </span>
                  </button>
                ))
              ) : (
                <p className="importacao-formulario__ajuda">
                  Nenhuma escola encontrada.
                </p>
              )}
            </div>
          )}

        {escolaSelecionada && (
          <div className="importacao-escola__selecionada">
            <div>
              <strong>
                {escolaSelecionada.nome}
              </strong>

              <span>
                INEP: {escolaSelecionada.inep}
              </span>
            </div>

            <button
              type="button"
              onClick={handleAlterarEscola}
            >
              Alterar
            </button>
          </div>
        )}
      </div>

      <div className="importacao-formulario__campo">
        <label htmlFor="designacao">
          Designação
        </label>

        <input
          id="designacao"
          type="text"
          value={designacao}
          onChange={(evento) =>
            setDesignacao(
              evento.target.value,
            )
          }
          placeholder="Ex.: STARLINK-001"
          required
        />
      </div>

      {erro && (
        <p className="importacao-formulario__erro">
          {erro}
        </p>
      )}

      <div className="importacao-formulario__footer">
        <button
          type="submit"
          className="importacao-button"
          disabled={
            carregandoEscolas ||
            !escolaId ||
            !designacao.trim()
          }
        >
          Revisar dados
        </button>
      </div>
    </form>
  );
}

