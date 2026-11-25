#!/usr/bin/env python3
"""追加一条自进化记录，按等级决定是否写回 reference 文件。"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "evolution" / "LOG.md"
REF_DIR = ROOT / "references"
START = "<!-- EVOLUTION-START -->"
END = "<!-- EVOLUTION-END -->"


def next_id(today: str) -> str:
    if not LOG.exists():
        last = 0
    else:
        ids = re.findall(r"E-(\d{8})-(\d{3})", LOG.read_text(encoding="utf-8"))
        last = max((int(n) for d, n in ids if d == today), default=0)
    return f"E-{today}-{last + 1:03d}"


def append_log(entry: dict):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text("# 个人档案自进化日志\n\n追加写，禁止覆盖历史。\n\n", encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(
            f"## {entry['id']}\n\n"
            f"- time: {entry['time']}\n"
            f"- trigger: {entry['trigger']}\n"
            f"- raw: {entry['raw']}\n"
            f"- distilled: {entry['distilled']}\n"
            f"- scope: {entry['scope']}\n"
            f"- level: {entry['level']}\n"
            f"- target: {entry['target'] or '仅日志'}\n\n"
        )


def apply_to_reference(target: str, distilled: str, eid: str, level: str):
    if target in {"", "仅日志"}:
        return "未写回 reference"
    if "/" in target or "\\" in target or target.endswith(".md") is False:
        raise ValueError("target 只能是 references/ 下的单个 md 文件名")
    path = REF_DIR / target
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    bullet = f"- [{eid}][{level}] {distilled}"
    if START in text and END in text:
        before, rest = text.split(START, 1)
        middle, after = rest.split(END, 1)
        if bullet in middle:
            return "已存在，未重复写回"
        text = before + START + middle.rstrip() + "\n" + bullet + "\n" + END + after
    else:
        text = text.rstrip() + f"\n\n## 自进化增量（自动生成）\n\n{START}\n{bullet}\n{END}\n"
    path.write_text(text, encoding="utf-8")
    return f"已写回 {target}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trigger", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--distilled", required=True)
    ap.add_argument("--scope", default="未注明")
    ap.add_argument("--level", choices=["C1", "C2", "C3"], required=True)
    ap.add_argument("--target", default="")
    args = ap.parse_args()

    if any(term in args.raw + args.distilled for term in ["陈小磊", "David Chen"]):
        pass  # 用户本人姓名允许；学生信息由 redact_check 在推送前兜底

    now = datetime.now()
    entry = {
        "id": next_id(now.strftime("%Y%m%d")),
        "time": now.isoformat(timespec="seconds"),
        "trigger": args.trigger,
        "raw": args.raw[:100],
        "distilled": args.distilled,
        "scope": args.scope,
        "level": args.level,
        "target": args.target,
    }
    append_log(entry)
    status = "C3 仅留日志，30 天后复核"
    if args.level in {"C1", "C2"} and args.target:
        status = apply_to_reference(args.target, args.distilled, entry["id"], args.level)
    print(f"{entry['id']} 已记录。{status}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"失败：{exc}", file=sys.stderr)
        sys.exit(1)
