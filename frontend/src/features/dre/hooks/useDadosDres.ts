import { useEffect, useState } from "react";

import { listarDres } from "../services/dreService";

import type { Dre } from "../types/dre";

/**
 * Responsável por carregar e manter os dados das DREs.
 *
 * Encapsula:
 * - carregamento inicial das DREs;
 * - estado da lista de DREs;
 * - estado de carregamento;
 * - estado de erro.
 *
 * A página utiliza este hook para acessar os dados
 * sem precisar conhecer os detalhes da chamada à API.
 */
export function useDadosDres() {
  const [dres, setDres] = useState<Dre[]>([]);
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

  return {
    dres,
    setDres,
    carregando,
    erro,
    setErro,
  };
}