import httpx


class RedditClient:
    """Async HTTP client for Reddit JSON API."""

    BASE_URL = "https://www.reddit.com"
    TIMEOUT = 10.0  # seconds

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "RedditClient":
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=httpx.Timeout(self.TIMEOUT, connect=5.0)
        )
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._client:
            await self._client.aclose()

    async def get(self, path: str, params: dict | None = None) -> dict:
        """Make a GET request to the Reddit API."""
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")
        response = await self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()
