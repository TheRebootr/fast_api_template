# Documentation Style Guide

This document outlines the style and structure used for technical documentation in the API project.

## Documentation Philosophy

All technical documentation should be:

- **Quick to scan** - Use headers, code blocks, and tables
- **Action-oriented** - Show HOW to do things, not just WHAT they are
- **Example-driven** - Every concept has a code example
- **Workflow-focused** - Common use cases front and center
- **Searchable** - Clear section headers for easy navigation

## Document Structure

### 1. Title - Quick Reference

All main docs should have "Quick Reference" in the title to set expectations.

```markdown
# Topic Name - Quick Reference
```

### 2. Quick Commands Section (If Applicable)

Start with the most common commands users will need.

````markdown
## Quick Commands

```bash
# Most common operation
just command-name "description"

# Second most common
just other-command
```
````

````

### 3. Common Workflows
Show complete workflows for common tasks, numbered 1-N.

```markdown
## Common Workflows

### 1. Task Name

**Step 1:** Description
```python
# Code example
````

**Step 2:** Description

```bash
# Command example
```

**Step 3:** Result

````

### 4. Command/API Reference
Comprehensive reference with examples.

```markdown
## Reference

### Command Name
**Purpose:** What it does
**Usage:**
```bash
command --options
````

**Example:**

```bash
command --flag value
```

````

### 5. Troubleshooting
Common problems and solutions.

```markdown
## Troubleshooting

### Problem Description

```bash
# Solution steps
````

````

### 6. Best Practices
Do's and Don'ts.

```markdown
## Best Practices

### ✅ Do
- Action item
- Another action

### ❌ Don't
- Anti-pattern
- Common mistake
````

### 7. Checklist (If Applicable)

Task checklists for complex operations.

```markdown
## Checklist

Before doing X:

- [ ] Check this
- [ ] Verify that
- [ ] Test something
```

### 8. Project-Specific Notes

Details specific to this project.

```markdown
## Project-Specific Notes

### Configuration

- Setting: Value
- Location: Path

### Important Files

- `path/to/file` - Description
```

### 9. Tips & Resources

Helpful tips and links.

```markdown
## Tips

💡 **Tip** - Helpful insight
💡 **Another tip** - More advice

## Resources

- [Link](url) - Description
- Project file: `path/to/file`
```

## Formatting Conventions

### Code Blocks

**Python:**

```python
# Always include comments explaining the code
from typing import Annotated

def example() -> str:
    """Always include docstrings."""
    return "value"
```

**Bash:**

```bash
# Use actual commands that work in the project
just command

# Show expected output when helpful
# Output: Success message
```

**SQL:**

```sql
-- Use proper SQL formatting
SELECT column_name
FROM table_name
WHERE condition = true
ORDER BY column_name;
```

### Headers

- `#` - Document title only
- `##` - Major sections
- `###` - Subsections
- `####` - Rarely used, only for nested content

### Lists

**Bullet points** for unordered items:

- First item
- Second item
  - Nested item

**Numbered lists** for sequential steps:

1. First step
2. Second step
3. Third step

**Checkboxes** for actionable items:

- [ ] Task to complete
- [ ] Another task
- [x] Completed task

### Tables

Use tables for comparing options or listing attributes:

| Feature | Description   | Example   |
| ------- | ------------- | --------- |
| Name    | What it does  | `code`    |
| Other   | Another thing | `example` |

### Emphasis

- **Bold** for commands, important concepts, and emphasis
- `backticks` for code, filenames, and variable names
- _Italic_ rarely used, prefer bold

### Callouts

Use emoji for visual callouts:

```markdown
✅ Do this
❌ Don't do this
⚠️ Warning
💡 Tip
🔜 Coming soon
📝 Note
🚀 Performance tip
```

## Examples from This Project

### Good Documentation Examples

1. **dependency_injection.md** - Quick reference with patterns
2. **database_migration.md** - Workflow-focused with examples
3. **dependency_injection_quick_reference.md** - Ultra-condensed reference

### Structure Comparison

#### Before (Old Style)

```markdown
# Database Migrations

Alembic is used for migrations.

## What is a Migration?

A migration is a versioned set of changes...

## Common Commands

- Create migration: `alembic revision`
- Apply migrations: `alembic upgrade`
```

**Problems:**

- Theory before practice
- No examples
- No workflows
- Command syntax hard to remember

#### After (New Style)

````markdown
# Database Migrations - Quick Reference

## Quick Commands

```bash
# Create migration (recommended)
just create-migration "add user table"

# Apply migrations
just migrate
```
````

## Common Workflows

### 1. Add a New Table

**Step 1:** Create the model

```python
class Product(Base):
    __tablename__ = "products"
    name: Mapped[str]
```

**Step 2:** Generate migration

```bash
just create-migration "add product table"
```

````

**Benefits:**
- Immediately useful
- Shows complete workflows
- Real code examples
- Easy to scan

## Writing New Documentation

### Checklist

When creating new documentation:

- [ ] Title includes "Quick Reference" if appropriate
- [ ] Starts with most common use cases
- [ ] Every concept has a code example
- [ ] Code examples are tested and work
- [ ] Commands use `just` when available
- [ ] Includes troubleshooting section
- [ ] Has best practices section
- [ ] Links to related documentation
- [ ] Uses consistent formatting
- [ ] Reviewed for clarity

### Template

```markdown
# [Topic Name] - Quick Reference

## Quick Commands

```bash
# Most common command
just main-command
````

## Common Workflows

### 1. Most Common Task

**Step 1:** First action

```python
# Code example
```

**Step 2:** Second action

```bash
# Command example
```

## Reference

### Feature Name

Description of feature

**Usage:**

```python
# Example usage
```

## Troubleshooting

### Common Problem

Solution steps

## Best Practices

### ✅ Do

- Good practice

### ❌ Don't

- Anti-pattern

## Tips

💡 **Tip** - Helpful advice

## Resources

- [Link](url)
- Project file: `path/to/file`

```

## Maintenance

### Updating Documentation

When code changes:
1. Update affected documentation
2. Test all code examples
3. Update screenshots if any
4. Check internal links
5. Update "last modified" date if tracked

### Documentation Reviews

Before merging:
- [ ] All code examples tested
- [ ] Commands verified to work
- [ ] Links are not broken
- [ ] Formatting is consistent
- [ ] Follows this style guide

## Summary

Good documentation:
- Gets users productive quickly
- Shows, doesn't just tell
- Anticipates common questions
- Stays current with code changes
- Is easy to scan and search

Follow these guidelines to maintain high-quality, consistent documentation across the project.
```
