import httpx

from investment_researcher.errors import LLMUnavailable

_DEFAULT_MODEL = "llama3.2:latest"
_DEFAULT_BASE_URL = "http://localhost:11434"
_DEFAULT_TIMEOUT = 180.0


class OllamaClient:
    """LLMClient adapter backed by a local Ollama server's /api/chat endpoint."""

    def __init__(
        self,
        model: str = _DEFAULT_MODEL,
        base_url: str = _DEFAULT_BASE_URL,
        client: httpx.Client | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        self._model = model
        self._base_url = base_url
        self._client = client or httpx.Client(timeout=timeout)

    def complete(self, system: str, user: str) -> str:
        """Return generated text from Ollama's chat endpoint.

        Raises LLMUnavailable on request errors, non-2xx responses, invalid
        JSON, or a body missing message.content. No retry.
        """
        payload = {
            "model": self._model,
            "stream": False,
            "options": {"num_predict": 150},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        try:
            response = self._client.post(f"{self._base_url}/api/chat", json=payload)
        except httpx.RequestError as exc:
            raise LLMUnavailable("request to Ollama failed") from exc

        if not response.is_success:
            raise LLMUnavailable(f"HTTP {response.status_code} from Ollama")

        try:
            body = response.json()
        except ValueError as exc:
            raise LLMUnavailable("invalid JSON from Ollama") from exc

        try:
            return body["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise LLMUnavailable(f"unexpected response shape from Ollama: {body}") from exc
