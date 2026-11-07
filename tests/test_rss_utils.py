"""Run with: python -m tests.test_rss_utils   (or pytest)"""
from src.bot.handlers.rss_utils import (
    build_rule_def, chunk_text, feed_host, is_valid_feed_url, is_valid_name,
    parse_add_feed_args, parse_add_rule_args, resolve_feed_urls,
)


def test_feed_host_hides_passkey():
    assert feed_host("https://example.org/feeds.php?passkey=SECRET&auth=1") == "example.org"
    assert "SECRET" not in feed_host("https://example.org/feeds.php?passkey=SECRET")


def test_valid_feed_url():
    assert is_valid_feed_url("https://a.b/rss")
    assert is_valid_feed_url("http://a.b:8080/rss?x=1")
    assert not is_valid_feed_url("ftp://a.b/rss")
    assert not is_valid_feed_url("javascript:alert(1)")
    assert not is_valid_feed_url("not a url")
    assert not is_valid_feed_url("")


def test_valid_name():
    assert is_valid_name("myfeed")
    assert not is_valid_name("")
    assert not is_valid_name("a/b")
    assert not is_valid_name("a|b")
    assert not is_valid_name("x" * 200)


def test_parse_add_feed_args():
    assert parse_add_feed_args("myfeed https://a.b/rss?k=1") == ("myfeed", "https://a.b/rss?k=1")
    assert parse_add_feed_args("  myfeed   https://a.b/rss  ") == ("myfeed", "https://a.b/rss")
    assert parse_add_feed_args("myfeed") is None
    assert parse_add_feed_args("myfeed notaurl") is None
    assert parse_add_feed_args(None) is None
    assert parse_add_feed_args("") is None


def test_parse_add_rule_args():
    r = parse_add_rule_args("shows | myfeed | Foo 1080p | 720p | TV")
    assert r == {"name": "shows", "feed": "myfeed", "must_contain": "Foo 1080p",
                 "must_not_contain": "720p", "category": "TV"}
    r = parse_add_rule_args("shows | myfeed | Foo")
    assert r["must_not_contain"] == "" and r["category"] == ""
    assert parse_add_rule_args("shows | myfeed") is None          # missing must-contain
    assert parse_add_rule_args("shows | | Foo") is None            # missing feed
    assert parse_add_rule_args("a|b|c|d|e|f") is None              # too many fields
    assert parse_add_rule_args(None) is None


def test_resolve_feed_urls():
    feeds = {"a": "https://a/rss", "b": "https://b/rss"}
    assert resolve_feed_urls("a", feeds) == ["https://a/rss"]
    assert resolve_feed_urls("missing", feeds) is None
    assert sorted(resolve_feed_urls("all", feeds)) == ["https://a/rss", "https://b/rss"]
    assert sorted(resolve_feed_urls("*", feeds)) == ["https://a/rss", "https://b/rss"]
    assert resolve_feed_urls("all", {}) is None


def test_build_rule_def():
    d = build_rule_def(["https://a/rss"], "Foo", "Bar", "TV")
    assert d["enabled"] is True and d["useRegex"] is False
    assert d["mustContain"] == "Foo" and d["mustNotContain"] == "Bar"
    assert d["affectedFeeds"] == ["https://a/rss"] and d["assignedCategory"] == "TV"


def test_build_rule_def_show_options():
    d = build_rule_def(["https://a/rss"], "Foo")
    assert d["smartFilter"] is False and "savePath" not in d          # default: nothing extra
    d = build_rule_def(["https://a/rss"], "Foo", "", "Shows", save_path="/downloads/Shows/Foo", smart_filter=True)
    assert d["smartFilter"] is True and d["savePath"] == "/downloads/Shows/Foo" and d["assignedCategory"] == "Shows"


def test_show_folder_name():
    from src.bot.handlers.rss_utils import show_folder_name
    assert show_folder_name("Agatha All Along") == "Agatha All Along"
    assert show_folder_name("  What  if...  ") == "What if"                 # trims spaces and trailing dots
    assert show_folder_name("Law & Order: SVU?") == "Law & Order SVU"         # characters SMB/Windows refuse
    assert "/" not in show_folder_name("../../etc/passwd") and ".." not in show_folder_name("../../etc/passwd")
    assert show_folder_name("..") == "" and show_folder_name("") == ""
    assert len(show_folder_name("x" * 300)) <= 80


def test_show_rule_options():
    from src.bot.handlers.rss_utils import is_shows_category, show_rule_options
    cats = {"Shows": {"savePath": "/downloads/Shows"}, "Movies": {"savePath": "/downloads/Movies"}, "TV": {"savePath": ""}}
    assert is_shows_category("Shows") and is_shows_category("shows") and is_shows_category("TV")
    assert not is_shows_category("Movies") and not is_shows_category("")
    assert show_rule_options("Shows", "Yaga", cats) == {"smart_filter": True, "save_path": "/downloads/Shows/Yaga"}
    assert show_rule_options("shows", "Yaga", {"shows": {"savePath": "/x/"}}) == {"smart_filter": True, "save_path": "/x/Yaga"}
    assert show_rule_options("TV", "Yaga", cats) == {"smart_filter": True}      # category without a save path: filter only
    assert show_rule_options("Shows", "..", cats) == {"smart_filter": True}     # unusable folder name: no folder
    assert show_rule_options("Movies", "Dune", cats) == {}                      # other categories untouched
    assert show_rule_options("", "Dune", cats) == {}
    assert show_rule_options("Shows", "Yaga", None) == {"smart_filter": True}


def test_short_id_and_find_by_id():
    from src.bot.handlers.rss_utils import find_by_id, short_id
    names = ["Foo Show 1080p", "Another feed", "x" * 200]
    for n in names:
        assert len(short_id(n)) == 10 and short_id(n) == short_id(n)   # stable, fits in callback data
    assert find_by_id(names, short_id("Another feed")) == "Another feed"
    assert find_by_id(names, short_id("x" * 200)) == "x" * 200
    assert find_by_id(names, "deadbeef00") is None


def test_unique_name():
    from src.bot.handlers.rss_utils import unique_name
    assert unique_name("a", []) == "a"
    assert unique_name("a", ["a"]) == "a (2)"
    assert unique_name("a", ["a", "a (2)"]) == "a (3)"


def test_callback_data_fits_telegram_limit():
    from src.bot.filters.callbacks import RssDelete, RssItem, RssToggle, RssWatchCat, RssWatchFeed, RssAddFeed
    from src.bot.handlers.rss_utils import short_id
    i = short_id("x" * 200)
    for packed in (RssItem(kind="feed", id=i).pack(), RssToggle(id=i).pack(), RssDelete(kind="rule", id=i, confirm=1).pack(),
                   RssWatchCat(id=i).pack(), RssWatchFeed(id=i).pack(), RssAddFeed(watch=1).pack()):
        assert len(packed.encode()) <= 64, packed


def test_chunk_text():
    text = "\n".join(f"line {i}" for i in range(2000))
    chunks = chunk_text(text, limit=3900)
    assert len(chunks) > 1 and all(len(c) <= 3901 for c in chunks)
    assert "".join(chunks).replace("\n", "") == text.replace("\n", "")


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok", fn.__name__)
    print(f"{len(fns)} tests passed")
