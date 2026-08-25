import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon: LucideIcon;
}

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