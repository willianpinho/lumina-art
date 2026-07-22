from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_generate_rejects_empty_prompt(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")
    response = client.post("/generate", json={"prompt": ""})
    assert response.status_code == 422


def test_generate_rejects_oversized_prompt(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")
    oversized_prompt = "a" * (main.MAX_PROMPT_LENGTH + 1)
    response = client.post("/generate", json={"prompt": oversized_prompt})
    assert response.status_code == 422


def test_generate_returns_data_url_from_mocked_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")

    mock_image = MagicMock()
    mock_image.b64_json = "ZmFrZS1pbWFnZS1ieXRlcw=="
    mock_response = MagicMock()
    mock_response.data = [mock_image]

    with patch("main.OpenAI") as mock_openai_cls:
        mock_client = MagicMock()
        mock_client.images.generate.return_value = mock_response
        mock_openai_cls.return_value = mock_client

        response = client.post("/generate", json={"prompt": "a glowing forest"})

        assert response.status_code == 200
        body = response.json()
        assert body["url"].startswith("data:image/png;base64,")
        mock_client.images.generate.assert_called_once()
