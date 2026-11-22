#!/usr/bin/env python3
"""Static site gate: HTML links, chapter manifest, standalone SVG."""
from __future__ import annotations
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
class Parse(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.h1=0
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=="h1": self.h1+=1
        for key in ("href", "src"):
            if key in attrs: self.links.append((tag,attrs[key]))
def main():
    errors=[]
    manifest=json.loads((ROOT/"courses.json").read_text(encoding="utf-8"))
    chapters=manifest["chapters"]
    if len(chapters)!=28: errors.append("manifest chapterCount != 28")
    for i,c in enumerate(chapters,1):
        if i<=8 and c.get("revision") != "illustrated": errors.append(f"chapter {i:02d} should be illustrated")
        num=f"{i:02d}"
        if c["num"]!=num or c["file"]!=f"lessons/{num}.html": errors.append(f"manifest {num} mismatch")
        if not (ROOT/c["file"]).is_file(): errors.append(f"missing {c['file']}")
        p=ROOT/f"{num}.html"
        if not p.is_file() or f"lessons/{num}.html" not in p.read_text(encoding="utf-8"): errors.append(f"legacy redirect {num} missing")
    for path in [ROOT/"index.html", *sorted((ROOT/"lessons").glob("*.html"))]:
        obj=Parse(); obj.feed(path.read_text(encoding="utf-8"))
        if path==ROOT/"index.html" or path.stem in tuple(f"{i:02d}" for i in range(1,9)):
            if obj.h1!=1: errors.append(f"{path.relative_to(ROOT)}: expected 1 H1, got {obj.h1}")
        if path.stem in tuple(f"{i:02d}" for i in range(1,9)):
            content=path.read_text(encoding="utf-8")
            if content.count("<figure") < 2:
                errors.append(f"{path.relative_to(ROOT)}: illustrated article has fewer than 2 figures")
            if 'class="article-section"' not in content:
                errors.append(f"{path.relative_to(ROOT)}: missing long-form article sections")
        for tag,link in obj.links:
            if not link or link.startswith(("#","data:","mailto:","tel:","javascript:")): continue
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc: continue
            target=(path.parent/unquote(parsed.path)).resolve()
            if not target.is_relative_to(ROOT): errors.append(f"{path.name}: unsafe path {link}")
            elif not target.is_file(): errors.append(f"{path.relative_to(ROOT)}: broken {link}")
    ns="{http://www.w3.org/2000/svg}"
    for path in sorted((ROOT/"assets/svg").glob("*.svg")):
        try:
            node=ET.parse(path).getroot()
            if node.tag!=ns+"svg" or "viewBox" not in node.attrib: errors.append(f"{path.name}: missing SVG namespace/viewBox")
            if node.find(ns+"title") is None or node.find(ns+"desc") is None: errors.append(f"{path.name}: missing title/desc")
            ids=[e.attrib["id"] for e in node.iter() if "id" in e.attrib]
            if len(ids)!=len(set(ids)): errors.append(f"{path.name}: duplicate id")
        except ET.ParseError as ex: errors.append(f"{path.name}: XML: {ex}")
    if errors:
        print("\n".join("FAIL "+e for e in errors))
        raise SystemExit(1)
    print(f"OK: {len(chapters)} chapters, {len(list((ROOT/'assets/svg').glob('*.svg')))} SVGs, links valid")
if __name__=="__main__": main()
