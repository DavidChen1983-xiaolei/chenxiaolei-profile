#!/usr/bin/env python3
"""个人档案 skill 不变量测试。断言规则，不断言当前值。"""
import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class SkillInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_frontmatter(self):
        self.assertRegex(self.skill, r"^---\nname: chenxiaolei-profile\n")
        self.assertIn('description: "Use when', self.skill)
        self.assertIn("触发词", self.skill)

    def test_required_files(self):
        required = [
            "README.md",
            "references/profile.md",
            "references/style-writing.md",
            "references/style-visual.md",
            "references/workflows.md",
            "references/self-evolution.md",
            "references/github-sync.md",
            "scripts/redact_check.py",
            "scripts/append_evolution.py",
            "evolution/LOG.md",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).exists(), f"缺少 {rel}")

    def test_identity_markers(self):
        text = (ROOT / "references/profile.md").read_text(encoding="utf-8")
        for marker in ["陈小磊", "中学高级教师", "四川师范大学附属实验学校", "知微"]:
            self.assertIn(marker, text)

    def test_writing_rules(self):
        text = (ROOT / "references/style-writing.md").read_text(encoding="utf-8")
        for marker in ["现代白话学术体", "去 AI 味", "GB/T 7714", "数字一律阿拉伯数字"]:
            self.assertIn(marker, text)

    def test_evolution_contract(self):
        text = (ROOT / "references/self-evolution.md").read_text(encoding="utf-8")
        for marker in ["六类触发点", "C1", "C2", "C3", "写回", "MEMORY.md"]:
            self.assertIn(marker, text)
        self.assertIn("结尾画面文字未纳入转写", text)

    def test_github_safety(self):
        text = (ROOT / "references/github-sync.md").read_text(encoding="utf-8")
        self.assertIn("Private", text)
        self.assertIn("pull --rebase", text)
        self.assertIn("禁止 `git push --force`", text)
        self.assertIn("redact_check.py", text)

    def test_no_hardcoded_credentials(self):
        pattern = re.compile(
            r"(api[_-]?key|secret[_-]?key|token)\s*[:=]\s*[\"'][A-Za-z0-9_-]{16,}",
            re.I,
        )
        for f in ROOT.rglob("*"):
            if f.is_file() and f.suffix in {".md", ".py", ".json"}:
                text = f.read_text(encoding="utf-8", errors="ignore")
                self.assertIsNone(pattern.search(text), f"疑似硬编码凭据：{f}")

    def test_skill_md_no_em_dash(self):
        self.assertNotIn("——", self.skill)

    def test_redact_gate_blocks_phone(self):
        mod = load_module("rc", ROOT / "scripts" / "redact_check.py")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "leak.md"
            p.write_text(" Contact: 13800138000 ", encoding="utf-8")
            hits = mod.scan(p)
            self.assertTrue(any(h["kind"] == "手机号" for h in hits))
            safe = Path(d) / "safe.md"
            safe.write_text("学生信息一律化名。", encoding="utf-8")
            self.assertEqual(mod.scan(safe), [])

    def test_evolution_writeback(self):
        mod = load_module("ae", ROOT / "scripts" / "append_evolution.py")
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            (tmp / "references").mkdir()
            ref = tmp / "references" / "workflows.md"
            ref.write_text("# 工作流\n", encoding="utf-8")
            mod.REF_DIR = tmp / "references"
            mod.apply_to_reference("workflows.md", "报告默认四环框架", "E-20261125-001", "C1")
            self.assertIn("E-20261125-001", ref.read_text(encoding="utf-8"))
            with self.assertRaises(ValueError):
                mod.apply_to_reference("../MEMORY.md", "越界", "E-1", "C1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
