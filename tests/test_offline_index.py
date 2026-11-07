"""Offline index integrity regression tests (stdlib only)."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OfflineNavParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_nav = False
        self.links = []
        self.nav_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "nav" and attrs.get("id") == "offlineChapters":
            self.in_nav = True
            self.nav_count += 1
        if self.in_nav and tag == "a":
            self.links.append(attrs.get("href"))

    def handle_endtag(self, tag):
        if tag == "nav" and self.in_nav:
            self.in_nav = False


class OfflineIndexTests(unittest.TestCase):
    def test_offline_links_match_course_manifest(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        courses = json.loads((ROOT / "courses.json").read_text(encoding="utf-8"))
        parser = OfflineNavParser()
        parser.feed(html)
        expected = [course["file"] for course in courses["chapters"]]
        self.assertEqual(parser.nav_count, 1)
        self.assertEqual(parser.links, expected)
        self.assertEqual(len(expected), len(set(expected)))
        for name in expected:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_fallback_is_present_without_javascript(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        nav = html.split('<nav id="offlineChapters"', 1)[1].split("</nav>", 1)[0]
        self.assertNotIn(" hidden", nav.split(">", 1)[0])
        self.assertIn("offlineChapters.hidden = true", html)
        self.assertIn("课程卡片未能加载，请使用上方离线章节目录", html)


if __name__ == "__main__":
    unittest.main()
