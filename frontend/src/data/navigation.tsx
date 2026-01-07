import {
  Banknote,
  BookOpen,
  CheckCircle,
  ClipboardList,
  FileCheck,
  FileText,
  GraduationCap,
  KeyRound,
  LayoutDashboard,
  Receipt,
  School,
  Shield,
  User,
  UserCheck,
  UserCog,
  Users,
  UsersRound,
  Wallet,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export type NavItem = {
  label: string;
  path: string;
  icon: LucideIcon;
};

export type NavSection = {
  label: string;
  items: NavItem[];
};

export const navigationSections: NavSection[] = [
  {
    label: "Geral",
    items: [
      { label: "Dashboard", path: "/", icon: LayoutDashboard },
      { label: "Cadastros", path: "/cadastros", icon: ClipboardList },
    ],
  },
  {
    label: "Academico",
    items: [
      { label: "Escolas", path: "/escolas", icon: School },
      { label: "Responsaveis", path: "/responsaveis", icon: UserCheck },
      { label: "Alunos", path: "/alunos", icon: GraduationCap },
      { label: "Professores", path: "/professores", icon: User },
      { label: "Turmas", path: "/turmas", icon: UsersRound },
    ],
  },
  {
    label: "Financeiro",
    items: [
      { label: "Financeiro", path: "/financeiro", icon: Wallet },
      { label: "Planos", path: "/planos", icon: ClipboardList },
      { label: "Pagamentos alunos", path: "/pagamentos-alunos", icon: Banknote },
      { label: "Pagamentos professores", path: "/pagamentos-professores", icon: Wallet },
      { label: "Despesas", path: "/despesas", icon: Receipt },
    ],
  },
  {
    label: "Documentos",
    items: [
      { label: "Documentos", path: "/documentos", icon: FileText },
      {
        label: "Templates de Contrato",
        path: "/templates-contrato",
        icon: BookOpen,
      },
      { label: "Contratos", path: "/contratos", icon: FileCheck },
      { label: "Assinaturas", path: "/assinaturas", icon: CheckCircle },
    ],
  },
  {
    label: "Seguranca",
    items: [
      { label: "Seguranca", path: "/seguranca", icon: Shield },
      { label: "Permissoes", path: "/permissoes", icon: KeyRound },
      { label: "Grupos", path: "/grupos", icon: Users },
      { label: "Usuarios", path: "/usuarios", icon: UserCog },
    ],
  },
];
