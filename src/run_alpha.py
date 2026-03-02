from __future__ import annotations

from agents.alpha_alerts import AlphaAlertsAgent
from models import Signal


def main() -> None:
    agent = AlphaAlertsAgent()
    signal = Signal(
        signal_type="whale_transfer",
        project="ProjectX",
        chain="arbitrum",
        value=1_200_000,
        metadata={
            "verified": True,
            "sources": [
                "https://explorer.example/tx/0xabc",
                "https://x.com/projectx/status/1",
            ],
            "suggested_watch": ["CEX netflows", "related wallet cluster"],
        },
    )
    alert = agent.evaluate_signal(signal)
    if alert:
        print("ALPHA ALERT:", alert)


if __name__ == "__main__":
    main()
