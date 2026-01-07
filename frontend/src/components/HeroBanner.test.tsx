import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import { HeroBanner } from "./HeroBanner";

describe("HeroBanner", () => {
  it("renders CTA and text", () => {
    render(
      <MemoryRouter>
        <HeroBanner
          title="Bem-vindo"
          subtitle="Subtitulo"
          ctaLabel="Ver matriculas"
          ctaHref="/alunos"
        />
      </MemoryRouter>
    );

    expect(screen.getByText(/Bem-vindo/i)).toBeInTheDocument();
    expect(screen.getByText(/Ver matriculas/i)).toBeInTheDocument();
  });
});
