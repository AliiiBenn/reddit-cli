import asyncio
import sys
import typer

from reddit_cli.reddit import RedditClient, PostsClient

app = typer.Typer()


async def _post_async(post_id: str) -> None:
    """Async implementation of post."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        post = await posts_client.get_post(post_id)

        print(f"Title: {post.title}")
        print(f"Score: {post.score}")
        print(f"Comments: {post.num_comments}")
        print(f"Author: {post.author}")
        print(f"Subreddit: r/{post.subreddit}")
        print(f"URL: {post.url}")
        print(f"Permalink: https://reddit.com{post.permalink}")
        print()
        if post.selftext:
            print(post.selftext.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))


async def _duplicates_async(post_id: str) -> None:
    """Async implementation of duplicates."""
    async with RedditClient() as client:
        posts_client = PostsClient(client)
        original, crossposts = await posts_client.get_duplicates(post_id)

        print("Original Post:")
        print(f"  [{original.score}] {original.title}")
        print(f"  r/{original.subreddit} by {original.author}")
        print(f"  https://reddit.com{original.permalink}")
        print()

        if crossposts:
            print(f"Crossposts ({len(crossposts)}):")
            for cp in crossposts:
                print(f"  [{cp.score}] {cp.title}")
                print(f"    r/{cp.subreddit} by {cp.author}")
                print(f"    https://reddit.com{cp.permalink}")
                print()
        else:
            print("No crossposts found.")


@app.command(name="post")
def post(
    post_id: str,
    view: bool = False,
    info: bool = False,
    duplicates: bool = False,
) -> None:
    """View a single post by ID.

    Args:
        post_id: Post ID (with or without t3_ prefix)
        view: Show post details (alias for post)
        info: Show detailed post info
        duplicates: Show crossposts/duplicates of the post
    """
    if duplicates:
        asyncio.run(_duplicates_async(post_id))
    else:
        asyncio.run(_post_async(post_id))


if __name__ == "__main__":
    app()
