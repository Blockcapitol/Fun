from datetime import datetime, timedelta, timezone

from agents.alpha_alerts import AlphaAlertsAgent
from agents.grant_bounty import GrantBountyHunterAgent, TeamProfile
from agents.yield_ops import DeFiYieldOpsAgent
from models import Opportunity, Severity, Signal, YieldOpportunity


def test_alpha_alerts_high_severity_whale() -> None:
    agent = AlphaAlertsAgent()
    signal = Signal(
        signal_type="whale_transfer",
        project="TokenA",
        chain="eth",
        value=600_000,
        metadata={"verified": True, "sources": ["s1", "s2"]},
    )

    alert = agent.evaluate_signal(signal)

    assert alert is not None
    assert alert.severity == Severity.HIGH
    assert alert.confidence > 0.7


def test_grant_matching_prefers_relevance_and_payout() -> None:
    agent = GrantBountyHunterAgent()
    profile = TeamProfile(
        name="ShipFast",
        skills=["ai", "python"],
        chains=["base"],
        portfolio_links=["https://example.com"],
    )
    opportunities = [
        Opportunity(
            title="Small bounty",
            source="B",
            deadline=datetime.now(timezone.utc) + timedelta(days=7),
            payout_usd=1_000,
            tags=["base", "python"],
        ),
        Opportunity(
            title="Big bounty",
            source="B",
            deadline=datetime.now(timezone.utc) + timedelta(days=7),
            payout_usd=15_000,
            tags=["base", "python", "ai"],
        ),
    ]

    matches = agent.match(profile, opportunities)

    assert matches[0].title == "Big bounty"


def test_yield_shortlist_enforces_policy() -> None:
    agent = DeFiYieldOpsAgent()
    opportunities = [
        YieldOpportunity("SafePool", "eth", 5.0, 7, 5_000_000, 0.2),
        YieldOpportunity("RiskyPool", "eth", 25.0, 90, 400_000, 0.8),
    ]

    shortlist = agent.shortlist(opportunities)

    assert len(shortlist) == 1
    assert shortlist[0].protocol == "SafePool"
