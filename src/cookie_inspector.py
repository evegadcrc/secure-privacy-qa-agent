from playwright.async_api import BrowserContext

from .models import CookieInfo, CookieAudit

# Known tracking/analytics cookie name patterns
TRACKING_PATTERNS = [
    "_ga", "_gid", "_gat", "__utma", "__utmb", "__utmc", "__utmz",  # Google Analytics
    "_fbp", "_fbc", "fr",  # Facebook
    "_tt_", "_ttp",  # TikTok
    "_pin_unauth",  # Pinterest
    "IDE", "DSID", "test_cookie",  # DoubleClick/Google Ads
    "_gcl_au", "_gcl_aw",  # Google Ads conversion
    "APISID", "SAPISID",  # Google general (NID, SSID excluded — too ambiguous as substrings)
    "_uetsid", "_uetvid",  # Microsoft/Bing
    "li_sugr", "bcookie", "lidc",  # LinkedIn
    "sc_at",  # Snapchat
    "_rdt_uuid",  # Reddit
    "hubspotutk", "__hssc", "__hssrc", "__hstc",  # HubSpot
    "_clck", "_clsk",  # Microsoft Clarity
    "_hj", "_hjSession", "_hjSessionUser", "_hjIncludedInSessionSample",  # Hotjar
    "_hjAbsoluteSessionInProgress", "_hjFirstSeen",  # Hotjar
    "ajs_anonymous_id", "ajs_user_id",  # Segment
    "mp_", "mixpanel",  # Mixpanel
    "__eventn",  # EventNative / Jitsu
    "amplitude_id",  # Amplitude
    "_pk_id", "_pk_ses",  # Matomo/Piwik
    "partnero_",  # Partnero (affiliate tracking)
]

# Patterns for necessary/functional cookies
NECESSARY_PATTERNS = [
    "session", "csrf", "xsrf", "token", "__cfduid", "cf_clearance",
    "PHPSESSID", "JSESSIONID", "ASP.NET_SessionId",
    "consent", "cookie_consent", "cookieconsent", "OptanonConsent",
    "CookieConsent", "euconsent",
]


def classify_cookie(name: str) -> str:
    """Classify a cookie as necessary, analytics, marketing, or unknown.

    Tracking patterns are checked FIRST because some tracking cookies
    contain words like 'session' (e.g. Hotjar's _hjSession) that would
    falsely match necessary patterns.
    """
    name_lower = name.lower()

    # Check tracking/analytics first — more specific patterns
    for pattern in TRACKING_PATTERNS:
        if pattern.lower() in name_lower:
            # Distinguish analytics vs marketing
            analytics_prefixes = (
                "_ga", "_gid", "_gat", "__utm", "_clck", "_clsk",  # Web analytics
                "_hj", "_pk_id", "_pk_ses",  # Session recording / analytics
                "mp_", "mixpanel", "amplitude_id", "__eventn",  # Product analytics
            )
            if any(name_lower.startswith(p.lower()) for p in analytics_prefixes):
                return "analytics"
            return "marketing"

    for pattern in NECESSARY_PATTERNS:
        if pattern.lower() in name_lower:
            return "necessary"

    return "unknown"


def is_tracking_cookie(cookie_info: CookieInfo) -> bool:
    """Check if a cookie is a tracking/analytics/marketing cookie."""
    return cookie_info.category in ("analytics", "marketing")


async def capture_cookies(context: BrowserContext) -> list[CookieInfo]:
    """Capture all cookies from the browser context."""
    raw_cookies = await context.cookies()
    cookies = []
    for c in raw_cookies:
        cookies.append(
            CookieInfo(
                name=c["name"],
                domain=c.get("domain", ""),
                category=classify_cookie(c["name"]),
                secure=c.get("secure", False),
                http_only=c.get("httpOnly", False),
            )
        )
    return cookies


def find_violations(
    cookies_before: list[CookieInfo],
    cookies_after_accept: list[CookieInfo],
    cookies_after_reject: list[CookieInfo],
) -> list[str]:
    """Identify GDPR/CCPA cookie violations."""
    violations = []

    # Check: tracking cookies present before consent
    tracking_before = [c for c in cookies_before if is_tracking_cookie(c)]
    if tracking_before:
        names = ", ".join(c.name for c in tracking_before)
        violations.append(
            f"Tracking cookies set BEFORE consent: {names}. "
            "GDPR requires no tracking cookies until explicit consent is given."
        )

    # Check: tracking cookies present after reject
    tracking_after_reject = [c for c in cookies_after_reject if is_tracking_cookie(c)]
    if tracking_after_reject:
        names = ", ".join(c.name for c in tracking_after_reject)
        violations.append(
            f"Tracking cookies present AFTER rejection: {names}. "
            "Rejecting consent must prevent all non-essential cookies."
        )

    # Check: no cookies set after accept (might indicate broken consent)
    if cookies_after_accept and not any(is_tracking_cookie(c) for c in cookies_after_accept):
        violations.append(
            "No tracking cookies set after accepting consent. "
            "This may indicate the consent mechanism is not functional."
        )

    return violations


async def audit_cookies(
    context: BrowserContext,
    cookies_before: list[CookieInfo] | None = None,
    cookies_after_accept: list[CookieInfo] | None = None,
    cookies_after_reject: list[CookieInfo] | None = None,
) -> CookieAudit:
    """Build a CookieAudit from the provided cookie snapshots.

    Any snapshot not provided will be captured from the current context.
    """
    if cookies_before is None:
        cookies_before = await capture_cookies(context)
    if cookies_after_accept is None:
        cookies_after_accept = []
    if cookies_after_reject is None:
        cookies_after_reject = []

    violations = find_violations(cookies_before, cookies_after_accept, cookies_after_reject)

    return CookieAudit(
        cookies_before_consent=cookies_before,
        cookies_after_accept=cookies_after_accept,
        cookies_after_reject=cookies_after_reject,
        violations=violations,
    )
