#!/usr/bin/env python3
"""推送前脱敏门禁。命中敏感模式返回退出码 1。"""
import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", "node_modules", "evolution", "tests"}
MAX_BYTES = 2 * 1024 * 1024

PATTERNS = [
    ("身份证号", re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")),
    ("手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("成绩排名", re.compile(r"第\s*\d{1,3}\s*名")),
    ("学号", re.compile(r"(?:学号|考生号)\s*[:：]?\s*\d{6,14}")),
    ("姓名与成绩同现", re.compile(r"姓名\s*[:：]\s*[\u4e00-\u9fa5]{2,4}[^\n]{0,30}(?:成绩|排名|家长)")),
    ("凭据", re.compile(r"(?:api[_-]?key|secret[_-]?key|token)\s*[:：=]\s*[\w\-]{16,}", re.I)),
]

ALLOW = [
    re.compile(r"陈小磊"),
    re.compile(r"David Chen"),
]


def scan(path: Path):
    hits = []
    if path.is_file():
        files = [path]
    else:
        files = [p for p in path.rglob("*") if p.is_file()
                 and not any(part in SKIP_DIRS for part in p.parts)]
    for f in files:
        try:
            if f.stat().st_size > MAX_BYTES:
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            cleaned = line
            for rule in ALLOW:
                cleaned = rule.sub("", cleaned)
            for name, pattern in PATTERNS:
                if pattern.search(cleaned):
                    hits.append({
                        "file": str(f),
                        "line": lineno,
                        "kind": name,
                        "excerpt": cleaned.strip()[:120],
                    })
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    hits = scan(Path(args.path))
    if args.json:
        import json
        print(json.dumps({"hits": hits, "blocked": bool(hits)}, ensure_ascii=False, indent=2))
    else:
        if hits:
            print("脱敏门禁未通过，禁止推送：")
            for h in hits:
                print(f"  {h['kind']} | {h['file']}:{h['line']} | {h['excerpt']}")
        else:
            print("脱敏门禁通过：未命中敏感模式。")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
