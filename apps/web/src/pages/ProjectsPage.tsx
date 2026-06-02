import type { Project } from "../types";

type ProjectsPageProps = {
  projects: Project[];
};

export function ProjectsPage({ projects }: ProjectsPageProps) {
  return (
    <main style={{ padding: 24, maxWidth: 1120, margin: "0 auto" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1>AI 漫剧工作台</h1>
          <p>上传小说，按 Phase 生成 VideoPrompt、人物资产卡和场景资产卡。</p>
        </div>
        <button type="button">新建项目</button>
      </header>

      <section style={{ marginTop: 24, display: "grid", gap: 12 }}>
        {projects.map((project) => (
          <article key={project.id} style={{ border: "1px solid #d6dbe4", borderRadius: 8, padding: 16 }}>
            <h2>{project.name}</h2>
            <p>{project.slug}</p>
            <strong>{project.current_phase}</strong>
          </article>
        ))}
      </section>
    </main>
  );
}
