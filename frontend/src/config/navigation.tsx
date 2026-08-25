import type { LucideIcon } from "lucide-react";
import { Home, Building2 } from "lucide-react";

export interface NavigationItem {
  label: string;
  path: string;
  icon: LucideIcon;
  end?: boolean;
}

export interface NavigationGroup {
  label?: string;
  items: NavigationItem[];
}

export const navigation: NavigationGroup[] = [
  {
    items: [
      {
        label: "Início",
        path: "/",
        icon: Home,
        end: true,
      },
      {
        label: "DRE",
        path: "/dre",
        icon: Building2,
      },
    ],
  },
];