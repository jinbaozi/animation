export function ModelSettingsPage(): JSX.Element {
  return (
    <main style={{ padding: 24 }}>
      <h1>模型配置</h1>
      <p>密钥状态：未解锁</p>
      <label>
        Base URL
        <input name="base_url" aria-label="Base URL" />
      </label>
      <label>
        Model
        <input name="model" aria-label="Model" />
      </label>
    </main>
  );
}
