import { useMemo, useState } from "react";

import type { Escola } from "../types/escola";

import { normalizarTexto } from "../../../utils/normalizar";

export function useBuscarEscolas(
  escolas: Escola[],
  dreId: number | null,
) {
  const [busca, setBusca] = useState("");

  const escolasFiltradas = useMemo(() => {
    const termo = normalizarTexto(busca);

    return escolas.filter((escola) => {
      const pertenceADre =
        dreId === null ||
        escola.dre_id === dreId;

      const correspondeABusca =
        !termo ||
        normalizarTexto(escola.nome).includes(termo) ||
        normalizarTexto(escola.inep).includes(termo) ||
        normalizarTexto(escola.municipio).includes(termo);

      return pertenceADre && correspondeABusca;
    });
  }, [busca, escolas, dreId]);

  return {
    busca,
    setBusca,
    escolasFiltradas,
  };
}