______________________________________________________________________

## name: typecheck description: Run static type checking on Python source using ty (Astral's type checker). Use when the user wants to check types, fix type errors, or enforce static typing in this project. allowed-tools: Bash, Read, Edit

Run `ty check` on Python source files and surface any type errors.

## Usage

```
uvx ty check [path]
```

- No path → checks the whole project from the repo root
- Pass a file or directory to scope the check

## Steps

1. Run `uvx ty check` (or with a path if the user specified one).
1. If there are errors, group them by file and summarise what needs fixing.
1. If the user asks to fix errors, apply targeted edits — add type annotations, narrow types, or add `ty: ignore` only as a last resort.
1. Re-run to confirm the errors are resolved.

## Notes

- `ty` is zero-config by default; it reads `pyproject.toml` for settings if present.
- Prefer fixing root causes over suppressing with `ty: ignore`.
- For third-party stubs, `uvx ty check --python .venv` resolves imports from the project venv.
