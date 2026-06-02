from pathlib import Path
import base64

import httpx


class OpenAICompatibleImageGenerator:
    def __init__(self, client: httpx.Client, base_url: str, api_key: str, model_name: str):
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str, output_path: Path, size: str = "1024x1024") -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        response = self.client.post(
            f"{self.base_url}/images/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model_name, "prompt": prompt, "size": size, "response_format": "b64_json"},
            timeout=180,
        )
        response.raise_for_status()
        image_data = response.json()["data"][0]["b64_json"]
        output_path.write_bytes(base64.b64decode(image_data))
        return output_path
