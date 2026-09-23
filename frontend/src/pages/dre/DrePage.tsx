import { useState } from "react";

import { useNavigate } from "react-router-dom";

import { EditarDreModal } from "../../features/dre/components/EditarDreModal";
import { ListaDres } from "../../features/dre/components/ListaDres";

import { useDadosDres } from "../../features/dre/hooks/useDadosDres";

import type { Dre } from "../../features/dre/types/dre";

import "./dre.css";

/**
 * Página responsável pelo gerenciamento das Diretorias Regionais de Ensino.
 *
 * Atua como componente orquestrador da tela, sendo responsável por:
 * - coordenar os dados fornecidos pelo hook useDadosDres;
 * - controlar a DRE atualmente em edição;
 * - navegar para a página de escolas da DRE selecionada;
 * - atualizar a lista local após uma edição.
 *
 * A renderização da lista e o carregamento dos dados são
 * delegados para componentes e hooks específicos.
 *
 * @returns Página de listagem e gerenciamento das DREs.
 */
export function DrePage() {
  const navigate = useNavigate();

  /**
   * Dados e estados relacionados às DREs.
   *
   * O carregamento e o controle dos dados são encapsulados
   * pelo hook useDadosDres.
   */
  const {
    dres,
    setDres,
    carregando,
    erro,
  } = useDadosDres();

  /**
   * DRE atualmente selecionada para edição.
   *
   * Quando null, nenhum modal de edição é exibido.
   */
  const [dreEmEdicao, setDreEmEdicao] =
    useState<Dre | null>(null);

  /**
   * Atualiza a DRE modificada dentro da lista local.
   *
   * Não é necessário realizar uma nova requisição para listar
   * todas as DREs após uma edição bem-sucedida.
   *
   * @param dreAtualizada DRE retornada após a edição.
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
   * Navega para a página de escolas filtrada pela DRE selecionada.
   *
   * @param dre DRE selecionada pelo usuário.
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

      <ListaDres
        dres={dres}
        carregando={carregando}
        erro={erro}
        onSelecionarDre={handleSelecionarDre}
        onEditarDre={setDreEmEdicao}
      />

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