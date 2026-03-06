# Java Code Upgrade Report

## Summary
- **Files scanned:** {file_count}
- **Patterns detected:** {pattern_count}
- **Categories affected:** {categories}
- **Minimum JDK required for all upgrades:** {max_jdk_needed}

## Detected Patterns

{for_each_pattern}
### {index}. {pattern_title} ({category})
- **File:** `{file_path}:{line_number}`
- **Current:** {old_approach} ({old_label})
- **Suggested:** {modern_approach} ({modern_label})
- **JDK Required:** {jdk_version}+

**Before:**
```java
{old_code}
```

**After:**
```java
{modern_code}
```

**Why upgrade:** {summary}

---
{end_for_each}

## Upgrade Priority
1. **Quick wins** (beginner difficulty, no API changes): Apply immediately
2. **Moderate effort** (intermediate, may need testing): Plan for next sprint
3. **Significant refactoring** (advanced, architectural changes): Discuss with team

## References
{references_list}
