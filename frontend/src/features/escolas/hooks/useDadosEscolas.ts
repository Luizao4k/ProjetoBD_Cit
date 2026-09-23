import { useEffect, useState } from "react";
import { listarEscolas } from "../services/escolaService";
import { listarDiretores } from "../../diretor/services/diretorService";
import { listarStarlinks } from "../../starlink/services/starlinkService";

import type { Escola } from "../types/escola";
import type { Diretor } from "../../diretor/types/diretor";
import type { Starlink } from "../../starlink/types/starlink";

export function useDadosEscolas() {
  const [escolas, setEscolas] = useState<Escola[]>([]);
  const [diretores, setDiretores] = useState<Diretor[]>([]);
  const [starlinks, setStarlinks] = useState<Starlink[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    async function carregarDados() {
      try {
        setCarregando(true);
        setErro(null);

        const [
          escolasDados,
          diretoresDados,
          starlinksDados,
        ] = await Promise.all([
          listarEscolas(),
          listarDiretores(),
          listarStarlinks(),
        ]);

        setEscolas(escolasDados);
        setDiretores(diretoresDados);
        setStarlinks(starlinksDados);
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
        setErro("Não foi possível carregar os dados.");
      } finally {
        setCarregando(false);
      }
    }

    carregarDados();
  }, []);

  return {
    escolas,
    setEscolas,

    diretores,
    setDiretores,

    starlinks,
    setStarlinks,

    carregando,
    erro,
    setErro,
  };
}