#!/usr/bin/env python3
"""Generates markdown reference files from javaevolved YAML content files.

Usage:
    python3 generate-references.py --content-dir /path/to/content --output-dir /path/to/references
"""

import argparse
import os
import re
import sys


def parse_yaml_simple(text):
    """Parse the simple YAML structure used by javaevolved content files.
    Handles flat scalars, block scalars (|-, |, >), lists of maps, and quoted strings.
    """
    result = {}
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip blank lines and document markers
        if not line.strip() or line.strip() == '---':
            i += 1
            continue

        # Top-level key
        m = re.match(r'^(\w+):\s*(.*)', line)
        if not m:
            i += 1
            continue

        key = m.group(1)
        value_part = m.group(2).strip()

        # Block scalar (|- or | or > or >-)
        if value_part in ('|-', '|', '>', '>-'):
            block_lines = []
            i += 1
            while i < len(lines) and (lines[i].startswith('  ') or lines[i].strip() == ''):
                if lines[i].strip() == '' and i + 1 < len(lines) and not lines[i + 1].startswith('  '):
                    break
                block_lines.append(lines[i][2:] if lines[i].startswith('  ') else '')
                i += 1
            result[key] = '\n'.join(block_lines).rstrip()
            continue

        # List of maps (whyModernWins, docs, related, etc.)
        if value_part == '' or value_part is None:
            i += 1
            if i < len(lines) and lines[i].startswith('- '):
                items = []
                while i < len(lines) and (lines[i].startswith('- ') or lines[i].startswith('  ')):
                    if lines[i].startswith('- '):
                        item = {}
                        first_field = lines[i][2:]
                        fm = re.match(r'(\w+):\s*(.*)', first_field)
                        if fm:
                            item[fm.group(1)] = fm.group(2).strip().strip('"').strip("'")
                        else:
                            # Simple list item (e.g., related slugs)
                            item = first_field.strip().strip('"').strip("'")
                        i += 1
                        while i < len(lines) and lines[i].startswith('  ') and not lines[i].startswith('- '):
                            fm2 = re.match(r'\s+(\w+):\s*(.*)', lines[i])
                            if fm2 and isinstance(item, dict):
                                val = fm2.group(2).strip().strip('"').strip("'")
                                # Handle continuation lines
                                if val.endswith('\\'):
                                    val = val[:-1]
                                    i += 1
                                    while i < len(lines) and lines[i].startswith('    '):
                                        val += lines[i].strip()
                                        if not val.endswith('\\'):
                                            break
                                        val = val[:-1]
                                        i += 1
                                    item[fm2.group(1)] = val
                                    continue
                                item[fm2.group(1)] = val
                            i += 1
                        items.append(item)
                    else:
                        i += 1
                result[key] = items
            continue

        # Quoted or plain scalar
        val = value_part.strip('"').strip("'")
        # Handle backslash continuation
        if val.endswith('\\'):
            val = val[:-1]
            i += 1
            while i < len(lines) and lines[i].startswith('  '):
                cont = lines[i].strip().strip('"').strip("'")
                if cont.endswith('\\'):
                    val += cont[:-1]
                    i += 1
                else:
                    val += cont
                    i += 1
                    break
            result[key] = val
            continue

        result[key] = val
        i += 1

    return result


def load_patterns(content_dir):
    """Load all YAML pattern files from the content directory."""
    patterns = {}
    for category in sorted(os.listdir(content_dir)):
        cat_path = os.path.join(content_dir, category)
        if not os.path.isdir(cat_path):
            continue
        patterns[category] = []
        for fname in sorted(os.listdir(cat_path)):
            if not fname.endswith('.yaml'):
                continue
            fpath = os.path.join(cat_path, fname)
            with open(fpath, 'r') as f:
                text = f.read()
            data = parse_yaml_simple(text)
            data['_category'] = category
            patterns[category].append(data)
    return patterns


def generate_category_md(category, entries):
    """Generate a markdown reference file for a category."""
    lines = [f"# {category.title()} Patterns", ""]

    for entry in entries:
        title = entry.get('title', 'Unknown')
        jdk = entry.get('jdkVersion', '?')
        old_label = entry.get('oldLabel', '')
        modern_label = entry.get('modernLabel', '')
        old_approach = entry.get('oldApproach', '')
        modern_approach = entry.get('modernApproach', '')
        summary = entry.get('summary', '')
        old_code = entry.get('oldCode', '')
        modern_code = entry.get('modernCode', '')
        why = entry.get('whyModernWins', [])
        docs = entry.get('docs', [])

        lines.append(f"## {title}")
        lines.append(f"- **Since:** Java {jdk}")
        lines.append(f"- **Old approach:** {old_approach} ({old_label})")
        lines.append(f"- **Modern approach:** {modern_approach} ({modern_label})")
        lines.append(f"- **Summary:** {summary}")
        lines.append("")

        if old_code:
            lines.append("### Before")
            lines.append("```java")
            lines.append(old_code)
            lines.append("```")
            lines.append("")

        if modern_code:
            lines.append("### After")
            lines.append("```java")
            lines.append(modern_code)
            lines.append("```")
            lines.append("")

        if why and isinstance(why, list):
            lines.append("### Why modern wins")
            for item in why:
                if isinstance(item, dict):
                    lines.append(f"- **{item.get('title', '')}:** {item.get('desc', '')}")
            lines.append("")

        if docs and isinstance(docs, list):
            lines.append("### References")
            for doc in docs:
                if isinstance(doc, dict):
                    lines.append(f"- [{doc.get('title', '')}]({doc.get('href', '')})")
            lines.append("")

        lines.append("---")
        lines.append("")

    return '\n'.join(lines)


def extract_detection_signatures(old_code, old_approach):
    """Extract meaningful code signatures from oldCode for pattern detection.
    Returns a list of grep-friendly signature strings."""
    if not old_code:
        return []

    sigs = []

    # 1. Full method call chains: e.g. Collections.unmodifiableList(, Runtime.getRuntime().exec(
    for m in re.finditer(r'[A-Z]\w+(?:\.\w+)+\s*\(', old_code):
        sig = m.group(0).rstrip('(').strip()
        if len(sig) > 8:
            sigs.append(sig + '(')

    # 2. Constructor calls: new ClassName<...>(
    for m in re.finditer(r'new\s+[A-Z]\w+(?:<[^>]*>)?\s*\(', old_code):
        # Simplify to: new ClassName(
        simplified = re.sub(r'<[^>]*>', '', m.group(0)).strip()
        if len(simplified) > 6:
            sigs.append(simplified)

    # 3. Annotations: @WebServlet, @Stateless, etc.
    for m in re.finditer(r'@[A-Z]\w+', old_code):
        sigs.append(m.group(0))

    # 4. extends/implements patterns: extends HttpServlet, implements MessageListener
    for m in re.finditer(r'(?:extends|implements)\s+[A-Z]\w+', old_code):
        sigs.append(m.group(0))

    # 5. Specific string literals that are detection-worthy (JNDI paths, XML tags)
    for m in re.finditer(r'"(java:comp/[^"]+|<bean\s|-----BEGIN)"', old_code):
        sigs.append(m.group(1))

    # 6. Chained method calls: .trim().isEmpty(), .get().toString()
    for m in re.finditer(r'\.\w+\(\)\.\w+\(\)', old_code):
        sig = m.group(0)
        if len(sig) > 6:
            sigs.append(sig)

    # 7. Variable method chains: list.get(list.size(), future.get(), optional.get()
    for m in re.finditer(r'\b\w+\.\w+\(\w*\.?\w*\(?\)?\s*[-+]?\s*\d*\)', old_code):
        sig = m.group(0).strip()
        # Only keep if it looks like a meaningful API call
        if len(sig) > 8 and not sig[0].isupper() and '.' in sig:
            sigs.append(sig)

    # 8. Keyword patterns from oldApproach when no code signatures found
    if not sigs and old_approach:
        sigs.append(old_approach)

    # Deduplicate preserving order
    seen = set()
    unique = []
    for s in sigs:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    return unique[:6]  # Cap at 6 signatures per pattern


def generate_detection_md(patterns):
    """Generate detection-patterns.md from oldCode and oldApproach fields."""
    lines = [
        "# Detection Patterns Reference", "",
        "Maps old Java code signatures to modernization patterns.",
        "Use this to identify which patterns apply when scanning source code.",
        "",
        "_Auto-generated from upstream YAML data. Do not edit manually._", ""
    ]

    for category in sorted(patterns.keys()):
        entries = patterns[category]
        lines.append(f"## {category.title()}")
        lines.append("")
        for entry in entries:
            slug = entry.get('slug', '')
            jdk = entry.get('jdkVersion', '?')
            old_approach = entry.get('oldApproach', '')
            old_code = entry.get('oldCode', '')

            sigs = extract_detection_signatures(old_code, old_approach)
            if sigs:
                sig_str = ", ".join(f"`{s}`" for s in sigs)
            else:
                sig_str = "_(informational — no code signature)_"

            lines.append(
                f"- **{slug}** (Java {jdk}+): "
                f"Old=`{old_approach}` | Detect: {sig_str}"
            )
        lines.append("")

    return '\n'.join(lines)


def generate_index_md(patterns):
    """Generate the pattern index lookup table."""
    lines = ["# Pattern Index", "",
             "Quick lookup table for all Java modernization patterns.", ""]

    total = 0
    for category in sorted(patterns.keys()):
        entries = patterns[category]
        lines.append(f"## {category.title()}")
        lines.append("")
        lines.append("| Slug | Title | JDK Version | Difficulty |")
        lines.append("|------|-------|-------------|------------|")
        for entry in entries:
            slug = entry.get('slug', '')
            title = entry.get('title', '')
            jdk = entry.get('jdkVersion', '?')
            diff = entry.get('difficulty', '')
            lines.append(f"| {slug} | {title} | {jdk} | {diff} |")
            total += 1
        lines.append("")

    lines.insert(3, f"**Total patterns: {total}**")
    lines.insert(4, "")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate markdown reference files from javaevolved YAML content."
    )
    parser.add_argument('--content-dir', required=True,
                        help="Path to the content/ directory with category subdirs.")
    parser.add_argument('--output-dir', required=True,
                        help="Path to the references/ output directory.")
    args = parser.parse_args()

    if not os.path.isdir(args.content_dir):
        print(f"ERROR: Content directory not found: {args.content_dir}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Loading patterns from {args.content_dir}...")
    patterns = load_patterns(args.content_dir)

    total = 0
    for category, entries in patterns.items():
        md = generate_category_md(category, entries)
        out_path = os.path.join(args.output_dir, f"{category}.md")
        with open(out_path, 'w') as f:
            f.write(md)
        count = len(entries)
        total += count
        print(f"  {category}.md: {count} patterns")

    index_md = generate_index_md(patterns)
    index_path = os.path.join(args.output_dir, "pattern-index.md")
    with open(index_path, 'w') as f:
        f.write(index_md)
    print(f"  pattern-index.md: index of {total} patterns")

    detection_md = generate_detection_md(patterns)
    detection_path = os.path.join(args.output_dir, "detection-patterns.md")
    with open(detection_path, 'w') as f:
        f.write(detection_md)
    print(f"  detection-patterns.md: detection signatures for {total} patterns")

    print(f"Done. {total} patterns written to {args.output_dir}/")


if __name__ == '__main__':
    main()
