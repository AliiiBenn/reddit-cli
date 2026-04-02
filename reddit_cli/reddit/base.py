import asyncio
import httpx


class RedditClient:
    """Async HTTP client for Reddit JSON API."""

    BASE_URL = "https://www.reddit.com"
    TIMEOUT = 10.0  # seconds
    USER_AGENT = "better-reddit-cli/0.4.4"
    MAX_RETRIES = 3
    INITIAL_BACKOFF = 1.0  # seconds

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "RedditClient":
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=httpx.Timeout(self.TIMEOUT, connect=5.0),
            headers={"User-Agent": self.USER_AGENT}
        )
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._client:
            await self._client.aclose()

    async def get(self, path: str, params: dict | None = None) -> dict:
        """Make a GET request to the Reddit API with retry logic.

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            JSON response as dict

        Raises:
            httpx.HTTPStatusError: For non-2xx responses that are not retryable
            httpx.TimeoutException: For timeout errors
            httpx.ConnectError: For connection errors
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")

        last_exception: Exception | None = None
        backoff = self.INITIAL_BACKOFF

        for attempt in range(self.MAX_RETRIES):
            try:
                response = await self._client.get(path, params=params)

                # Retry on rate limiting (429) and server errors (500, 502, 503)
                if response.status_code == 429:
                    if attempt < self.MAX_RETRIES - 1:
                        await asyncio.sleep(backoff)
                        backoff *= 2
                        continue
                    else:
                        last_exception = httpx.HTTPStatusError(
                            "429 Rate Limited",
                            request=response.request,
                            response=response,
                        )
                        raise last_exception

                if response.status_code >= 500:
                    if attempt < self.MAX_RETRIES - 1:
                        await asyncio.sleep(backoff)
                        backoff *= 2
                        continue
                    else:
                        response.raise_for_status()

                response.raise_for_status()
                return response.json()

            except (httpx.TimeoutException, httpx.ConnectError):
                raise
            except httpx.HTTPStatusError:
                raise

        if last_exception:
            raise last_exception
        raise RuntimeError("Max retries exceeded")
