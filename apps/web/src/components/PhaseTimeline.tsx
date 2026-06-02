const phases: string[] = ["G0", "Phase0", "Phase1", "Phase1.5", "Phase2a", "Phase2b", "Audit Gate", "最终交付"];

export function PhaseTimeline(): JSX.Element {
  return (
    <nav aria-label="Phase 导航" style={{ display: "grid", gap: 8 }}>
      {phases.map((phase) => (
        <button key={phase} type="button" style={{ textAlign: "left" }}>
          {phase}
        </button>
      ))}
    </nav>
  );
}
