# Conventional Commit

Create well-formatted git commits following conventional commit standards.

## Purpose

Standardize commit messages for better changelog generation and semantic versioning.

## Usage

```
/commit
```

## What this command does

1. **Checks git status** to see what's staged
2. **Suggests commit type** based on changes
3. **Formats commit message** with conventional format
4. **Creates commit** with proper structure

## Conventional Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style (formatting, no logic change)
- **refactor:** Code refactoring (no feature/fix)
- **test:** Adding or updating tests
- **chore:** Maintenance (deps, config, etc.)
- **perf:** Performance improvement
- **ci:** CI/CD changes
- **build:** Build system changes

## Examples

### Simple commit
```bash
git add .
git commit -m "feat: add user authentication"
```

### With scope
```bash
git commit -m "fix(api): handle timeout errors gracefully"
```

### With body and footer
```bash
git commit -m "feat(auth): add JWT token refresh

- Implement refresh token endpoint
- Add token expiry validation
- Update authentication middleware

Closes #123"
```

### Breaking change
```bash
git commit -m "feat(api)!: redesign authentication API

BREAKING CHANGE: Auth endpoints now require API version header"
```

## Best Practices

- ✅ Use present tense ("add" not "added")
- ✅ Keep subject under 50 characters
- ✅ Capitalize subject line
- ✅ No period at end of subject
- ✅ Use body to explain "what" and "why"
- ✅ Reference issues in footer
- ✅ Use `!` or `BREAKING CHANGE:` for breaking changes

## Quick Reference

```bash
# Stage changes
git add <files>

# Check what's staged
git status

# Create commit
git commit -m "type: description"

# Amend last commit (if not pushed)
git commit --amend
```
