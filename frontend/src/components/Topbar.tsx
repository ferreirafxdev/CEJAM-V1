import { Link, useLocation } from "react-router-dom";

import { resourceGroups, resources } from "../resources";

type TopbarProps = {
  onMenu: () => void;
};

export default function Topbar({ onMenu }: TopbarProps) {
  const location = useLocation();
  const resource = resources.find((item) => item.path === location.pathname);
  const group = resource
    ? resourceGroups.find((entry) => entry.items.includes(resource.key))
    : null;

  return (
    <header className="topbar">
      <button className="btn btn-ghost topbar__menu" onClick={onMenu}>
        Menu
      </button>
      <div>
        <div className="breadcrumbs">
          <Link to="/">Inicio</Link>
          {group && (
            <>
              <span>/</span>
              <span>{group.label}</span>
            </>
          )}
          {resource && (
            <>
              <span>/</span>
              <strong>{resource.label}</strong>
            </>
          )}
        </div>
        <h2>{resource?.label ?? "Painel CEJAM"}</h2>
        <p>{resource?.description ?? "Gestao juridica e educacional integrada."}</p>
      </div>
      <div className="topbar__accent">
        <span className="topbar__accent-line" />
        <span>ABNT / Juridico</span>
      </div>
    </header>
  );
}
