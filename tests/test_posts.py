"""Tests for PostsClient."""
import pytest
from reddit_cli.reddit.posts import PostsClient
from reddit_cli.reddit.models import Post

class MockRedditClient:
    def __init__(self, response_data=None):
        self._response_data = response_data
    async def get(self, path, params=None):
        return self._response_data

@pytest.fixture
def sample_post_data():
    return {
        "id": "abc123",
        "title": "Test Post Title",
        "author": "testuser",
        "subreddit": "python",
        "score": 100,
        "num_comments": 42,
        "permalink": "/r/python/comments/abc123/test/",
        "url": "https://example.com",
        "created_utc": 1704067200.0,
        "selftext": "Test content",
    }

@pytest.fixture
def sample_posts_response(sample_post_data):
    return {
        "data": {
            "children": [
                {"kind": "t3", "data": sample_post_data},
                {"kind": "t3", "data": {**sample_post_data, "id": "def456", "title": "Another Post"}},
            ],
            "after": "t3_next",
            "before": "t3_prev",
        }
    }

@pytest.fixture
def empty_posts_response():
    return {"data": {"children": [], "after": None, "before": None}}

@pytest.fixture
def sample_post_response(sample_post_data):
    return {"data": {"children": [{"kind": "t3", "data": sample_post_data}]}}

@pytest.fixture
def sample_duplicates_response(sample_post_data):
    return [
        {"data": {"children": [{"kind": "t3", "data": {**sample_post_data, "id": "original123", "title": "Original Post"}}]}},
        {"data": {"children": [
            {"kind": "t3", "data": {**sample_post_data, "id": "dup123", "title": "Duplicate 1"}},
            {"kind": "t3", "data": {**sample_post_data, "id": "dup456", "title": "Duplicate 2"}},
        ]}}
    ]

class TestListPosts:
    @pytest.mark.asyncio
    async def test_list_posts_default_params(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.list_posts("python")
        assert len(posts) == 2
        assert posts[0].id == "abc123"
        assert after == "t3_next"
        assert before == "t3_prev"

    @pytest.mark.asyncio
    async def test_list_posts_with_sort(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.list_posts("python", sort="new")
        assert len(posts) == 2

    @pytest.mark.asyncio
    async def test_list_posts_with_limit(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.list_posts("python", limit=50)
        assert len(posts) == 2

    @pytest.mark.asyncio
    async def test_list_posts_with_period(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.list_posts("python", sort="top", period="week")
        assert len(posts) == 2

    @pytest.mark.asyncio
    async def test_list_posts_empty_response(self, empty_posts_response):
        mock_client = MockRedditClient(response_data=empty_posts_response)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.list_posts("emptysub")
        assert len(posts) == 0
        assert after is None

    @pytest.mark.asyncio
    async def test_list_posts_returns_post_objects(self, sample_posts_response, sample_post_data):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, _, _ = await posts_client.list_posts("python")
        assert all(isinstance(p, Post) for p in posts)
class TestGetPost:
    @pytest.mark.asyncio
    async def test_get_post_by_id(self, sample_post_response, sample_post_data):
        mock_client = MockRedditClient(response_data=sample_post_response)
        posts_client = PostsClient(mock_client)
        post = await posts_client.get_post("abc123")
        assert isinstance(post, Post)
        assert post.id == sample_post_data["id"]
        assert post.title == sample_post_data["title"]

    @pytest.mark.asyncio
    async def test_get_post_with_t3_prefix(self, sample_post_response, sample_post_data):
        mock_client = MockRedditClient(response_data=sample_post_response)
        posts_client = PostsClient(mock_client)
        post = await posts_client.get_post("t3_abc123")
        assert isinstance(post, Post)
        assert post.id == sample_post_data["id"]

    @pytest.mark.asyncio
    async def test_get_post_extracts_all_fields(self, sample_post_response, sample_post_data):
        mock_client = MockRedditClient(response_data=sample_post_response)
        posts_client = PostsClient(mock_client)
        post = await posts_client.get_post("abc123")
        assert post.author == sample_post_data["author"]
        assert post.subreddit == sample_post_data["subreddit"]
        assert post.score == sample_post_data["score"]
        assert post.num_comments == sample_post_data["num_comments"]
        assert post.permalink == sample_post_data["permalink"]
        assert post.url == sample_post_data["url"]
        assert post.selftext == sample_post_data["selftext"]

class TestGetSticky:
    @pytest.mark.asyncio
    async def test_get_sticky_returns_post(self, sample_post_response, sample_post_data):
        mock_client = MockRedditClient(response_data=sample_post_response)
        posts_client = PostsClient(mock_client)
        post = await posts_client.get_sticky("python")
        assert isinstance(post, Post)
        assert post.id == sample_post_data["id"]

    @pytest.mark.asyncio
    async def test_get_sticky_correct_subreddit(self, sample_post_response):
        mock_client = MockRedditClient(response_data=sample_post_response)
        posts_client = PostsClient(mock_client)
        post = await posts_client.get_sticky("announcements")
        assert isinstance(post, Post)

class TestGetRandom:
    @pytest.mark.asyncio
    async def test_get_random_returns_post(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        post = await posts_client.get_random("python")
        assert isinstance(post, Post)

    @pytest.mark.asyncio
    async def test_get_random_raises_on_empty(self, empty_posts_response):
        mock_client = MockRedditClient(response_data=empty_posts_response)
        posts_client = PostsClient(mock_client)
        with pytest.raises(ValueError, match="No random post found"):
            await posts_client.get_random("empty_sub")
class TestGetDuplicates:
    @pytest.mark.asyncio
    async def test_get_duplicates_with_t3_prefix(self, sample_duplicates_response):
        mock_client = MockRedditClient(response_data=sample_duplicates_response)
        posts_client = PostsClient(mock_client)
        original, duplicates = await posts_client.get_duplicates("t3_original123")
        assert isinstance(original, Post)
        assert original.id == "original123"
        assert len(duplicates) == 2

    @pytest.mark.asyncio
    async def test_get_duplicates_without_prefix(self, sample_duplicates_response):
        mock_client = MockRedditClient(response_data=sample_duplicates_response)
        posts_client = PostsClient(mock_client)
        original, duplicates = await posts_client.get_duplicates("original123")
        assert isinstance(original, Post)
        assert len(duplicates) == 2

    @pytest.mark.asyncio
    async def test_get_duplicates_returns_original_and_crossposts(self, sample_duplicates_response):
        mock_client = MockRedditClient(response_data=sample_duplicates_response)
        posts_client = PostsClient(mock_client)
        original, duplicates = await posts_client.get_duplicates("original123")
        assert original.title == "Original Post"
        assert len(duplicates) == 2
        assert duplicates[0].title == "Duplicate 1"
        assert duplicates[1].title == "Duplicate 2"

    @pytest.mark.asyncio
    async def test_get_duplicates_fallback_format(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        original, duplicates = await posts_client.get_duplicates("abc123")
        assert isinstance(original, Post)
        assert original.id == "abc123"
        assert duplicates == []

    @pytest.mark.asyncio
    async def test_get_duplicates_empty_response(self, empty_posts_response):
        mock_client = MockRedditClient(response_data=empty_posts_response)
        posts_client = PostsClient(mock_client)
        original, duplicates = await posts_client.get_duplicates("notfound")
        assert isinstance(original, Post)
        assert original.id == ""
        assert original.title == ""
        assert duplicates == []
class TestSearchPosts:
    @pytest.mark.asyncio
    async def test_search_posts_basic_query(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.search_posts("python")
        assert len(posts) == 2
        assert all(isinstance(p, Post) for p in posts)

    @pytest.mark.asyncio
    async def test_search_posts_with_subreddit(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, _, _ = await posts_client.search_posts("python", subreddit="learnprogramming")
        assert len(posts) == 2

    @pytest.mark.asyncio
    async def test_search_posts_with_sort(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, _, _ = await posts_client.search_posts("python", sort="new")
        assert len(posts) == 2

    @pytest.mark.asyncio
    async def test_search_posts_with_limit(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, _, _ = await posts_client.search_posts("python", limit=50)
        assert len(posts) == 2

    @pytest.mark.asyncio
    async def test_search_posts_with_period(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, _, _ = await posts_client.search_posts("python", sort="top", period="month")
        assert len(posts) == 2

    @pytest.mark.asyncio
    async def test_search_posts_empty_results(self, empty_posts_response):
        mock_client = MockRedditClient(response_data=empty_posts_response)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.search_posts("nonexistent_query_xyz")
        assert len(posts) == 0
        assert after is None
        assert before is None

    @pytest.mark.asyncio
    async def test_search_posts_returns_post_objects(self, sample_posts_response, sample_post_data):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, _, _ = await posts_client.search_posts("python")
        assert all(isinstance(p, Post) for p in posts)
        assert posts[0].score == sample_post_data["score"]
        assert posts[0].author == sample_post_data["author"]

    @pytest.mark.asyncio
    async def test_search_posts_with_cursors(self, sample_posts_response):
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.search_posts("python")
        assert after == "t3_next"
        assert before == "t3_prev"

class TestPostsClientEdgeCases:
    @pytest.mark.asyncio
    async def test_posts_client_handles_missing_children(self):
        response_data = {"data": {"after": None, "before": None}}
        mock_client = MockRedditClient(response_data=response_data)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.list_posts("python")
        assert posts == []
        assert after is None
        assert before is None

    @pytest.mark.asyncio
    async def test_posts_client_handles_missing_data_key(self):
        response_data = {}
        mock_client = MockRedditClient(response_data=response_data)
        posts_client = PostsClient(mock_client)
        posts, after, before = await posts_client.list_posts("python")
        assert posts == []

    @pytest.mark.asyncio
    async def test_posts_client_handles_malformed_post_data(self, sample_posts_response):
        sample_posts_response["data"]["children"][0]["data"]["extra_field"] = "should be ignored"
        mock_client = MockRedditClient(response_data=sample_posts_response)
        posts_client = PostsClient(mock_client)
        posts, _, _ = await posts_client.list_posts("python")
        assert len(posts) == 2
        assert posts[0].id == "abc123"