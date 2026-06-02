import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ProjectsPage } from "../pages/ProjectsPage";

describe("ProjectsPage", () => {
  it("renders project status and creation action", () => {
    render(
      <ProjectsPage
        projects={[
          { id: 1, name: "Demo Project", slug: "demo-project", current_phase: "phase1", output_dir: "output/demo-project" },
        ]}
      />,
    );

    expect(screen.getByText("Demo Project")).toBeInTheDocument();
    expect(screen.getByText("phase1")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "新建项目" })).toBeInTheDocument();
  });
});
