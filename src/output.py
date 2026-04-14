"""Centralized output directory management.

All generated artifacts go under:
    output/{domain}/
        screenshots/
        analysis-input.json
        analysis-prompt.md
        analysis-result.json
        report.md
        report.html
"""

from pathlib import Path
from urllib.parse import urlparse


def get_output_dir(url: str, base: str = "output") -> Path:
    """Derive a per-site output directory from a URL.

    Examples:
        https://secureprivacy.ai       -> output/secureprivacy.ai/
        https://www.stackoverflow.com  -> output/stackoverflow.com/
        https://sub.example.co.uk/path -> output/sub.example.co.uk/
    """
    parsed = urlparse(url)
    host = parsed.hostname or parsed.netloc or "unknown"
    # Strip leading www.
    if host.startswith("www."):
        host = host[4:]
    output_dir = Path(base) / host
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_screenshots_dir(url: str, base: str = "output") -> Path:
    """Return the screenshots subdirectory for a URL."""
    screenshots = get_output_dir(url, base) / "screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)
    return screenshots
