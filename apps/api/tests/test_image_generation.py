from pathlib import Path
import base64

import httpx
import pytest

from app.services.image_generation import OpenAICompatibleImageGenerator


@pytest.mark.unit
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


@pytest.mark.unit
def test_image_generator_creates_parent_dirs(tmp_path: Path):
    png_bytes = b"\x89PNG\r\n\x1a\n"
    nested = tmp_path / "deep" / "nested" / "dirs" / "preview.png"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": [{"b64_json": base64.b64encode(png_bytes).decode("ascii")}]})

    generator = OpenAICompatibleImageGenerator(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://api.example.test/v1",
        api_key="sk-test",
        model_name="image-model",
    )

    output = generator.generate(prompt="any", output_path=nested)

    assert output == nested
    assert output.read_bytes() == png_bytes
    assert nested.parent.is_dir()


@pytest.mark.unit
def test_image_generator_strips_trailing_slash():
    captured: dict[str, httpx.Request] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["request"] = request
        return httpx.Response(200, json={"data": [{"b64_json": base64.b64encode(b"x").decode("ascii")}]})

    generator = OpenAICompatibleImageGenerator(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://api.example.test/v1/",
        api_key="sk-test",
        model_name="image-model",
    )

    generator.generate(prompt="any", output_path=Path("/tmp/_unused.png"))

    request = captured["request"]
    assert str(request.url) == "https://api.example.test/v1/images/generations"


@pytest.mark.unit
def test_image_generator_raises_on_http_error(tmp_path: Path):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "boom"})

    generator = OpenAICompatibleImageGenerator(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://api.example.test/v1",
        api_key="sk-test",
        model_name="image-model",
    )

    with pytest.raises(httpx.HTTPStatusError):
        generator.generate(prompt="any", output_path=tmp_path / "preview.png")


@pytest.mark.unit
def test_image_generator_raises_on_empty_data(tmp_path: Path):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": []})

    generator = OpenAICompatibleImageGenerator(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://api.example.test/v1",
        api_key="sk-test",
        model_name="image-model",
    )

    with pytest.raises(IndexError):
        generator.generate(prompt="any", output_path=tmp_path / "preview.png")
