import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../state/auth";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha no login.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login">
      <div className="login__card fade-in">
        <div className="login__brand">
          <span className="pill">CEJAM</span>
          <h1>Sistema de Contratos</h1>
          <p>Gestao juridica educacional com padrao ABNT.</p>
        </div>
        <form className="login__form" onSubmit={handleSubmit}>
          <label>
            Usuario
            <input
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              placeholder="usuario.admin"
              required
            />
          </label>
          <label>
            Senha
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="********"
              required
            />
          </label>
          {error && <div className="alert alert-error">{error}</div>}
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>
      </div>
      <div className="login__aside">
        <div className="login__panel fade-in">
          <h2>Fluxo completo</h2>
          <ul>
            <li>Cadastros, financeiro e contratos em um painel unificado.</li>
            <li>Emissao de PDF juridico com hash e auditoria.</li>
            <li>Controle de permissoes por perfil.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
