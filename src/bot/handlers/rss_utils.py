"""Pure helpers for the /rss commands (no Telegram or qBittorrent calls, easy to test)."""
from typing import Optional
from urllib.parse import urlparse

MAX_NAME_LEN = 80


def feed_host(url: str) -> str:
    """Return only the host of a feed URL. Feed URLs often embed passkeys, so never show the full URL."""
    try:
        return urlparse(url).netloc or "?"
    except ValueError:
        return "?"


def is_valid_feed_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def is_valid_name(name: str) -> bool:
    """Names are used as qBittorrent item paths, so keep them simple."""
    return bool(name) and len(name) <= MAX_NAME_LEN and not any(c in name for c in '\\/|\n\r\t')


def parse_add_feed_args(args: Optional[str]):
    """'/rss_addfeed <name> <url>' -> (name, url) or None."""
    if not args:
        return None
    parts = args.strip().split(None, 1)
    if len(parts) != 2:
        return None
    name, url = parts[0].strip(), parts[1].strip()
    if not is_valid_name(name) or not is_valid_feed_url(url):
        return None
    return name, url


def parse_add_rule_args(args: Optional[str]):
    """
    '/rss_addrule name | feed | must contain | [must not contain] | [category]'
    -> dict(name, feed, must_contain, must_not_contain, category) or None.
    """
    if not args:
        return None
    parts = [p.strip() for p in args.split("|")]
    if len(parts) < 3 or len(parts) > 5:
        return None
    parts += [""] * (5 - len(parts))
    name, feed, must_contain, must_not_contain, category = parts
    if not is_valid_name(name) or not feed or not must_contain:
        return None
    return {
        "name": name,
        "feed": feed,
        "must_contain": must_contain,
        "must_not_contain": must_not_contain,
        "category": category,
    }


def build_rule_def(feed_urls: list, must_contain: str, must_not_contain: str = "", category: str = "") -> dict:
    return {
        "enabled": True,
        "mustContain": must_contain,
        "mustNotContain": must_not_contain,
        "useRegex": False,
        "affectedFeeds": feed_urls,
        "assignedCategory": category,
        "addPaused": None,
    }


def resolve_feed_urls(feed: str, feeds: dict):
    """
    feed: a feed name, or 'all' / '*' for every feed.
    feeds: {name: url}. Returns the list of URLs, or None if the feed doesn't exist.
    """
    if feed.lower() in ("all", "*"):
        return list(feeds.values()) or None
    url = feeds.get(feed)
    return [url] if url else None


def chunk_text(text: str, limit: int = 3900) -> list:
    """Split a long message on line boundaries to respect Telegram's 4096 character limit."""
    chunks, current = [], ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > limit and current:
            chunks.append(current)
            current = ""
        current += line + "\n"
    if current.strip():
        chunks.append(current)
    return chunks
