import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { useDadosEscolas } from "../../features/escolas/hooks/useDadosEscolas";
import { useBuscarEscolas } from "../../features/escolas/hooks/useBuscarEscolas";

import { EditarEscolaModal } from "../../features/escolas/components/EditarEscolaModal";
import { EditarDiretorModal } from "../../features/diretor/components/EditarDiretorModal";
import { EditarStarlinkModal } from "../../features/starlink/components/EditarStarlinkModal";

import { ListaEscolas } from "../../features/escolas/components/ListaEscolas"
import { DetalhesEscola } from "../../features/escolas/components/DetalhesEscola";


import type { Escola } from "../../features/escolas/types/escola";
import type { Diretor } from "../../features/diretor/types/diretor";
import type { Starlink } from "../../features/starlink/types/starlink";

import { excluirStarlink } from "../../features/starlink/services/starlinkService";

import "./escolas.css";

/**
 * Página responsável pela consulta e gerenciamento das escolas.
 *
 * Funcionalidades:
 * - Carregamento de escolas, diretores e Starlinks.
 * - Busca e filtro por texto e DRE.
 * - Seleção da escola atual.
 * - Exibição dos detalhes da escola.
 * - Abertura dos modais de edição.
 * - Exclusão de registros de Starlink.
 *
 * Atua como componente orquestrador da tela,
 * delegando a renderização para componentes menores.
 */
export function EscolasPage() {

  /**
   * Obtém o identificador da DRE pela URL.
   *
   * Exemplo:
   * /escolas?dre_id=3
   */
  const [searchParams] = useSearchParams();
  const dreIdParam = searchParams.get("dre_id");
  const dreId = dreIdParam ? Number(dreIdParam) : null;

  /**
   * Carrega e gerencia os dados necessários da página.
   *
   * Disponibiliza:
   * - listas de entidades
   * - estados de carregamento
   * - mensagens de erro
   * - funções de atualização local
   */
  const {
    escolas,
    diretores,
    starlinks,
    setEscolas,
    setDiretores,
    setStarlinks,
    carregando,
    erro,
    setErro,
  } = useDadosEscolas();

  /**
   * Gerencia a busca textual e o filtro por DRE.
   */
  const {
    busca,
    setBusca,
    escolasFiltradas,
  } = useBuscarEscolas(escolas, dreId);

  /**
   * Escola atualmente selecionada na lista.
   */
  const [escolaSelecionada, setEscolaSelecionada] =
    useState<Escola | null>(null);

  /**
   * Escola em edição.
   */
  const [escolaEmEdicao, setEscolaEmEdicao] =
    useState<Escola | null>(null);

  /**
   * Diretor em edição.
   */
  const [diretorEmEdicao, setDiretorEmEdicao] =
    useState<Diretor | null>(null);

  /**
   * Starlink em edição.
   */
  const [starlinkEmEdicao, setStarlinkEmEdicao] =
    useState<Starlink | null>(null);

  /**
   * Diretor vinculado à escola selecionada.
   */ 
  const diretorDaEscola = escolaSelecionada
    ? diretores.find(
        (diretor) =>
          diretor.escola_id ===
          escolaSelecionada.id,
      )
    : undefined;
      
  /**
   * Lista de Starlinks vinculadas à escola selecionada.
   */
  const starlinksDaEscola = escolaSelecionada
    ? starlinks.filter(
      (starlink) => starlink.escola_id === escolaSelecionada?.id,
      )
    : [];

  /**
   * Mantém uma escola válida selecionada.
   *
   * Regras:
   * - Se não houver escolas, remove a seleção.
   * - Se a escola atual desaparecer do filtro,
   *   seleciona automaticamente a primeira escola.
  */
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
   * Atualiza a escola modificada dentro da lista,
   * atualiza a seleção atual e fecha o modal.
   *
   * @param escolaAtualizada Escola retornada após a edição.
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

  /**
   * Atualiza o diretor modificado na lista
   * e fecha o modal de edição.
   *
   * @param diretorAtualizado Diretor atualizado.
   */
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

  /**
   * Atualiza a Starlink modificada na lista
   * e fecha o modal de edição.
   *
   * @param starlinkAtualizado Starlink atualizada.
   */
  function handleStarlinkAtualizado(
    starlinkAtualizado: Starlink,
  ) {
    setStarlinks((starlinksAtuais) =>
      starlinksAtuais.map((starlink) =>
        starlink.id === starlinkAtualizado.id
          ? starlinkAtualizado
          : starlink,
      ),
    );

    setStarlinkEmEdicao(null);
  }

  /**
   * Solicita confirmação ao usuário e exclui
   * uma Starlink.
   *
   * Em caso de sucesso:
   * - remove a Starlink da lista local.
   *
   * Em caso de erro:
   * - registra o erro no console;
   * - apresenta mensagem ao usuário.
   *
   * @param starlink Starlink que será removida.
   */
  async function handleExcluirStarlink(
    starlink: Starlink,
  ) {
    const confirmar = window.confirm(
      `Deseja excluir a Starlink "${starlink.designacao}"?`,
    );

    if (!confirmar) {
      return;
    }

    try {
      await excluirStarlink(starlink.id);

      setStarlinks((starlinksAtuais) =>
        starlinksAtuais.filter(
          (item) => item.id !== starlink.id,
        ),
      );
    } catch (error) {
      console.error("Erro ao excluir Starlink:", error);

      setErro("Não foi possível excluir a Starlink.");
    }
  }

  /**
   * Estrutura da página:
   *
   * - Lista lateral de escolas.
   * - Painel de detalhes da escola.
   * - Modais de edição.
   */
  return (
    <div className="escolas-page">
      <ListaEscolas
        escolas={escolasFiltradas}
        escolaSelecionada={escolaSelecionada}
        busca={busca}
        carregando={carregando}
        erro={erro}
        onBuscaChange={setBusca}
        onSelecionarEscola={setEscolaSelecionada}
      />

      <DetalhesEscola
        escola={escolaSelecionada}
        diretor={diretorDaEscola}
        starlinks={starlinksDaEscola}
        onEditarEscola={setEscolaEmEdicao}
        onEditarDiretor={setDiretorEmEdicao}
        onEditarStarlink={setStarlinkEmEdicao}
        onExcluirStarlink={handleExcluirStarlink}
      />


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

      {starlinkEmEdicao && (
        <EditarStarlinkModal
          starlink={starlinkEmEdicao}
          onClose={() => setStarlinkEmEdicao(null)}
          onSuccess={handleStarlinkAtualizado}
        />
      )}
    </div>
  );
}