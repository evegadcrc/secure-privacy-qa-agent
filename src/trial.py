"""Demo trial management — limits audit scans to 10.

Stores scan count in a signed local file. Editing the file
invalidates the signature and locks the tool.
"""

import hashlib
import hmac
import json
import time
from pathlib import Path

_SECRET = b"cqa-agent-2026-sp"
_CONFIG_DIR = Path.home() / ".config" / "consent-audit"
_TRIAL_FILE = _CONFIG_DIR / "trial.dat"
SCAN_LIMIT = 10
CONTACT_EMAIL = "evegacrc@gmail.com"


def _sign(data: str) -> str:
    return hmac.new(_SECRET, data.encode(), hashlib.sha256).hexdigest()


def _load() -> dict:
    if not _TRIAL_FILE.exists():
        return {"scans": 0, "started": time.time()}
    try:
        raw = _TRIAL_FILE.read_text()
        parts = raw.rsplit("|", 1)
        if len(parts) != 2:
            return {"scans": 0, "started": time.time()}
        payload, sig = parts
        if not hmac.compare_digest(_sign(payload), sig):
            # Tampered — lock
            return {"scans": SCAN_LIMIT, "started": 0}
        return json.loads(payload)
    except Exception:
        return {"scans": SCAN_LIMIT, "started": 0}


def _save(state: dict) -> None:
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state)
    sig = _sign(payload)
    _TRIAL_FILE.write_text(f"{payload}|{sig}")


def check_trial() -> tuple[bool, int]:
    """Check if the trial is still active.

    Returns (allowed, scans_remaining).
    """
    state = _load()
    remaining = SCAN_LIMIT - state.get("scans", 0)
    return remaining > 0, max(0, remaining)


def record_scan() -> None:
    """Record a completed scan."""
    state = _load()
    state["scans"] = state.get("scans", 0) + 1
    _save(state)


def trial_status_message(scans_remaining: int) -> str:
    """Return a status message for the current trial state."""
    if scans_remaining <= 0:
        return (
            f"[bold red]Demo limit reached ({SCAN_LIMIT} audit scans).[/bold red]\n\n"
            f"Thank you for trying the Cookie Consent Compliance QA Agent.\n"
            f"To unlock unlimited scans, contact: [cyan]{CONTACT_EMAIL}[/cyan]"
        )
    if scans_remaining <= 3:
        return f"[yellow]Demo mode: {scans_remaining} audit scan(s) remaining[/yellow]"
    return f"[dim]Demo mode: {scans_remaining} audit scan(s) remaining[/dim]"
