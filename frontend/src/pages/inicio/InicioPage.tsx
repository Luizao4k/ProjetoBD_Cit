import { useEffect, useState } from "react";

import {
  Activity,
  Building2,
  BookAlert,
  Network,
} from "lucide-react";

import { StatCard } from "../../components/dashboard/StatCard";
import { DashboardSection } from "../../components/dashboard/DashboardSection";
import { listarDres, type Dre } from "../../features/dre/services/dreService";
import { listarEscolas, type Escola } from "../../features/escolas/services/escolaService";

/**
 * Página inicial do sistema.
 *
 * Apresenta uma visão geral da conectividade das escolas através
 * de indicadores e seções do dashboard.
 *
 * Atualmente realiza o carregamento das Diretorias Regionais de
 * Ensino para apresentar a quantidade total de DREs cadastradas.
 *
 * @returns Página inicial contendo os indicadores do dashboard.
 */
export function InicioPage() {
  const [dres, setDres] = useState<Dre[]>([]);
  const [carregandoDres, setCarregandoDres] = useState(true);
  const [erroDres, setErroDres] = useState<string | null>(null);

  const [escolas, setEscolas] = useState<Escola[]>([]);
  const [carregandoEscolas, setCarregandoEscolas] = useState(true);
  const [erroEscolas, setErroEscolas] = useState<string | null>(null);

  useEffect(() => {
    /**
     * Carrega as Diretorias Regionais de Ensino através da API.
     *
     * Controla os estados de carregamento e erro e armazena
     * os dados retornados pela API no estado da página.
     */
    async function carregarDres() {
      try {
        setCarregandoDres(true);
        setErroDres(null);

        const dados = await listarDres();

        setDres(dados);
      } catch (error) {
        console.error("Erro ao carregar DREs:", error);
        setErroDres("Não foi possível carregar as DREs.");
      } finally {
        setCarregandoDres(false);
      }

      try {
        setCarregandoEscolas(true);
        setErroEscolas(null);

        const dadosEscola = await listarEscolas();

        setEscolas(dadosEscola);
      } catch (error) {
        console.error("Erro ao carregar escolas:", error);
        setErroEscolas("Não foi possível carregar as Escolas.");
      } finally {
        setCarregandoEscolas(false);
      }
    }

    carregarDres();
  }, []);

  /**
   * Define o valor exibido para o total de DREs conforme
   * o estado atual do carregamento.
   *
   * Durante o carregamento, exibe um marcador de espera.
   * Em caso de erro, exibe um marcador de erro.
   * Caso contrário, exibe a quantidade de DREs cadastradas.
   */
  const totalDres = carregandoDres
    ? "—"
    : erroDres
      ? "!"
      : dres.length;

  const totalEscolas = carregandoEscolas
    ? "—"
    : erroEscolas
      ? "!"
      : escolas.length;


  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <div>
          <h1>Início</h1>

          <p>
            Visão geral da conectividade das escolas.
          </p>
        </div>
      </header>

      <section className="dashboard__stats">
        <StatCard
          title="DRE"
          value={totalDres}
          description="Total de DRE's cadastradas"
          icon={Building2}
        />

        <StatCard
          title="Ativas"
          value={totalEscolas}
          description="Total de Escolas em funcionamento"
          icon={Network}
        />

        <StatCard
          title="Paralizadas"
          value="—"
          description="Escolas paralizadas"
          icon={BookAlert}
        />

        <StatCard
          title="Starlink"
          value="—"
          description="Situação geral da rede"
          icon={Activity}
        />
      </section>

      <DashboardSection
        title="Visão geral"
        description="Indicadores de conectividade das escolas."
      >
        <div className="dashboard__placeholder">
          <p>
            Os indicadores e gráficos serão conectados
            aos dados reais nesta etapa.
          </p>
        </div>
      </DashboardSection>
    </div>
  );
}