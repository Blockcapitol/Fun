from __future__ import annotations

from dataclasses import dataclass

from models import YieldOpportunity


@dataclass(slots=True)
class YieldPolicy:
    max_lockup_days: int = 30
    min_tvl_usd: float = 2_000_000
    max_risk_score: float = 0.35


class DeFiYieldOpsAgent:
    """Ranks non-custodial yield opportunities and enforces explicit-confirmation execution."""

    def __init__(self, policy: YieldPolicy | None = None) -> None:
        self.policy = policy or YieldPolicy()

    def shortlist(self, opportunities: list[YieldOpportunity]) -> list[YieldOpportunity]:
        accepted = [x for x in opportunities if self._eligible(x)]
        return sorted(accepted, key=self._rank_score, reverse=True)

    def build_recommendation(self, opportunity: YieldOpportunity) -> dict[str, str | float]:
        return {
            "protocol": opportunity.protocol,
            "chain": opportunity.chain,
            "apr": opportunity.apr,
            "risk_summary": (
                f"Risk score={opportunity.smart_contract_risk_score:.2f}, "
                f"TVL=${opportunity.tvl_usd:,.0f}, lockup={opportunity.lockup_days}d"
            ),
            "execution_mode": "manual_confirmation_required",
            "note": "No transaction should be signed automatically.",
        }

    def _eligible(self, opportunity: YieldOpportunity) -> bool:
        return (
            opportunity.lockup_days <= self.policy.max_lockup_days
            and opportunity.tvl_usd >= self.policy.min_tvl_usd
            and opportunity.smart_contract_risk_score <= self.policy.max_risk_score
        )

    def _rank_score(self, opportunity: YieldOpportunity) -> float:
        risk_penalty = 1 - opportunity.smart_contract_risk_score
        lockup_penalty = max(0.2, 1 - (opportunity.lockup_days / 120))
        liquidity_bonus = min(2.0, opportunity.tvl_usd / 10_000_000)
        return opportunity.apr * risk_penalty * lockup_penalty * liquidity_bonus
