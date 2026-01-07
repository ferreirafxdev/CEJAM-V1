import { render, screen } from "@testing-library/react";

import { ActivityList } from "./ActivityList";

describe("ActivityList", () => {
  it("shows empty state", () => {
    render(<ActivityList items={[]} />);
    expect(screen.getByText(/Nenhuma atividade recente/i)).toBeInTheDocument();
  });

  it("renders activity items", () => {
    render(
      <ActivityList
        items={[
          {
            type: "aluno",
            message: "Nova matricula: Ana",
            timestamp: "2024-04-01T10:00:00Z",
          },
        ]}
      />
    );

    expect(screen.getByText(/Nova matricula: Ana/i)).toBeInTheDocument();
  });
});
