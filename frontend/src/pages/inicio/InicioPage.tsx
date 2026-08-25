import { useEffect, useState } from "react";

import {
  Activity,
  Building2,
  GlobeCheck,
  Network,
} from "lucide-react";

import { StatCard } from "../../components/dashboard/StatCard";
import { DashboardSection } from "../../components/dashboard/DashboardSection";
import { listarDres, type Dre } from "../../services/api";

export function InicioPage() {
  const [dres, setDres] = useState<Dre[]>([]);
  const [carregandoDres, setCarregandoDres] = useState(true);
  const [erroDres, setErroDres] = useState<string | null>(null);

  useEffect(() => {
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
    }

    carregarDres();
  }, []);

  const totalDres = carregandoDres
    ? "—"
    : erroDres
      ? "!"
      : dres.length;
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
          value="—"
          description="Total de DRE cadastradas"
          icon={Building2}
        />

        <StatCard
          title="Escolas"
          value="—"
          description="Escolas por DRE"
          icon={Network}
        />

        <StatCard
          title="Medições"
          value="—"
          description="Escolas com prodepa"
          icon={GlobeCheck}
        />

        <StatCard
          title="Status"
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