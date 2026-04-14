import asyncio
import base64
from pathlib import Path

import anthropic
from playwright.async_api import Page, Locator, FrameLocator

from .models import BannerDetection

# Common selectors for consent banners
BANNER_SELECTORS = [
    # Known CMP selectors — check first, most reliable
    "#CybotCookiebotDialog",
    ".cc-banner",
    "#onetrust-banner-sdk",
    "#onetrust-consent-sdk",
    ".sp-message-container",
    "#sp-cc",
    ".evidon-banner",
    "#truste-consent-track",
    "#cookieConsent",
    ".js-cookie-consent",
    "[data-testid='cookie-banner']",
    "[data-cookieconsent]",
    ".cky-consent-container",       # CookieYes
    "[data-cky-tag='notice']",      # CookieYes
    ".cc-window",                   # Cookie Consent (Osano)
    "#cookie-law-info-bar",         # GDPR Cookie Consent plugin
    ".gdpr-cookie-notice",          # GDPR Cookie Notice plugin
    "#moove_gdpr_cookie_info_bar",  # GDPR Cookie Compliance
    ".cli-modal-backdrop",          # CookieLaw plugin
    # Aria-based — fairly reliable
    "[aria-label*='cookie consent' i]",
    "[aria-label*='cookie banner' i]",
    "[role='dialog'][aria-label*='cookie' i]",
    "[role='dialog'][aria-label*='consent' i]",
    "[role='region'][aria-label*='cookie' i]",
    "[role='region'][aria-label*='consent' i]",
    # Specific class patterns — consent banners specifically
    "[class*='cookie-banner' i]",
    "[class*='cookie-notice' i]",
    "[class*='consent-banner' i]",
    "[class*='consent-bar' i]",
    "[class*='cookie-consent' i]",
    "[class*='gdpr-banner' i]",
    "[class*='privacy-banner' i]",
    # Generic fallbacks — last resort, may match non-banner elements
    "[class*='consent' i][class*='container' i]",
    "[id*='cookie-banner' i]",
    "[id*='consent-banner' i]",
    "[id*='gdpr' i]",
]

# Known CMP iframe selectors — checked when the banner element is an iframe
IFRAME_BANNER_SELECTORS = [
    "#ifrmCookieBanner",
    "iframe[title*='cookie' i]",
    "iframe[title*='consent' i]",
    "iframe[title*='privacy' i]",
    "iframe[id*='cookie' i]",
    "iframe[id*='consent' i]",
    "#sp-consent-message",
    "iframe.sp-message-container",
]

# Exclude elements that are likely not the banner itself
MIN_BANNER_HEIGHT = 40
MIN_BANNER_WIDTH = 200
MAX_BANNER_HEIGHT_RATIO = 0.6  # Banner shouldn't be more than 60% of viewport

# Tags that are never the banner itself
EXCLUDED_TAGS = {"HTML", "BODY", "HEAD", "HEADER", "FOOTER", "NAV", "MAIN", "SECTION", "ARTICLE"}


async def _is_banner_candidate(el: Locator, viewport_height: int = 900) -> bool:
    """Check if an element is a plausible consent banner (not body, nav, footer, etc.)."""
    try:
        tag = await el.evaluate("el => el.tagName")
        if tag.upper() in EXCLUDED_TAGS:
            return False
        box = await el.bounding_box()
        if not box:
            return False
        if box["height"] < MIN_BANNER_HEIGHT or box["width"] < MIN_BANNER_WIDTH:
            return False
        # Banner shouldn't take up most of the page (that's probably the page itself)
        if box["height"] > viewport_height * MAX_BANNER_HEIGHT_RATIO:
            return False
        return True
    except Exception:
        return False


async def _find_banner_element(page: Page) -> Locator | None:
    """Try each selector to find a visible consent banner on the parent page."""
    viewport = page.viewport_size or {"height": 900}
    vh = viewport["height"]

    for selector in BANNER_SELECTORS:
        try:
            elements = page.locator(selector)
            count = await elements.count()
            for i in range(count):
                el = elements.nth(i)
                if not await el.is_visible():
                    continue
                if await _is_banner_candidate(el, vh):
                    return el
        except Exception:
            continue
    return None


async def _find_iframe_banner(page: Page) -> tuple[Locator | None, FrameLocator | None]:
    """Find a consent banner inside an iframe.

    Returns (iframe_element, frame_locator) or (None, None).
    The iframe_element is the <iframe> tag in the parent DOM (for screenshots).
    The frame_locator reaches inside the iframe (for text/buttons).
    """
    for selector in IFRAME_BANNER_SELECTORS:
        try:
            iframe_el = page.locator(selector)
            if await iframe_el.count() == 0:
                continue
            if not await iframe_el.first.is_visible():
                continue
            box = await iframe_el.first.bounding_box()
            if not box or box["height"] < MIN_BANNER_HEIGHT:
                continue

            # Get a frame_locator to reach inside
            frame = page.frame_locator(selector)
            # Verify we can access content inside
            body = frame.locator("body")
            body_text = await body.inner_text(timeout=3000)
            if body_text and body_text.strip():
                return iframe_el.first, frame
        except Exception:
            continue
    return None, None


async def _is_iframe(locator: Locator) -> bool:
    """Check if a locator points to an iframe element."""
    try:
        tag = await locator.evaluate("el => el.tagName")
        return tag.upper() == "IFRAME"
    except Exception:
        return False


async def _extract_buttons(banner: Locator | FrameLocator) -> list[str]:
    """Extract visible button/link text from the banner (works with both Locator and FrameLocator)."""
    buttons: list[str] = []
    for tag in ["button", "a", "[role='button']", "input[type='submit']"]:
        elements = banner.locator(tag)
        count = await elements.count()
        for i in range(count):
            el = elements.nth(i)
            try:
                if await el.is_visible():
                    text = (await el.inner_text()).strip()
                    if text and text not in buttons:
                        buttons.append(text)
            except Exception:
                continue
    return buttons


async def _extract_text_from_frame(frame: FrameLocator) -> str:
    """Extract visible text from inside an iframe banner."""
    try:
        body = frame.locator("body")
        return (await body.inner_text(timeout=3000)).strip()
    except Exception:
        return ""


async def _extract_html_from_frame(frame: FrameLocator) -> str:
    """Extract HTML from inside an iframe banner."""
    try:
        body = frame.locator("body")
        html = await body.evaluate("el => el.innerHTML")
        return html[:5000]
    except Exception:
        return ""


async def _vision_fallback(page: Page, screenshot_path: str) -> BannerDetection:
    """Use Claude Vision to detect a consent banner from a screenshot."""
    import os

    screenshot_bytes = await page.screenshot(full_page=False)
    Path(screenshot_path).write_bytes(screenshot_bytes)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return BannerDetection(banner_found=False, screenshot_path=screenshot_path)

    client = anthropic.Anthropic(api_key=api_key)
    b64_image = base64.b64encode(screenshot_bytes).decode()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": b64_image,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "Look at this webpage screenshot. Is there a cookie consent banner visible? "
                            "If yes, describe the banner text and list the button labels you see. "
                            "Respond in this exact JSON format:\n"
                            '{"banner_found": true/false, "text": "banner text or null", "buttons": ["button1", "button2"]}'
                        ),
                    },
                ],
            }
        ],
    )

    import json
    text = response.content[0].text
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        data = json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        return BannerDetection(banner_found=False, screenshot_path=screenshot_path)

    return BannerDetection(
        banner_found=data.get("banner_found", False),
        text=data.get("text"),
        buttons=data.get("buttons", []),
        screenshot_path=screenshot_path,
    )


async def detect_banner(page: Page, url: str, screenshots_dir: str | Path | None = None) -> BannerDetection:
    """Navigate to URL and detect a cookie consent banner.

    Handles both regular DOM banners and iframe-based CMPs.
    Returns a BannerDetection with banner info or banner_found=False.
    """
    if screenshots_dir is None:
        from .output import get_screenshots_dir
        screenshots_dir = get_screenshots_dir(url)
    screenshots_path = Path(screenshots_dir)
    screenshots_path.mkdir(parents=True, exist_ok=True)

    await page.goto(url, wait_until="domcontentloaded")
    # Wait for potential delayed banner render
    await asyncio.sleep(3)

    # Strategy 1: Find banner in the parent DOM
    banner = await _find_banner_element(page)

    if banner is not None:
        # Check if the found element is an iframe
        if await _is_iframe(banner):
            # The selector matched an iframe — try to reach inside it
            iframe_el, frame = await _find_iframe_banner(page)
            if frame is not None:
                return await _build_iframe_detection(page, iframe_el, frame, screenshots_path)
            # iframe found but can't access content — fall through to extract what we can
        else:
            # Regular DOM banner
            banner_text = await banner.inner_text()
            banner_html = await banner.evaluate("el => el.outerHTML")
            buttons = await _extract_buttons(banner)

            screenshot_path = str(screenshots_path / "banner.png")
            try:
                await banner.screenshot(path=screenshot_path)
            except Exception:
                await page.screenshot(path=screenshot_path)

            return BannerDetection(
                banner_found=True,
                text=banner_text.strip(),
                buttons=buttons,
                screenshot_path=screenshot_path,
                html=banner_html[:5000],
            )

    # Strategy 2: Look specifically for iframe-based CMP banners
    if banner is None:
        await asyncio.sleep(3)  # Extra wait for lazy-loaded iframes
    iframe_el, frame = await _find_iframe_banner(page)
    if frame is not None:
        return await _build_iframe_detection(page, iframe_el, frame, screenshots_path)

    # Strategy 3: Vision fallback
    screenshot_path = str(screenshots_path / "page-full.png")
    return await _vision_fallback(page, screenshot_path)


async def _build_iframe_detection(
    page: Page,
    iframe_el: Locator | None,
    frame: FrameLocator,
    screenshots_path: Path,
) -> BannerDetection:
    """Build a BannerDetection from an iframe-based banner."""
    banner_text = await _extract_text_from_frame(frame)
    banner_html = await _extract_html_from_frame(frame)
    buttons = await _extract_buttons(frame)

    screenshot_path = str(screenshots_path / "banner.png")
    try:
        if iframe_el is not None:
            await iframe_el.screenshot(path=screenshot_path)
        else:
            await page.screenshot(path=screenshot_path)
    except Exception:
        await page.screenshot(path=screenshot_path)

    return BannerDetection(
        banner_found=True,
        text=banner_text,
        buttons=buttons,
        screenshot_path=screenshot_path,
        html=banner_html,
    )
