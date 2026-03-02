from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class Signal:
    signal_type: str
    project: str
    chain: str
    value: float
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class Alert:
    headline: str
    summary: str
    impact: str
    confidence: float
    severity: Severity
    sources: list[str]
    suggested_watch: list[str]
    signal: Signal


@dataclass(slots=True)
class Opportunity:
    title: str
    source: str
    deadline: datetime
    payout_usd: int
    tags: list[str]


@dataclass(slots=True)
class YieldOpportunity:
    protocol: str
    chain: str
    apr: float
    lockup_days: int
    tvl_usd: float
    smart_contract_risk_score: float
