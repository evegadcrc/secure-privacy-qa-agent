import pytest

from src.flow_tester import _classify_button, _find_button_for_action


class TestClassifyButton:
    def test_accept_buttons(self):
        assert _classify_button("Accept All") == "accept"
        assert _classify_button("Accept") == "accept"
        assert _classify_button("Allow All Cookies") == "accept"
        assert _classify_button("I Agree") == "accept"
        assert _classify_button("Got it") == "accept"

    def test_reject_buttons(self):
        assert _classify_button("Reject All") == "reject"
        assert _classify_button("Decline") == "reject"
        assert _classify_button("No Thanks") == "reject"
        assert _classify_button("Deny") == "reject"

    def test_manage_buttons(self):
        assert _classify_button("Manage Preferences") == "manage"
        assert _classify_button("Cookie Settings") == "manage"
        assert _classify_button("Customize") == "manage"
        assert _classify_button("More Options") == "manage"

    def test_close_buttons(self):
        assert _classify_button("Close") == "close"
        assert _classify_button("×") == "close"
        assert _classify_button("Dismiss") == "close"

    def test_ok_button(self):
        assert _classify_button("Okay") == "accept"
        assert _classify_button("Yes") == "accept"

    def test_unknown_buttons(self):
        assert _classify_button("Learn More") is None
        assert _classify_button("Privacy Policy") is None


class TestFindButtonForAction:
    def test_finds_accept(self):
        buttons = ["Manage Preferences", "Accept All", "Reject All"]
        assert _find_button_for_action(buttons, "accept") == "Accept All"

    def test_finds_reject(self):
        buttons = ["Accept", "Reject All"]
        assert _find_button_for_action(buttons, "reject") == "Reject All"

    def test_returns_none_when_not_found(self):
        buttons = ["Accept All"]
        assert _find_button_for_action(buttons, "reject") is None

    def test_empty_buttons(self):
        assert _find_button_for_action([], "accept") is None
