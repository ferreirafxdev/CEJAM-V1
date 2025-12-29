import { NavLink } from "react-router-dom";
import clsx from "clsx";

import { resourceGroups, resourceMap } from "../resources";
import { useAuth } from "../state/auth";

type SidebarProps = {
  open: boolean;
  onClose: () => void;
};

export default function Sidebar({ open, onClose }: SidebarProps) {
  const { user, logout } = useAuth();

  return (
    <>
      <div className={clsx("sidebar", open && "sidebar--open")}>
        <div className="sidebar__header">
          <div>
            <h1>CEJAM</h1>
            <p>Contratos Educacionais</p>
          </div>
          <button className="btn btn-ghost sidebar__close" onClick={onClose}>
            Fechar
          </button>
        </div>

        <div className="sidebar__user">
          <div className="badge">
            <span>{user?.username?.toUpperCase() ?? "USUARIO"}</span>
          </div>
          <div className="sidebar__user-info">
            <strong>{user?.first_name || user?.username}</strong>
            <small>{user?.groups?.join(" / ") || "Acesso interno"}</small>
          </div>
        </div>

        <nav className="sidebar__nav">
          <div className="nav-group">
            <div className="nav-group__title">Painel</div>
            <div className="nav-group__links">
              <NavLink
                to="/"
                className={({ isActive }) => clsx("nav-link", isActive && "nav-link--active")}
                onClick={onClose}
              >
                Visao geral
              </NavLink>
            </div>
          </div>
          {resourceGroups.map((group) => (
            <div key={group.label} className="nav-group">
              <div className="nav-group__title">{group.label}</div>
              <div className="nav-group__links">
                {group.items.map((key) => {
                  const resource = resourceMap.get(key);
                  if (!resource) return null;
                  return (
                    <NavLink
                      key={resource.key}
                      to={resource.path}
                      className={({ isActive }) =>
                        clsx("nav-link", isActive && "nav-link--active")
                      }
                      onClick={onClose}
                    >
                      {resource.label}
                    </NavLink>
                  );
                })}
              </div>
            </div>
          ))}
        </nav>

        <div className="sidebar__footer">
          <button className="btn btn-danger" onClick={logout}>
            Sair
          </button>
        </div>
      </div>
      {open && <div className="sidebar__overlay" onClick={onClose} />}
    </>
  );
}
