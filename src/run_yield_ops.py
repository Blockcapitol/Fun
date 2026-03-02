from __future__ import annotations

from agents.yield_ops import DeFiYieldOpsAgent
from models import YieldOpportunity


def main() -> None:
    agent = DeFiYieldOpsAgent()
    opportunities = [
        YieldOpportunity(
            protocol="Aave",
            chain="base",
            apr=7.4,
            lockup_days=0,
            tvl_usd=25_000_000,
            smart_contract_risk_score=0.2,
        )
    ]

    shortlist = agent.shortlist(opportunities)
    if shortlist:
        print("YIELD RECOMMENDATION:", agent.build_recommendation(shortlist[0]))


if __name__ == "__main__":
    main()
