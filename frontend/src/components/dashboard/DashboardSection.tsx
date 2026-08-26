import type { ReactNode } from "react";

/**
 * Propriedades utilizadas pelo componente DashboardSection.
 */
interface DashboardSectionProps {
  /** Título exibido no cabeçalho da seção. */
  title: string;

  /** Descrição opcional exibida abaixo do título. */
  description?: string;

  /** Conteúdo principal que será renderizado dentro da seção. */
  children: ReactNode;
}

/**
 * Componente reutilizável para estruturar seções do dashboard.
 *
 * Exibe um título, uma descrição opcional e o conteúdo
 * fornecido pelos componentes filhos.
 *
 * @param props - Propriedades utilizadas para configurar a seção.
 * @returns Uma seção HTML contendo cabeçalho e conteúdo.
 */
export function DashboardSection({
  title,
  description,
  children,
}: DashboardSectionProps) {
  return (
    <section className="dashboard-section">
      <div className="dashboard-section__header">
        <div>
          <h2>{title}</h2>

          {description && (
            <p>{description}</p>
          )}
        </div>
      </div>

      <div className="dashboard-section__content">
        {children}
      </div>
    </section>
  );
}