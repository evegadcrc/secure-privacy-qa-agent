from pydantic import BaseModel
from enum import Enum


class Status(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


class Severity(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class Finding(BaseModel):
    criterion: str
    status: Status
    detail: str
    severity: Severity | None = None
    framework: str | None = None  # e.g. "GDPR", "WCAG", "CNIL"
    rule_id: str | None = None    # e.g. "GDPR-001", "WCAG-005"


class BannerDetection(BaseModel):
    banner_found: bool
    text: str | None = None
    buttons: list[str] = []
    screenshot_path: str | None = None
    html: str | None = None


class CookieInfo(BaseModel):
    name: str
    domain: str
    category: str  # necessary, analytics, marketing, unknown
    secure: bool
    http_only: bool


class CookieAudit(BaseModel):
    cookies_before_consent: list[CookieInfo] = []
    cookies_after_accept: list[CookieInfo] = []
    cookies_after_reject: list[CookieInfo] = []
    violations: list[str] = []


class FlowTestResult(BaseModel):
    action: str  # accept, reject, close, manage
    banner_dismissed: bool
    tracking_cookies_set: bool
    screenshot_path: str | None = None
    passed: bool


class ComplianceReport(BaseModel):
    url: str
    overall_score: str  # pass, partial, fail
    findings: list[Finding] = []
    cookie_audit: CookieAudit
    flow_results: list[FlowTestResult] = []
    summary: str
    recommendations: list[str] = []
