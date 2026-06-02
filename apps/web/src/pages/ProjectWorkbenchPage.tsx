import { PhaseTimeline } from "../components/PhaseTimeline";

export function ProjectWorkbenchPage(): JSX.Element {
  return (
    <main style={{ display: "grid", gridTemplateColumns: "220px 1fr 240px", gap: 20, padding: 24 }}>
      <PhaseTimeline />
      <section>
        <h1>Phase 工作台</h1>
        <h2>当前输出</h2>
        <pre>等待生成或选择 Phase。</pre>
      </section>
      <aside style={{ display: "grid", gap: 8, alignContent: "start" }}>
        <button type="button">继续生成</button>
        <button type="button">重新生成</button>
        <button type="button">标记通过</button>
        <button type="button">返工到上游</button>
      </aside>
    </main>
  );
}
