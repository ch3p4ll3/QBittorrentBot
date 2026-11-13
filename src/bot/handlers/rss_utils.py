"""Pure helpers for the /rss commands (no Telegram or qBittorrent calls, easy to test)."""
import hashlib
import posixpath
import re
from typing import Optional
from urllib.parse import urlparse

MAX_NAME_LEN = 80


def short_id(name: str) -> str:
    """Stable short id for a feed/rule/category name, used in button callback data (64 byte limit)."""
    return hashlib.sha1(name.encode("utf-8")).hexdigest()[:10]


def find_by_id(names, item_id: str) -> Optional[str]:
    """Return the name whose short_id matches item_id, or None."""
    return next((n for n in names if short_id(n) == item_id), None)


def unique_name(name: str, existing) -> str:
    """Return name, or 'name (2)', 'name (3)'... if it is already taken."""
    taken = set(existing)
    if name not in taken:
        return name
    n = 2
    while f"{name} ({n})" in taken:
        n += 1
    return f"{name} ({n})"


def feed_host(url: str) -> str:
    """Return only the host of a feed URL. Feed URLs often embed passkeys, so never show the full URL."""
    try:
        return urlparse(url).netloc or "?"
    except (ValueError, AttributeError):
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


RULE_DELIMITER = ";"   # not "|": qBittorrent itself uses "|" inside a must-contain field to mean "or"
SHOW_FLAG = "show"


def parse_add_rule_args(args: Optional[str]):
    """
    '/rss_addrule name ; feed ; must contain ; [must not contain] ; [category] ; [show]'
    -> dict(name, feed, must_contain, must_not_contain, category, show) or None.
    The optional last field must be the word "show": it turns on the TV options (see show_rule_options).
    """
    if not args:
        return None
    parts = [p.strip() for p in args.split(RULE_DELIMITER)]
    if len(parts) < 3 or len(parts) > 6:
        return None
    parts += [""] * (6 - len(parts))
    name, feed, must_contain, must_not_contain, category, flag = parts
    if not is_valid_name(name) or not feed or not must_contain:
        return None
    if flag and flag.lower() != SHOW_FLAG:
        return None
    return {
        "name": name,
        "feed": feed,
        "must_contain": must_contain,
        "must_not_contain": must_not_contain,
        "category": category,
        "show": bool(flag),
    }


def build_rule_def(feed_urls: list, must_contain: str, must_not_contain: str = "", category: str = "",
                   save_path: str = "", smart_filter: bool = False) -> dict:
    rule = {
        "enabled": True,
        "mustContain": must_contain,
        "mustNotContain": must_not_contain,
        "useRegex": False,
        "affectedFeeds": feed_urls,
        "assignedCategory": category,
        "smartFilter": smart_filter,
        "addPaused": None,
    }
    if save_path:
        # an explicit save path switches qBittorrent's automatic torrent management off for this rule
        rule["savePath"] = save_path
    return rule


def resolve_category(category: str, categories) -> str:
    """
    Return the real name of a category from qBittorrent's list ({name: {...}}), matching case-insensitively
    ('tv' -> 'TV'). Returns the text unchanged when there is no match.
    """
    category = (category or "").strip()
    if category in (categories or {}):
        return category
    return next((c for c in (categories or {}) if c.lower() == category.lower()), category)


def show_folder_name(name: str) -> str:
    """A safe folder name for a show: no path separators or characters that Windows/SMB refuse."""
    cleaned = re.sub(r'[\\/:*?"<>|\x00-\x1f]', " ", name or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned[:MAX_NAME_LEN]


def show_rule_options(category: str, show_name: str, categories) -> dict:
    """
    Extra build_rule_def() arguments for a rule the user explicitly marked as a TV show: the smart episode filter
    (skips an episode that was already downloaded, e.g. a re-release) and, when the category has a save path, a folder
    named after the show inside it. categories: {name: {"savePath": ...}} as returned by qBittorrent; the category
    is looked up by its real name, ignoring case.
    """
    options = {"smart_filter": True}
    base = ((categories or {}).get(resolve_category(category, categories)) or {}).get("savePath") or ""
    folder = show_folder_name(show_name)
    if base and folder:
        options["save_path"] = posixpath.join(base, folder)
    return options


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
