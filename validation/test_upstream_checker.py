#!/usr/bin/env python3
"""Synthetic, local boundary tests for the pinned upstream checker; never edits upstream."""
from __future__ import annotations

import hashlib
import json
import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / ".agents/skills/handwritten-math-notes-to-latex"
CHECKER = UPSTREAM / "scripts/check_latex_project.py"
OUT = ROOT / "validation/upstream-checker-tests"
BASE = "\\documentclass{article}\n\\begin{document}\n% Source PDF page 1\n$x=1$.\n\\end{document}\n"


def git(*args: str) -> str:
    # Portable metadata adapter: upstream is a pristine bundled copy, not a nested Git repo.
    info = json.loads((ROOT / "validation/upstream-provenance.json").read_text())
    if args == ("ls-files",):
        return "\n".join(info["files_sha256"])
    if args == ("rev-parse", "HEAD"):
        return info["commit"]
    if args == ("remote", "get-url", "origin"):
        return info["upstream_url"] + ".git"
    if args == ("status", "--porcelain"):
        bad = [name for name, digest in info["files_sha256"].items()
               if hashlib.sha256((UPSTREAM / name).read_bytes()).hexdigest() != digest]
        return "\n".join("modified: " + name for name in bad)
    raise ValueError("unsupported metadata query: " + repr(args))


def snapshot() -> dict:
    return {
        name: hashlib.sha256((UPSTREAM / name).read_bytes()).hexdigest()
        for name in git("ls-files").splitlines()
    }


def case(name: str, files: dict[str, str], expected_exit: int, meaning: str,
         args: list[str] | None = None, expected_text: str | None = None) -> dict:
    path = OUT / name
    path.mkdir(parents=True, exist_ok=True)
    for relative, value in files.items():
        target = path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value, encoding="utf-8")
    command = [sys.executable, str(CHECKER), str(path), *(args or [])]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    return {
        "name": name, "meaning": meaning, "command": command,
        "expected_exit": expected_exit, "exit": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr,
        "matched_observation": result.returncode == expected_exit
        and (expected_text is None or expected_text in result.stdout + result.stderr),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    before = snapshot()
    cases = [
        case("01_valid", {"main.tex": BASE}, 0, "正常单页基线", ["--expected-start", "1", "--expected-end", "1"]),
        case("02_duplicate_labels", {"main.tex": BASE + "\\label{a}\\label{a}\n"}, 1, "真实重复标签能检出", expected_text="Duplicate labels: 1"),
        case("03_missing_direct_include", {"main.tex": BASE + "\\input{missing}\n"}, 1, "main.tex 的直接缺失 input 能检出", expected_text="Missing includes: 1"),
        case("04_environment_mismatch", {"main.tex": "\\begin{proof}\n\\end{theorem}\n"}, 1, "环境不配对能检出"),
        case("05_page_order_same_file", {"main.tex": "% Source PDF page 2\n% Source PDF page 1\n"}, 1, "同文件页码倒序能检出"),
        case("06_missing_expected_page", {"main.tex": BASE}, 1, "指定页段时缺页能检出", ["--expected-start", "1", "--expected-end", "2"], "Missing expected pages: 2"),
        case("07_missing_main", {"chapter.tex": "% Source PDF page 1\n"}, 0, "main.tex 不存在仍返回成功"),
        case("08_nested_missing_include", {"main.tex": "\\input{chapter}\n", "chapter.tex": "% Source PDF page 1\n\\input{missing}\n"}, 0, "不会递归核查 chapter.tex 内的缺失 input"),
        case("09_comment_only_coverage", {"main.tex": "% Source PDF page 1\n% Source PDF page 2\n"}, 0, "只有页码注释而无正文也算覆盖", ["--expected-start", "1", "--expected-end", "2"]),
        case("10_unreachable_coverage", {"main.tex": "% Source PDF page 1\n", "orphan.tex": "% Source PDF page 2\n"}, 0, "未被入口引用的 TeX 也贡献覆盖", ["--expected-start", "1", "--expected-end", "2"]),
        case("11_duplicate_page_marker", {"main.tex": "% Source PDF page 1\n% Source PDF page 1\n"}, 0, "重复页码不报错"),
        case("12_cross_file_page_order", {"main.tex": "\\input{a}\n\\input{b}\n", "a.tex": "% Source PDF page 2\n", "b.tex": "% Source PDF page 1\n"}, 0, "跨文件实际阅读顺序倒置不检出"),
        case("13_check_is_nonblocking", {"main.tex": BASE + "% CHECK: page 1 uncertain sign\n"}, 0, "CHECK 只报告，不阻止成功", expected_text="CHECK markers: 1"),
        case("14_english_unclear_nonblocking", {"main.tex": BASE + "Unclear in the original manuscript\n"}, 0, "英文未决标记只报告，不阻止成功", expected_text="Unclear markers: 1"),
        case("15_chinese_unclear_unrecognized", {"main.tex": BASE + "【原稿不清，待确认】\n"}, 0, "中文未决标记不识别", expected_text="Unclear markers: 0"),
        case("16_comment_label_false_positive", {"main.tex": BASE + "\\label{a}\n% \\label{a}\n"}, 1, "注释内 label 会造成重复误报", expected_text="Duplicate labels: 1"),
        case("17_comment_include_false_positive", {"main.tex": BASE + "% \\input{not-used}\n"}, 1, "注释内 input 会造成缺文件误报", expected_text="Missing includes: 1"),
        case("18_unbalanced_brace", {"main.tex": BASE + "\\textbf{broken\n"}, 0, "不检查大括号平衡"),
        case("19_broken_reference", {"main.tex": BASE + "See \\ref{never-defined}.\n"}, 0, "不检查未定义引用"),
        case("20_wrong_mathematics", {"main.tex": BASE.replace("$x=1$", "$1+1=3$")}, 0, "数学错误不在结构检查范围"),
        case("21_reverse_expected_range", {"main.tex": BASE}, 0, "expected-start 大于 end 时空范围仍成功", ["--expected-start", "2", "--expected-end", "1"]),
        case("22_partial_expected_range", {"main.tex": BASE}, 2, "只传页段单端会拒绝", ["--expected-start", "1"]),
        case("23_no_tex_markdown_only", {"notes.md": "# 中文笔记\n$x=1$\n"}, 2, "不支持 Markdown 输入"),
        case("24_no_page_flags", {"main.tex": "\\begin{document}\nempty\n\\end{document}\n"}, 0, "未指定 expected 时没有来源页也成功"),
        case("25_chinese_page_marker", {"main.tex": "% 原 PDF 第 1 页\n"}, 1, "中文页码注释不识别", ["--expected-start", "1", "--expected-end", "1"]),
        case("26_extra_page_not_rejected", {"main.tex": "% Source PDF page 1\n% Source PDF page 99\n"}, 0, "预期范围外的页码不拒绝", ["--expected-start", "1", "--expected-end", "1"]),
        case("27_split_environment_false_positive", {"main.tex": "\\begin{proof}\n\\input{chapter}\n", "chapter.tex": "done.\n\\end{proof}\n"}, 1, "合法跨 input 环境会按文件边界误报"),
        case("28_cache_excluded", {"main.tex": BASE, ".cache/experiment.tex": "\\begin{bad}\n"}, 0, ".cache 内 TeX 被排除"),
        case("29_verbatim_environment_false_positive", {"main.tex": BASE + "\\verb|\\begin{fake}|\n"}, 1, "verbatim 样式内容会被当成环境"),
        case("30_multinote_page_collision", {"main.tex": "\\input{note-a}\n\\input{note-b}\n", "note-a.tex": "% Source PDF page 1\n", "note-b.tex": "% Source PDF page 2\n"}, 0, "没有 note_id；另一份笔记的页码可掩盖本份缺页", ["--expected-start", "1", "--expected-end", "2"]),
        case("31_selfcheck_not_supported", {"main.tex": BASE}, 2, "没有内建 --selfcheck", ["--selfcheck"]),
    ]
    help_result = subprocess.run([sys.executable, str(CHECKER), "--help"], text=True, capture_output=True, check=False)
    absent_result = subprocess.run([sys.executable, str(CHECKER), str(OUT / "not-created")], text=True, capture_output=True, check=False)
    after = snapshot()
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "upstream_sha": git("rev-parse", "HEAD"),
        "upstream_remote": git("remote", "get-url", "origin"),
        "tracked_files_sha256_before": before,
        "tracked_files_sha256_after": after,
        "upstream_unchanged": before == after and git("status", "--porcelain") == "",
        "help": {"exit": help_result.returncode, "stdout": help_result.stdout, "stderr": help_result.stderr},
        "missing_directory": {"exit": absent_result.returncode, "stdout": absent_result.stdout, "stderr": absent_result.stderr},
        "cases": cases,
        "case_count": len(cases),
        "matched_observation_count": sum(item["matched_observation"] for item in cases),
    }
    assert len({item["name"] for item in cases}) == len(cases)
    assert report["case_count"] == report["matched_observation_count"]
    assert report["upstream_unchanged"]
    assert help_result.returncode == 0 and absent_result.returncode == 2
    (OUT / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ["upstream_sha", "upstream_unchanged", "case_count", "matched_observation_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
