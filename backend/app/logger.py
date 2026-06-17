"""
Centralised logger for the AI Travel Planner backend.

All modules import `get_logger(__name__)` to get a child logger that inherits
this configuration automatically.  Log levels:

  INFO  – normal pipeline flow (what every request does)
  DEBUG – detailed data (use when debugging a single run)
  WARNING – recoverable issues (API fallback, missing price)
  ERROR – unexpected failures caught by try/except
"""
import logging
import sys


# ── ANSI colour codes ──────────────────────────────────────────────────────────
_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_DIM    = "\033[2m"

_CYAN   = "\033[96m"
_GREEN  = "\033[92m"
_YELLOW = "\033[93m"
_RED    = "\033[91m"
_BLUE   = "\033[94m"
_MAGENTA= "\033[95m"
_WHITE  = "\033[97m"
_GREY   = "\033[90m"

LEVEL_COLOURS = {
    "DEBUG":    _DIM    + _WHITE,
    "INFO":     _CYAN,
    "WARNING":  _YELLOW,
    "ERROR":    _RED    + _BOLD,
    "CRITICAL": _RED    + _BOLD,
}

# Short icons per level
LEVEL_ICONS = {
    "DEBUG":    "·",
    "INFO":     "▸",
    "WARNING":  "⚠",
    "ERROR":    "✖",
    "CRITICAL": "✖",
}


class _ColouredFormatter(logging.Formatter):
    """Custom formatter that adds colour, icons and module context."""

    def format(self, record: logging.LogRecord) -> str:
        level   = record.levelname
        colour  = LEVEL_COLOURS.get(level, "")
        icon    = LEVEL_ICONS.get(level, " ")

        # Module name: trim "app." prefix and pad
        module  = record.name.replace("app.", "").replace(".", "/")
        module_str = f"{_GREY}[{module}]{_RESET}"

        level_str = f"{colour}{icon} {level:<7}{_RESET}"
        message   = super().format(record)

        return f"{level_str} {module_str} {message}"


def _build_root_logger() -> logging.Logger:
    root = logging.getLogger("app")
    if root.handlers:          # already configured (e.g. reloader re-import)
        return root

    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(_ColouredFormatter())

    root.addHandler(handler)
    root.propagate = False     # don't double-print via uvicorn's root logger
    return root


_build_root_logger()


def get_logger(name: str) -> logging.Logger:
    """Return a child logger for the given module name."""
    return logging.getLogger(name)
