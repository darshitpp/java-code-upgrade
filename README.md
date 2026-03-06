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
| Language    | 24       | var, records, sealed classes, pattern matching, switch expressions, text blocks |
| Enterprise  | 16       | EJB to CDI, Servlet to JAX-RS, JDBC to JPA, SOAP to REST, Spring modernization  |
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
npx skills add darshitpp/java-code-upgrade
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

### Other Agents

This skill follows the [agentskills.io](https://agentskills.io) open standard and works with any compatible agent. See [Usage with Different Agents](#usage-with-different-agents) below for agent-specific setup.

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

## Usage with Different Agents

This skill follows the [agentskills.io](https://agentskills.io) open standard. It auto-activates when relevant to Java modernization tasks, or can be invoked explicitly.

### Claude Code

| Scope                   | Path                                  |
|-------------------------|---------------------------------------|
| Personal (all projects) | `~/.claude/skills/java-code-upgrade/` |
| Project                 | `.claude/skills/java-code-upgrade/`   |

**Invoke:** Ask naturally ("modernize this Java code") or explicitly with `/java-code-upgrade`. Claude loads the skill automatically when relevant.

[Claude Code skills docs](https://code.claude.com/docs/en/skills)

### Cursor

| Scope         | Path                                                                       |
|---------------|----------------------------------------------------------------------------|
| User (global) | `~/.cursor/skills/java-code-upgrade/`                                      |
| Project       | `.cursor/skills/java-code-upgrade/` or `.agents/skills/java-code-upgrade/` |

**Invoke:** Ask naturally or use `/java-code-upgrade` in chat. Cursor auto-discovers skills at startup. You can also install from GitHub via **Settings > Rules > Add Rule > Remote Rule (Github)**.

[Cursor skills docs](https://cursor.com/docs/context/skills)

### GitHub Copilot / VS Code

| Scope    | Path                                                                            |
|----------|---------------------------------------------------------------------------------|
| Personal | `~/.copilot/skills/java-code-upgrade/` or `~/.claude/skills/java-code-upgrade/` |
| Project  | `.github/skills/java-code-upgrade/` or `.claude/skills/java-code-upgrade/`      |

**Invoke:** Copilot auto-discovers and loads skills when relevant to the task.

[Copilot skills docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

### OpenAI Codex

| Scope   | Path                                   |
|---------|----------------------------------------|
| User    | `~/.agents/skills/java-code-upgrade/`  |
| Project | `.agents/skills/java-code-upgrade/`    |
| System  | `/etc/codex/skills/java-code-upgrade/` |

**Invoke:** Reference with `/skills` or `$` mention syntax, or let Codex auto-select based on task context.

[Codex skills docs](https://developers.openai.com/codex/skills/)

### Goose

| Scope   | Path                                                                                        |
|---------|---------------------------------------------------------------------------------------------|
| Global  | `~/.config/goose/skills/java-code-upgrade/` or `~/.config/agents/skills/java-code-upgrade/` |
| Project | `.goose/skills/java-code-upgrade/` or `.agents/skills/java-code-upgrade/`                   |

**Invoke:** Ask "Use the java-code-upgrade skill" or let Goose auto-activate when relevant.

[Goose skills docs](https://block.github.io/goose/docs/guides/context-engineering/using-skills/)

### Roo Code

| Scope   | Path                                                                        |
|---------|-----------------------------------------------------------------------------|
| Global  | `~/.roo/skills/java-code-upgrade/` or `~/.agents/skills/java-code-upgrade/` |
| Project | `.roo/skills/java-code-upgrade/` or `.agents/skills/java-code-upgrade/`     |

**Invoke:** Roo indexes all skills at startup and auto-activates when your request matches. No manual registration needed.

[Roo Code skills docs](https://docs.roocode.com/features/skills)

### Amp

| Scope   | Path                                |
|---------|-------------------------------------|
| Project | `.agents/skills/java-code-upgrade/` |

[Amp skills docs](https://ampcode.com/manual#agent-skills)

### Junie (JetBrains)

[Junie skills docs](https://junie.jetbrains.com/docs/agent-skills.html)

### Gemini CLI

[Gemini CLI skills docs](https://geminicli.com/docs/cli/skills/)

### Other Agents

For any other [agentskills.io](https://agentskills.io)-compatible agent, place the skill directory where the agent discovers skills (typically `~/.agents/skills/` globally or `.agents/skills/` per-project). The `SKILL.md` file is the entry point. The agent loads references and scripts on demand via progressive disclosure.

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

MIT License.

- **Pattern data** (`references/` content) — Copyright (c) 2026 Bruno Borges, from [javaevolved.github.io](https://github.com/javaevolved/javaevolved.github.io)
- **Skill tooling** (SKILL.md, scripts, assets, CI pipelines) — Copyright (c) 2026 Darshit Patel

Both components are licensed under the MIT License. See [LICENSE](LICENSE) for the full text.
