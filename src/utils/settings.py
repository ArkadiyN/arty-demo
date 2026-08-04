"""Project-wide settings. Loads .env once at import time, then reads os.environ."""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, model_validator


def _env_candidates() -> list[Path]:
    """`.env` paths to load, in precedence order.

    `.claude/rules/git-flow.md` mandates working in a worktree, but `.env` is
    untracked and therefore exists only in the primary checkout. Resolving it
    from the repo root alone left every worktree with zero credentials — the
    tooling appeared to have no API key configured when it simply was not
    looking where the key lives.

    In a worktree, `.git` is a *file* holding `gitdir: <primary>/.git/worktrees/<name>`,
    so the primary checkout is three parents up from that path.
    """
    root = Path(__file__).resolve().parents[2]
    candidates = [root / ".env"]
    git = root / ".git"
    if git.is_file():
        try:
            gitdir = git.read_text(encoding="utf-8").split(":", 1)[1].strip()
            primary = (root / gitdir).resolve().parents[2]
            candidates.append(primary / ".env")
        except (IndexError, OSError):
            pass  # not a worktree pointer we understand; the root candidate stands
    return candidates


#: Searched at import time, in order; first value found for a given key wins.
#: Exposed so a missing-credential error can name the paths actually searched.
ENV_PATHS = _env_candidates()

for _path in ENV_PATHS:
    load_dotenv(_path, override=False)


class Settings(BaseModel):
    anthropic_api_key: str | None = None
    openrouter_api_key: str | None = None
    openrouter_model: str = "openrouter/free"
    google_api_key: str | None = None
    google_model: str = "gemma-4-31b-it"
    google_timeout_ms: int = 120_000
    #: Which vision backend `pdf-processor.py` uses. Selected explicitly rather
    #: than probed: the previous `Google → except → Anthropic` chain turned a
    #: transient Google failure into a silent switch to a paid provider.
    vision_provider: str = "google"

    @model_validator(mode="before")
    @classmethod
    def _from_env(cls, data: object) -> object:
        if isinstance(data, dict) and data:
            return data
        return {
            "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY"),
            "openrouter_api_key": os.environ.get("OPENROUTER_API_KEY"),
            "openrouter_model": os.environ.get("OPENROUTER_MODEL", "openrouter/free"),
            "google_api_key": os.environ.get("GOOGLE_API_KEY"),
            "google_model": os.environ.get("GOOGLE_MODEL", "gemma-4-31b-it"),
            "google_timeout_ms": int(os.environ.get("GOOGLE_TIMEOUT_MS", "120000")),
        }
