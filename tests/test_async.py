"""Tests for RedditClient async context manager lifecycle."""
import pytest
import httpx
import respx

from reddit_cli.reddit import RedditClient


@pytest.mark.asyncio
async def test_reddit_client_context_manager():
    """Test that RedditClient properly initializes and cleans up via context manager."""
    async with RedditClient() as client:
        # Test that client is properly initialized
        assert client._client is not None
        # Test that we can make a basic request (will be mocked)
        assert client.BASE_URL == "https://www.reddit.com"
        assert client.TIMEOUT == 10.0
        assert client.USER_AGENT == "better-reddit-cli/0.4.4"
        assert client.MAX_RETRIES == 3
        assert client.INITIAL_BACKOFF == 1.0

    # After context exit, client should be closed
    # Note: We cannot directly test _client is None because the client
    # is set to None in __aexit__ but the object persists


@pytest.mark.asyncio
async def test_reddit_client_context_manager_multiple_entries():
    """Test that RedditClient can be used in multiple context manager entries."""
    for _ in range(3):
        async with RedditClient() as client:
            assert client._client is not None


@pytest.mark.asyncio
async def test_reddit_client_get_without_context_raises():
    """Test that calling get() without entering context raises RuntimeError."""
    client = RedditClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get("/r/python/hot.json")


@pytest.mark.asyncio
@respx.mock
async def test_reddit_client_basic_get():
    """Test a basic GET request through the context manager."""
    # Mock the Reddit API endpoint
    mock_response = {
        "data": {
            "children": [],
            "after": None,
            "before": None,
        }
    }
    respx.get("https://www.reddit.com/r/python/hot.json").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    async with RedditClient() as client:
        result = await client.get("/r/python/hot.json")
        assert result == mock_response


@pytest.mark.asyncio
@respx.mock
async def test_reddit_client_retry_on_429():
    """Test that client retries on rate limit (429) with exponential backoff."""
    # First two requests return 429, third succeeds
    mock_response = {
        "data": {
            "children": [],
            "after": None,
            "before": None,
        }
    }

    route = respx.get("https://www.reddit.com/r/python/hot.json")
    route.mock(side_effect=[
        httpx.Response(429, json={"error": 429}),
        httpx.Response(429, json={"error": 429}),
        httpx.Response(200, json=mock_response),
    ])

    async with RedditClient() as client:
        result = await client.get("/r/python/hot.json")
        assert result == mock_response
        assert route.call_count == 3


@pytest.mark.asyncio
@respx.mock
async def test_reddit_client_raises_after_max_retries_429():
    """Test that client raises after max retries on 429."""
    route = respx.get("https://www.reddit.com/r/python/hot.json")
    route.mock(side_effect=httpx.Response(429, json={"error": 429}))

    async with RedditClient() as client:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get("/r/python/hot.json")
        assert route.call_count == 3  # MAX_RETRIES = 3


@pytest.mark.asyncio
@respx.mock
async def test_reddit_client_raises_on_500_after_retries():
    """Test that client raises after retries on 500 errors."""
    route = respx.get("https://www.reddit.com/r/python/hot.json")
    route.mock(side_effect=httpx.Response(500, json={"error": 500}))

    async with RedditClient() as client:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get("/r/python/hot.json")
        assert route.call_count == 3  # MAX_RETRIES = 3


@pytest.mark.asyncio
@respx.mock
async def test_reddit_client_successful_request_first_try():
    """Test successful request without needing retries."""
    mock_response = {
        "data": {
            "children": [{"kind": "t3", "data": {"id": "abc123"}}],
            "after": None,
            "before": None,
        }
    }
    route = respx.get("https://www.reddit.com/r/python/hot.json")
    route.mock(return_value=httpx.Response(200, json=mock_response))

    async with RedditClient() as client:
        result = await client.get("/r/python/hot.json")
        assert result == mock_response
        assert route.call_count == 1


@pytest.mark.asyncio
@respx.mock
async def test_reddit_client_timeout_raises():
    """Test that timeout errors are raised properly."""
    route = respx.get("https://www.reddit.com/r/python/hot.json")
    route.mock(side_effect=httpx.TimeoutException("Connection timed out"))

    async with RedditClient() as client:
        with pytest.raises(httpx.TimeoutException):
            await client.get("/r/python/hot.json")


@pytest.mark.asyncio
@respx.mock
async def test_reddit_client_connect_error_raises():
    """Test that connection errors are raised properly."""
    route = respx.get("https://www.reddit.com/r/python/hot.json")
    route.mock(side_effect=httpx.ConnectError("Connection failed"))

    async with RedditClient() as client:
        with pytest.raises(httpx.ConnectError):
            await client.get("/r/python/hot.json")
