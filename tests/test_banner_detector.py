import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.banner_detector import _find_banner_element, _extract_buttons, BANNER_SELECTORS


@pytest.fixture
def mock_page():
    page = AsyncMock()
    page.viewport_size = {"width": 1280, "height": 900}
    return page


@pytest.fixture
def mock_locator():
    locator = AsyncMock()
    locator.count = AsyncMock(return_value=1)
    locator.nth = MagicMock(return_value=locator)
    locator.is_visible = AsyncMock(return_value=True)
    locator.bounding_box = AsyncMock(return_value={"height": 100, "width": 800, "x": 0, "y": 0})
    locator.evaluate = AsyncMock(return_value="DIV")  # Not an excluded tag
    return locator


class TestBannerDetectorSelectors:
    def test_has_common_selectors(self):
        """Verify essential selectors are present."""
        selector_str = " ".join(BANNER_SELECTORS)
        assert "cookie" in selector_str.lower()
        assert "consent" in selector_str.lower()
        assert "gdpr" in selector_str.lower()
        assert "#CybotCookiebotDialog" in BANNER_SELECTORS
        assert "#onetrust-banner-sdk" in BANNER_SELECTORS

    def test_has_cmp_selectors(self):
        """Verify known CMP selectors are included."""
        assert ".cc-banner" in BANNER_SELECTORS
        assert ".sp-message-container" in BANNER_SELECTORS


class TestFindBannerElement:
    @pytest.mark.asyncio
    async def test_finds_visible_banner(self, mock_page, mock_locator):
        """Banner element is returned when visible and large enough."""
        mock_page.locator = MagicMock(return_value=mock_locator)

        result = await _find_banner_element(mock_page)
        assert result is not None

    @pytest.mark.asyncio
    async def test_skips_small_elements(self, mock_page):
        """Elements below minimum size are ignored."""
        locator = AsyncMock()
        locator.count = AsyncMock(return_value=1)
        locator.nth = MagicMock(return_value=locator)
        locator.is_visible = AsyncMock(return_value=True)
        locator.bounding_box = AsyncMock(return_value={"height": 10, "width": 50, "x": 0, "y": 0})

        mock_page.locator = MagicMock(return_value=locator)

        result = await _find_banner_element(mock_page)
        assert result is None

    @pytest.mark.asyncio
    async def test_skips_hidden_elements(self, mock_page):
        """Hidden elements are skipped."""
        locator = AsyncMock()
        locator.count = AsyncMock(return_value=1)
        locator.nth = MagicMock(return_value=locator)
        locator.is_visible = AsyncMock(return_value=False)

        mock_page.locator = MagicMock(return_value=locator)

        result = await _find_banner_element(mock_page)
        assert result is None


class TestExtractButtons:
    @pytest.mark.asyncio
    async def test_extracts_button_text(self):
        """Extracts visible button text from a banner."""
        button = AsyncMock()
        button.is_visible = AsyncMock(return_value=True)
        button.inner_text = AsyncMock(return_value="Accept All")

        banner = AsyncMock()
        locator = AsyncMock()
        locator.count = AsyncMock(return_value=1)
        locator.nth = MagicMock(return_value=button)
        banner.locator = MagicMock(return_value=locator)

        buttons = await _extract_buttons(banner)
        assert "Accept All" in buttons

    @pytest.mark.asyncio
    async def test_deduplicates_buttons(self):
        """Duplicate button text is not repeated."""
        button = AsyncMock()
        button.is_visible = AsyncMock(return_value=True)
        button.inner_text = AsyncMock(return_value="Accept")

        banner = AsyncMock()
        locator = AsyncMock()
        locator.count = AsyncMock(return_value=2)
        locator.nth = MagicMock(return_value=button)
        banner.locator = MagicMock(return_value=locator)

        buttons = await _extract_buttons(banner)
        assert buttons.count("Accept") == 1
