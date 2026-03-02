from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from models import Opportunity


@dataclass(slots=True)
class TeamProfile:
    name: str
    skills: list[str]
    chains: list[str]
    portfolio_links: list[str]


class GrantBountyHunterAgent:
    """Matches teams to grants and generates structured application drafts."""

    def match(self, profile: TeamProfile, opportunities: list[Opportunity]) -> list[Opportunity]:
        now = datetime.now(timezone.utc)
        scored: list[tuple[int, Opportunity]] = []

        for item in opportunities:
            if item.deadline < now:
                continue

            score = 0
            for skill in profile.skills:
                if skill.lower() in {tag.lower() for tag in item.tags}:
                    score += 2
            for chain in profile.chains:
                if chain.lower() in {tag.lower() for tag in item.tags}:
                    score += 1
            if item.payout_usd >= 10_000:
                score += 2

            scored.append((score, item))

        scored.sort(key=lambda row: (row[0], row[1].payout_usd), reverse=True)
        return [item for score, item in scored if score > 0]

    def application_draft(self, profile: TeamProfile, opportunity: Opportunity) -> dict[str, str]:
        return {
            "title": f"{profile.name} x {opportunity.title}",
            "problem": "Current ecosystem users need better tooling, onboarding, and measurable outcomes.",
            "proposal": (
                f"We will deliver a milestone-based project aligned with {', '.join(opportunity.tags)} "
                "and publish progress updates weekly."
            ),
            "execution_plan": "Week 1 discovery, Week 2 implementation, Week 3 testing, Week 4 launch.",
            "proof_of_work": "; ".join(profile.portfolio_links),
            "budget": f"Requested budget: ${opportunity.payout_usd:,}",
        }
