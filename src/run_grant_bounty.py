from __future__ import annotations

from datetime import datetime, timedelta, timezone

from agents.grant_bounty import GrantBountyHunterAgent, TeamProfile
from models import Opportunity


def main() -> None:
    agent = GrantBountyHunterAgent()
    profile = TeamProfile(
        name="BuilderDAO",
        skills=["python", "data", "ai"],
        chains=["base", "arbitrum"],
        portfolio_links=["https://github.com/builderdao/alpha-agent"],
    )
    opportunities = [
        Opportunity(
            title="Arbitrum Analytics Bounty",
            source="QuestBook",
            deadline=datetime.now(timezone.utc) + timedelta(days=15),
            payout_usd=12_000,
            tags=["arbitrum", "ai", "data"],
        )
    ]

    matches = agent.match(profile, opportunities)
    if matches:
        print("GRANT DRAFT:", agent.application_draft(profile, matches[0]))


if __name__ == "__main__":
    main()
