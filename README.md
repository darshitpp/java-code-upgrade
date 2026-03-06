# java-code-upgrade

An agent skill that helps developers upgrade Java code from older idioms to modern equivalents. Built on the comprehensive pattern database from [java.evolved](https://javaevolved.github.io/) by [Bruno Borges](https://github.com/brunoborges) ([source](https://github.com/javaevolved/javaevolved.github.io)).

## What it does

This skill enables AI coding agents to:

- **Detect legacy Java patterns** in codebases and suggest modern replacements
- **Provide before/after code examples** for 113 patterns across 11 categories
- **Guide enterprise migrations** from Java EE to Jakarta EE, Spring XML to annotations
- **Filter by JDK version** to only suggest patterns compatible with the project's target
- **Prioritize upgrades** by difficulty (beginner, intermediate, advanced)

## Coverage

| Category    | Patterns | Examples                                                                        |
|-------------|----------|---------------------------------------------------------------------------------|
| Language    | 24       | var, records, sealed classes, pattern matching, switch expressions, text blocks  |
| Enterprise  | 16       | EJB to CDI, Servlet to JAX-RS, JDBC to JPA, SOAP to REST, Spring modernization |
| Streams     | 12       | toList(), mapMulti(), gatherers, takeWhile/dropWhile, optional improvements     |
| Concurrency | 11       | Virtual threads, structured concurrency, scoped values, stable values           |
| Collections | 11       | List.of(), Map.of(), sequenced collections, unmodifiable collectors             |
| I/O         | 11       | HTTP client, Files API, Path.of(), transferTo, memory-mapped files              |
| Strings     | 7        | isBlank(), strip(), repeat(), lines(), formatted()                              |
| Errors      | 7        | Helpful NPE, multi-catch, optional chaining, null-in-switch                     |
| Tooling     | 8        | JShell, single-file execution, JFR, AOT preloading                              |
| Date/Time   | 6        | java.time API, Duration/Period, HexFormat, Math.clamp                           |
| Security    | 5        | PEM encoding, KDF, strong random, TLS defaults                                  |
| **Total**   | **113**  | **Java 7 through Java 25**                                                      |

## JDK Version Quick Reference

| JDK | Key Patterns                                                               |
|-----|----------------------------------------------------------------------------|
| 7   | multi-catch, diamond operator                                              |
| 8   | default/static interface methods, streams, CompletableFuture, java.time    |
| 9   | List/Set/Map.of(), Optional improvements, private interface methods        |
| 10  | var, unmodifiable copy                                                     |
| 11  | String.isBlank/strip/repeat/lines, HTTP client, Path.of                    |
| 14  | switch expressions, helpful NPE                                            |
| 15  | text blocks, String.formatted                                              |
| 16  | records, Stream.toList(), mapMulti                                         |
| 17  | sealed classes, RandomGenerator                                            |
| 21  | virtual threads, pattern matching, sequenced collections                   |
| 22  | unnamed variables, FFM API                                                 |
| 24  | stream gatherers                                                           |
| 25  | structured concurrency, scoped values, stable values, compact source files |

## Installation

### Quick Install (recommended)

Install using [skills.sh](https://skills.sh/) — works with Claude Code, GitHub Copilot, Cursor, Cline, Windsurf, and 15+ other agents:

```bash
npx skillsadd darshitpp/java-code-upgrade
```

This auto-detects the agent and installs the skill in the correct location. No manual setup needed.

### Claude Code (manual)

There are two installation scopes:

**Global (available in all projects):**

```bash
git clone https://github.com/darshitpp/java-code-upgrade.git ~/.claude/skills/java-code-upgrade
```

**Per-project (available only in that project):**

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/darshitpp/java-code-upgrade.git .claude/skills/java-code-upgrade
```

After installation, the skill appears automatically in Claude Code's available skills list. It triggers when asking to modernize Java code, review for outdated patterns, or upgrade JDK idioms. It can also be invoked explicitly with `/java-code-upgrade`.

To update the skill later:

```bash
cd ~/.claude/skills/java-code-upgrade   # or .claude/skills/java-code-upgrade
git pull
```

### Other Agent Frameworks

This skill follows the [agentskills.io](https://agentskills.io) specification:

- `SKILL.md` — core agent instructions (entry point)
- `references/` — pattern database loaded on demand via progressive disclosure
- `scripts/find-pattern.py` — CLI tool for programmatic pattern search
- `assets/` — output templates

Clone the repo and point the agent framework at `SKILL.md` as the skill entry point.

## Directory Structure

```
java-code-upgrade/
  SKILL.md                          # Core skill instructions
  scripts/
    find-pattern.py                 # CLI tool for searching patterns
    generate-references.py          # Regenerates references from upstream YAML
    sync-from-source.sh             # Pulls upstream and regenerates
  references/
    detection-patterns.md           # Code signatures for detecting legacy patterns
    pattern-index.md                # Quick lookup table of all 113 patterns
    language.md                     # Language feature patterns (23)
    collections.md                  # Collection patterns (11)
    strings.md                      # String patterns (7)
    streams.md                      # Stream patterns (12)
    concurrency.md                  # Concurrency patterns (11)
    io.md                           # I/O patterns (11)
    errors.md                       # Error handling patterns (7)
    datetime.md                     # Date/time patterns (6)
    security.md                     # Security patterns (5)
    tooling.md                      # Tooling patterns (8)
    enterprise.md                   # Enterprise migration patterns (16)
  assets/
    upgrade-report-template.md      # Template for upgrade reports
```

## Usage Examples

### Search patterns by category
```bash
python3 scripts/find-pattern.py --category concurrency --format brief
```

### Find patterns for a specific JDK version
```bash
python3 scripts/find-pattern.py --min-jdk 17 --max-jdk 21 --format brief
```

### Search by keyword
```bash
python3 scripts/find-pattern.py --keyword "virtual thread" --format full
```

### Detect patterns in code
```bash
python3 scripts/find-pattern.py --detect 'Collections.unmodifiableList(Arrays.asList("a"))' --format brief
```

## Keeping Up to Date

All files in `references/` are auto-generated from upstream YAML data. No manual editing needed.

The reference files can be automatically synced from the upstream [javaevolved](https://github.com/javaevolved/javaevolved.github.io) repository.

### Manual sync
```bash
./scripts/sync-from-source.sh
```

### GitHub Actions (automated)

The included `.github/workflows/sync-upstream.yml` runs weekly and opens a pull request if patterns changed.

**Setup:**
1. No extra tokens needed — the default `GITHUB_TOKEN` handles everything.
2. The schedule runs weekly on Monday at 06:00 UTC. Adjust the cron in the workflow file if needed.
3. Trigger manually anytime from **Actions > Sync from upstream java.evolved > Run workflow**.

### GitLab CI (automated)

The included `.gitlab-ci.yml` defines a `sync-upstream` job with the same behavior, opening a merge request on changes.

**Setup:**
1. Go to **Settings > CI/CD > Variables** and add `GITLAB_TOKEN` — a project access token with `write_repository` and `api` scopes.
2. Go to **CI/CD > Schedules** and create a new schedule with cron `0 6 * * 1` (weekly Monday 06:00 UTC) or any frequency you prefer.
3. Trigger manually anytime from **CI/CD > Pipelines > Run pipeline**.

Both CI options create a PR/MR for review rather than pushing directly, so you can inspect changes before merging.

## Credits & Data Source

All pattern data is sourced from the **[java.evolved](https://javaevolved.github.io/)** project, created by [Bruno Borges](https://github.com/brunoborges). The original YAML content files have been consolidated into markdown reference files for efficient agent consumption with progressive disclosure.

- **Source repository:** [javaevolved/javaevolved.github.io](https://github.com/javaevolved/javaevolved.github.io)
- **Original license:** [MIT License](https://github.com/javaevolved/javaevolved.github.io/blob/main/LICENSE) - Copyright (c) 2026 Bruno Borges

## License

MIT — same as the upstream source data.

```
MIT License

Copyright (c) 2026 Bruno Borges

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
