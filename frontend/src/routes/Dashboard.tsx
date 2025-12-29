import { Link } from "react-router-dom";

import { resourceGroups, resourceMap } from "../resources";

export default function Dashboard() {
  return (
    <div className="dashboard">
      <section className="admin-index fade-in">
        <div>
          <h1>Site administration</h1>
          <p>CEJAM - Centro Educacional Jamilza Moreira</p>
        </div>
        <div className="admin-index__note">
          <strong>Atalhos rapidos</strong>
          <p>Escolha um modulo abaixo para gerenciar dados e contratos.</p>
        </div>
      </section>

      <section className="app-list">
        {resourceGroups.map((group, index) => (
          <div key={group.label} className="app-card slide-up" style={{ animationDelay: `${index * 0.08}s` }}>
            <div className="app-card__header">
              <h3>{group.label}</h3>
              <span>{group.items.length} modulos</span>
            </div>
            <div className="app-card__links">
              {group.items.map((key) => {
                const resource = resourceMap.get(key);
                if (!resource) return null;
                return (
                  <Link key={resource.key} to={resource.path} className="link-row">
                    <span>{resource.label}</span>
                    <span className="link-row__arrow">→</span>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
