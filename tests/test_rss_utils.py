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
