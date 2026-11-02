#!/usr/bin/env python3
"""Validate repository skill entry points, catalog metadata, and local links."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
REQUIRED_METADATA = {"version", "author", "abstract", "categories", "rules", "sections"}


def validate_skill(directory: Path) -> list[str]:
    errors = []
    entry = directory / "SKILL.md"
    if not entry.is_file():
        return [f"{directory}: missing SKILL.md"]
    content = entry.read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) != 3 or parts[0].strip():
        return [f"{entry}: missing frontmatter"]
    fields = {}
    for line in parts[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([a-z][a-z-]*):[ \t]+([^\n]+)", line)
        if not match:
            errors.append(f"{entry}: unsupported frontmatter line {line!r}")
            continue
        key, value = match.groups()
        if key in fields:
            errors.append(f"{entry}: duplicate frontmatter key {key}")
        if value[0] in "'\"[{|>&*!%@`" or re.search(r":\s|\s#", value):
            errors.append(f"{entry}: unsupported frontmatter scalar for {key}")
        fields[key] = value
    for key in sorted(fields.keys() - ALLOWED_KEYS):
        errors.append(f"{entry}: unsupported frontmatter key {key}")
    if fields.get("name", "").strip('"\'') != directory.name:
        errors.append(f"{entry}: name must match directory {directory.name}")
    if not fields.get("description", "").strip():
        errors.append(f"{entry}: missing description")

    for filename in ("README.md", "metadata.json"):
        if not (directory / filename).is_file():
            errors.append(f"{directory}: missing {filename}")
    try:
        metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
        missing = REQUIRED_METADATA - metadata.keys()
        if missing:
            errors.append(f"{directory}: missing metadata fields {sorted(missing)}")
        else:
            sections = metadata["sections"]
            if not isinstance(sections, list) or any(
                not isinstance(s, dict)
                or not {"prefix", "name", "count"} <= s.keys()
                or not isinstance(s["count"], int)
                or isinstance(s["count"], bool)
                or s["count"] < 0
                for s in sections
            ):
                errors.append(f"{directory}: invalid metadata sections")
            elif metadata["categories"] != len(sections) or metadata["rules"] != sum(
                s["count"] for s in sections
            ):
                errors.append(f"{directory}: inconsistent metadata counts")
            else:
                rules = directory / "rules"
                for section in sections:
                    prefix = section["prefix"]
                    guide = rules / prefix / "guide.md"
                    if guide.is_file():
                        matches = [guide]
                    else:
                        matches = list(rules.glob(f"{prefix}-*.md"))
                        flat = rules / f"{prefix}.md"
                        if flat.is_file():
                            matches.append(flat)
                        if directory.name == "python-coding-standards" and prefix == "design":
                            matches.extend(rules.glob("solid-*.md"))
                    if len(matches) != section["count"]:
                        errors.append(f"{directory}: section {prefix} count differs from rule files")
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        errors.append(f"{directory}: invalid metadata: {exc}")
    return errors


def heading_anchors(text: str) -> set[str]:
    anchors = set()
    counts = {}
    text = re.sub(r"```[\s\S]*?```", "", text)
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        heading = re.sub(r"<[^>]*>|[`*]", "", heading).lower()
        heading = re.sub(r"(?<!\w)_(?=\S)|(?<=\S)_(?!\w)", "", heading)
        slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(f"{slug}-{count}" if count else slug)
    return anchors


def validate_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`\n]*`", "", text)
    errors = []
    for target in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^\s)]+)", text):
        if target.startswith(("http:", "https:", "mailto:", "/", "<")):
            continue
        filename, _, fragment = target.partition("#")
        destination = path.parent / unquote(filename) if filename else path
        if not destination.exists():
            errors.append(f"{path}: unresolved link {target}")
        elif fragment and destination.is_file() and destination.suffix.lower() == ".md":
            fragment = unquote(fragment).replace("\ufe0f", "")
            if fragment not in heading_anchors(destination.read_text(encoding="utf-8")):
                errors.append(f"{path}: unresolved heading {target}")
    return errors


def main() -> int:
    directories = sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith("."))
    errors = []
    for directory in directories:
        errors.extend(validate_skill(directory))
        for path in directory.rglob("*.md"):
            # Templates and generated example output intentionally use placeholder links.
            if path.name == "_template.md" or "assets" in path.parts or path.name == "sample-output.md":
                continue
            errors.extend(validate_links(path))
    errors.extend(validate_links(ROOT / "README.md"))
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Validated {len(directories)} skills; {len(errors)} error(s).")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
