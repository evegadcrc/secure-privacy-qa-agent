import pytest
from unittest.mock import AsyncMock

from src.cookie_inspector import classify_cookie, is_tracking_cookie, find_violations, capture_cookies
from src.models import CookieInfo


class TestClassifyCookie:
    def test_google_analytics(self):
        assert classify_cookie("_ga") == "analytics"
        assert classify_cookie("_gid") == "analytics"
        assert classify_cookie("_gat_gtag") == "analytics"

    def test_utm_cookies(self):
        assert classify_cookie("__utma") == "analytics"
        assert classify_cookie("__utmz") == "analytics"

    def test_facebook_tracking(self):
        assert classify_cookie("_fbp") == "marketing"
        assert classify_cookie("_fbc") == "marketing"

    def test_doubleclick(self):
        assert classify_cookie("IDE") == "marketing"

    def test_session_cookies(self):
        assert classify_cookie("PHPSESSID") == "necessary"
        assert classify_cookie("session_id") == "necessary"

    def test_consent_cookies(self):
        assert classify_cookie("CookieConsent") == "necessary"
        assert classify_cookie("OptanonConsent") == "necessary"

    def test_csrf_tokens(self):
        assert classify_cookie("csrf_token") == "necessary"
        assert classify_cookie("XSRF-TOKEN") == "necessary"

    def test_hotjar(self):
        assert classify_cookie("_hjSession_5137978") == "analytics"
        assert classify_cookie("_hjSessionUser_5137978") == "analytics"
        assert classify_cookie("_hjFirstSeen") == "analytics"
        assert classify_cookie("_hjAbsoluteSessionInProgress") == "analytics"

    def test_eventnative(self):
        assert classify_cookie("__eventn_id_UMTEy95MJh") == "analytics"

    def test_partnero(self):
        assert classify_cookie("partnero_session_uuid") == "marketing"

    def test_unknown_cookies(self):
        assert classify_cookie("my_custom_cookie") == "unknown"
        assert classify_cookie("random123") == "unknown"


class TestIsTrackingCookie:
    def test_analytics_is_tracking(self):
        cookie = CookieInfo(name="_ga", domain=".example.com", category="analytics", secure=True, http_only=False)
        assert is_tracking_cookie(cookie) is True

    def test_marketing_is_tracking(self):
        cookie = CookieInfo(name="_fbp", domain=".facebook.com", category="marketing", secure=True, http_only=False)
        assert is_tracking_cookie(cookie) is True

    def test_necessary_is_not_tracking(self):
        cookie = CookieInfo(name="session", domain="example.com", category="necessary", secure=True, http_only=True)
        assert is_tracking_cookie(cookie) is False

    def test_unknown_is_not_tracking(self):
        cookie = CookieInfo(name="foo", domain="example.com", category="unknown", secure=False, http_only=False)
        assert is_tracking_cookie(cookie) is False


class TestFindViolations:
    def _make_cookie(self, name: str, category: str) -> CookieInfo:
        return CookieInfo(name=name, domain=".example.com", category=category, secure=True, http_only=False)

    def test_no_violations(self):
        before = [self._make_cookie("session", "necessary")]
        after_accept = [self._make_cookie("session", "necessary"), self._make_cookie("_ga", "analytics")]
        after_reject = [self._make_cookie("session", "necessary")]

        violations = find_violations(before, after_accept, after_reject)
        assert len(violations) == 0

    def test_tracking_before_consent(self):
        before = [self._make_cookie("_ga", "analytics")]
        violations = find_violations(before, [], [])
        assert any("BEFORE consent" in v for v in violations)

    def test_tracking_after_reject(self):
        before = [self._make_cookie("session", "necessary")]
        after_reject = [self._make_cookie("session", "necessary"), self._make_cookie("_fbp", "marketing")]
        violations = find_violations(before, [], after_reject)
        assert any("AFTER rejection" in v for v in violations)


class TestCaptureCookies:
    @pytest.mark.asyncio
    async def test_captures_and_classifies(self):
        context = AsyncMock()
        context.cookies = AsyncMock(return_value=[
            {"name": "_ga", "domain": ".example.com", "secure": True, "httpOnly": False},
            {"name": "session", "domain": "example.com", "secure": True, "httpOnly": True},
        ])

        cookies = await capture_cookies(context)
        assert len(cookies) == 2
        assert cookies[0].category == "analytics"
        assert cookies[1].category == "necessary"
