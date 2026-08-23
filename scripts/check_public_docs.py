#!/usr/bin/env python3
"""检查公开仓库的本地链接、事实快照和禁用旧口径。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
FORBIDDEN_TEXT = {
    "168,950": "已过期的精确馆藏数",
    "162,690": "已过期的分类合计数",
    "均可免费在线阅读与下载": "未经核验的在线阅读和永久可用表述",
    "所以书籍都提供": "旧FAQ错字和过度承诺",
    "合肥智人同行网络科技工作室": "不在公开仓库披露运营主体",
}


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


def check_local_links(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    text_without_code = FENCED_CODE_RE.sub("", text)
    for raw_target in LINK_RE.findall(text_without_code):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith(("#", "https://", "http://", "mailto:")):
            continue
        target_path = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not target_path:
            continue
        resolved = (path.parent / target_path).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: 本地链接越出仓库范围: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: 本地链接不存在: {target}")
    return errors


def check_snapshot() -> list[str]:
    errors: list[str] = []
    snapshot_path = ROOT / "data" / "public-snapshot.json"
    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"data/public-snapshot.json 无法读取: {exc}"]

    expected = {
        "schema_version": 1,
        "verified_on": "2026-08-23",
        "collection_label": "17万+",
        "online_reader_verified": False,
        "automatic_copyright_ownership_check": False,
        "repository_hosts_ebook_files": False,
    }
    for key, value in expected.items():
        if snapshot.get(key) != value:
            errors.append(f"data/public-snapshot.json: {key} 应为 {value!r}")

    required_search_fields = {"书名", "作者", "出版社", "ISBN"}
    if set(snapshot.get("search_fields", [])) != required_search_fields:
        errors.append("data/public-snapshot.json: search_fields 与已核验搜索字段不一致")
    return errors


def main() -> int:
    errors: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        errors.extend(check_local_links(path, text))
        for phrase, reason in FORBIDDEN_TEXT.items():
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)}: 包含{reason}: {phrase}")

    errors.extend(check_snapshot())
    if errors:
        print("公开文档检查失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"公开文档检查通过：{len(markdown_files())} 个Markdown文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
