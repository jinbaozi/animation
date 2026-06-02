import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AssetsPage } from "../pages/AssetsPage";
import { ModelSettingsPage } from "../pages/ModelSettingsPage";
import { ProjectWorkbenchPage } from "../pages/ProjectWorkbenchPage";
import { VideoPromptPage } from "../pages/VideoPromptPage";

describe("Workbench pages", () => {
  it("renders phase review controls", () => {
    render(<ProjectWorkbenchPage />);
    expect(screen.getByText("Phase 工作台")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "标记通过" })).toBeInTheDocument();
  });

  it("renders asset and prompt pages", () => {
    render(<AssetsPage />);
    expect(screen.getByText("人物资产")).toBeInTheDocument();
    render(<VideoPromptPage />);
    expect(screen.getByText("视频任务包导出")).toBeInTheDocument();
  });

  it("renders encrypted key status", () => {
    render(<ModelSettingsPage />);
    expect(screen.getByText("密钥状态：未解锁")).toBeInTheDocument();
  });
});
