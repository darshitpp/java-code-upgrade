#!/usr/bin/env python3
"""Search Java evolution pattern YAML files and return matching patterns.

Reads YAML pattern files from a data directory and filters them by category,
JDK version, difficulty, keyword, or code snippet detection.
"""

import argparse
import os
import re
import sys
import textwrap


# ---------------------------------------------------------------------------
# Minimal YAML parser (stdlib-only fallback)
# ---------------------------------------------------------------------------

def _try_import_yaml():
    """Try to import PyYAML; return None on failure."""
    try:
        import yaml  # type: ignore
        return yaml
    except ImportError:
        return None


_yaml_mod = _try_import_yaml()


def _parse_yaml_value(raw):
    """Coerce a raw YAML scalar string into a Python value."""
    if raw is None:
        return None
    stripped = raw.strip()
    if stripped == "" or stripped == "~" or stripped.lower() == "null":
        return None
    if stripped.lower() == "true":
        return True
    if stripped.lower() == "false":
        return False
    # Try int
    try:
        return int(stripped)
    except ValueError:
        pass
    # Try float
    try:
        return float(stripped)
    except ValueError:
        pass
    # Remove surrounding quotes
    if (stripped.startswith('"') and stripped.endswith('"')) or \
       (stripped.startswith("'") and stripped.endswith("'")):
        return stripped[1:-1]
    return stripped


def _simple_yaml_load(text):
    """Parse a *simple* YAML document (flat scalars, block scalars, simple
    lists of scalars/maps) into a dict.  This is intentionally limited to
    the structure used by the Java-evolution pattern files.
    """
    result = {}
    lines = text.splitlines()
    i = 0
    n = len(lines)

    def _current_indent(line):
        return len(line) - len(line.lstrip())

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Skip blanks, comments, document markers
        if not stripped or stripped.startswith("#") or stripped == "---":
            i += 1
            continue

        # Must be a key line at indent 0
        m = re.match(r'^([A-Za-z_][\w]*):\s*(.*)', line)
        if not m:
            i += 1
            continue

        key = m.group(1)
        rest = m.group(2).strip()

        # Block scalar (|- or |, >- or >)
        if rest in ("|-", "|", ">-", ">", "|+", ">+"):
            fold = rest.startswith(">")
            block_lines = []
            i += 1
            if i < n:
                block_indent = _current_indent(lines[i])
                if block_indent == 0 and lines[i].strip():
                    # No indented content follows
                    result[key] = ""
                    continue
                while i < n:
                    bl = lines[i]
                    if bl.strip() == "":
                        block_lines.append("")
                        i += 1
                        continue
                    if _current_indent(bl) < block_indent and bl.strip():
                        break
                    block_lines.append(bl[block_indent:] if len(bl) >= block_indent else bl.lstrip())
                    i += 1
            # Strip trailing empty lines for |- / >-
            if rest.endswith("-"):
                while block_lines and block_lines[-1] == "":
                    block_lines.pop()
            if fold:
                result[key] = " ".join(block_lines)
            else:
                result[key] = "\n".join(block_lines)
            continue

        # List value (next lines start with "- ")
        if rest == "":
            # Could be a list or nested map
            items = []
            i += 1
            if i < n and re.match(r'^\s+-\s', lines[i]):
                list_indent = _current_indent(lines[i])
                while i < n:
                    li = lines[i]
                    if li.strip() == "" or li.strip().startswith("#"):
                        i += 1
                        continue
                    if _current_indent(li) < list_indent and li.strip():
                        break
                    lm = re.match(r'^(\s+)-\s+(.*)', li)
                    if lm and _current_indent(li) == list_indent:
                        item_first = lm.group(2).strip()
                        # Check if it's a map entry (key: value)
                        km = re.match(r'^([A-Za-z_][\w]*):\s*(.*)', item_first)
                        if km:
                            item_dict = {km.group(1): _parse_yaml_value(km.group(2))}
                            i += 1
                            # Read continuation keys at deeper indent
                            while i < n:
                                ci = lines[i]
                                if ci.strip() == "" or ci.strip().startswith("#"):
                                    i += 1
                                    continue
                                if _current_indent(ci) <= list_indent:
                                    break
                                ckm = re.match(r'^\s+([A-Za-z_][\w]*):\s*(.*)', ci)
                                if ckm:
                                    item_dict[ckm.group(1)] = _parse_yaml_value(ckm.group(2))
                                i += 1
                            items.append(item_dict)
                        else:
                            items.append(_parse_yaml_value(item_first))
                            i += 1
                    else:
                        i += 1
                result[key] = items
            else:
                result[key] = None
            continue

        # Inline value — may be a long folded line with backslash continuation
        val = rest
        i += 1
        # Handle trailing backslash continuation (YAML folded style used in some files)
        while val.endswith("\\") and i < n:
            next_line = lines[i].strip()
            val = val[:-1] + next_line
            i += 1

        # Inline list [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            result[key] = [_parse_yaml_value(v) for v in inner.split(",")]
            continue

        result[key] = _parse_yaml_value(val)
        continue

    return result


def load_yaml(path):
    """Load a YAML file and return a dict."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if _yaml_mod:
        return _yaml_mod.safe_load(text) or {}
    return _simple_yaml_load(text)


# ---------------------------------------------------------------------------
# Pattern loading and filtering
# ---------------------------------------------------------------------------

def discover_yaml_files(data_dir):
    """Return sorted list of .yaml file paths under data_dir."""
    files = []
    for dirpath, _dirnames, filenames in os.walk(data_dir):
        for fn in filenames:
            if fn.endswith(".yaml"):
                files.append(os.path.join(dirpath, fn))
    files.sort()
    return files


def load_patterns(data_dir):
    """Load all patterns from YAML files."""
    patterns = []
    for path in discover_yaml_files(data_dir):
        try:
            data = load_yaml(path)
            if data and isinstance(data, dict) and "slug" in data:
                patterns.append(data)
        except Exception as exc:
            print(f"Warning: failed to parse {path}: {exc}", file=sys.stderr)
    return patterns


def matches_keyword(pattern, keyword):
    """Return True if keyword appears in searchable text fields."""
    kw = keyword.lower()
    for field in ("title", "summary", "explanation", "oldApproach", "modernApproach"):
        val = pattern.get(field)
        if val and kw in str(val).lower():
            return True
    return False


def matches_detect(pattern, snippet):
    """Return True if the Java code snippet appears to use old patterns
    described by this YAML entry.  We tokenize oldCode and oldApproach into
    meaningful keywords and check if any appear in the snippet.
    """
    snippet_lower = snippet.lower()
    for field in ("oldCode", "oldApproach"):
        val = pattern.get(field)
        if not val:
            continue
        # Extract identifiers / method-like tokens from the old code/approach
        tokens = set(re.findall(r'[A-Za-z_][\w.]*(?:\(\))?', str(val)))
        for token in tokens:
            tok_lower = token.lower()
            # Skip very short / generic tokens
            if len(tok_lower) <= 2:
                continue
            if tok_lower in snippet_lower:
                return True
    return False


def filter_patterns(patterns, args):
    """Apply all filters and return matching patterns."""
    results = []
    for p in patterns:
        if args.category and p.get("category") != args.category:
            continue
        jdk = p.get("jdkVersion")
        try:
            jdk_int = int(jdk) if jdk is not None else None
        except (ValueError, TypeError):
            jdk_int = None
        if args.min_jdk is not None and (jdk_int is None or jdk_int < args.min_jdk):
            continue
        if args.max_jdk is not None and (jdk_int is None or jdk_int > args.max_jdk):
            continue
        if args.difficulty and p.get("difficulty") != args.difficulty:
            continue
        if args.keyword and not matches_keyword(p, args.keyword):
            continue
        if args.detect and not matches_detect(p, args.detect):
            continue
        results.append(p)
    return results


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_brief(pattern):
    category = pattern.get("category", "?")
    slug = pattern.get("slug", "?")
    title = pattern.get("title", "?")
    jdk = pattern.get("jdkVersion", "?")
    summary = pattern.get("summary", "")
    return f"[{category}/{slug}] {title} (Java {jdk}) - {summary}"


def format_full(pattern):
    lines = []
    lines.append("=" * 72)
    lines.append(f"  {pattern.get('title', '?')}")
    lines.append(f"  Category: {pattern.get('category', '?')}  |  "
                 f"Difficulty: {pattern.get('difficulty', '?')}  |  "
                 f"JDK: {pattern.get('jdkVersion', '?')}")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"Slug: {pattern.get('category', '?')}/{pattern.get('slug', '?')}")
    lines.append("")
    if pattern.get("summary"):
        lines.append("Summary:")
        lines.append(textwrap.indent(str(pattern["summary"]), "  "))
        lines.append("")
    if pattern.get("explanation"):
        lines.append("Explanation:")
        lines.append(textwrap.indent(str(pattern["explanation"]), "  "))
        lines.append("")
    lines.append(f"--- Old Approach: {pattern.get('oldLabel', '')} ---")
    lines.append(f"  {pattern.get('oldApproach', '')}")
    lines.append("")
    if pattern.get("oldCode"):
        lines.append("Old Code:")
        lines.append(textwrap.indent(str(pattern["oldCode"]), "  "))
        lines.append("")
    lines.append(f"--- Modern Approach: {pattern.get('modernLabel', '')} ---")
    lines.append(f"  {pattern.get('modernApproach', '')}")
    lines.append("")
    if pattern.get("modernCode"):
        lines.append("Modern Code:")
        lines.append(textwrap.indent(str(pattern["modernCode"]), "  "))
        lines.append("")
    why = pattern.get("whyModernWins")
    if why and isinstance(why, list):
        lines.append("Why Modern Wins:")
        for item in why:
            if isinstance(item, dict):
                icon = item.get("icon", "")
                ttl = item.get("title", "")
                desc = item.get("desc", "")
                lines.append(f"  {icon} {ttl}: {desc}")
            else:
                lines.append(f"  - {item}")
        lines.append("")
    docs = pattern.get("docs")
    if docs and isinstance(docs, list):
        lines.append("Docs:")
        for d in docs:
            if isinstance(d, dict):
                lines.append(f"  - {d.get('title', '')}: {d.get('href', '')}")
            else:
                lines.append(f"  - {d}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_parser():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_data_dir = os.path.join(script_dir, "..", "references")

    parser = argparse.ArgumentParser(
        description="Search Java evolution pattern YAML files and return matching patterns."
    )
    parser.add_argument(
        "--data-dir",
        default=default_data_dir,
        help="Directory containing category sub-dirs with YAML files "
             "(default: references/ relative to this script)."
    )
    parser.add_argument(
        "--category",
        choices=[
            "language", "collections", "strings", "streams",
            "concurrency", "io", "errors", "datetime",
            "security", "tooling", "enterprise",
        ],
        help="Filter by category.",
    )
    parser.add_argument(
        "--min-jdk",
        type=int,
        help="Minimum JDK version (e.g., 10, 17, 21).",
    )
    parser.add_argument(
        "--max-jdk",
        type=int,
        help="Maximum JDK version.",
    )
    parser.add_argument(
        "--difficulty",
        choices=["beginner", "intermediate", "advanced"],
        help="Filter by difficulty.",
    )
    parser.add_argument(
        "--keyword",
        help="Search keyword in title, summary, explanation, oldApproach, modernApproach.",
    )
    parser.add_argument(
        "--detect",
        help="A snippet of Java code to scan for old patterns.",
    )
    parser.add_argument(
        "--format",
        choices=["brief", "full"],
        default="brief",
        dest="output_format",
        help="Output format: brief (default) or full.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    data_dir = os.path.abspath(args.data_dir)
    if not os.path.isdir(data_dir):
        print(f"Error: data directory not found: {data_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        patterns = load_patterns(data_dir)
    except Exception as exc:
        print(f"Error loading patterns: {exc}", file=sys.stderr)
        sys.exit(1)

    results = filter_patterns(patterns, args)

    for p in results:
        if args.output_format == "full":
            print(format_full(p))
        else:
            print(format_brief(p))

    sys.exit(0)


if __name__ == "__main__":
    main()
