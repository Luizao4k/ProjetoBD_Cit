import type { LucideIcon } from "lucide-react";

/**
 * Propriedades utilizadas pelo componente StatCard.
 */
interface StatCardProps {
  /** Título que identifica a estatística apresentada. */
  title: string;

  /** Valor principal da estatística. */
  value: string | number;

  /** Descrição complementar exibida abaixo do valor. */
  description?: string;

  /** Ícone exibido no cabeçalho do cartão. */
  icon: LucideIcon;
}

/**
 * Componente responsável por exibir uma estatística em formato de cartão.
 *
 * Apresenta um título, um valor principal, um ícone e,
 * opcionalmente, uma descrição complementar.
 *
 * @param props - Propriedades utilizadas para configurar o cartão.
 * @returns Um elemento HTML contendo a informação estatística.
 */
export function StatCard({
  title,
  value,
  description,
  icon: Icon,
}: StatCardProps) {
  return (
    <article className="stat-card">
      <div className="stat-card__header">
        <span className="stat-card__title">{title}</span>

        <div className="stat-card__icon">
          <Icon size={20} />
        </div>
      </div>

      <strong className="stat-card__value">
        {value}
      </strong>

      {description && (
        <span className="stat-card__description">
          {description}
        </span>
      )}
    </article>
  );
}