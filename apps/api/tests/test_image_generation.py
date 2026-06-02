from pathlib import Path
import base64

import httpx

from app.services.image_generation import OpenAICompatibleImageGenerator


def test_image_generator_saves_base64_png(tmp_path: Path):
    png_bytes = b"\x89PNG\r\n\x1a\n"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": [{"b64_json": base64.b64encode(png_bytes).decode("ascii")}]})

    generator = OpenAICompatibleImageGenerator(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://api.example.test/v1",
        api_key="sk-test",
        model_name="image-model",
    )

    output = generator.generate(prompt="角色正面全身", output_path=tmp_path / "preview.png", size="1024x1024")

    assert output.read_bytes() == png_bytes
