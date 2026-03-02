from __future__ import annotations

from dataclasses import dataclass

from models import Alert, Severity, Signal


@dataclass(slots=True)
class AlphaScoringConfig:
    whale_threshold_usd: float = 500_000
    lp_pull_threshold_pct: float = 0.2
    high_confidence_cutoff: float = 0.8


class AlphaAlertsAgent:
    """Ingests project signals, scores severity, and emits explainable alerts."""

    def __init__(self, config: AlphaScoringConfig | None = None) -> None:
        self.config = config or AlphaScoringConfig()

    def evaluate_signal(self, signal: Signal) -> Alert | None:
        severity = self._severity(signal)
        if severity is None:
            return None

        confidence = self._confidence(signal, severity)
        headline = f"{signal.project}: {signal.signal_type.replace('_', ' ').title()}"
        summary = (
            f"Detected {signal.signal_type} on {signal.chain} with value={signal.value}."
        )
        impact = self._impact_text(signal, severity)

        return Alert(
            headline=headline,
            summary=summary,
            impact=impact,
            confidence=confidence,
            severity=severity,
            sources=signal.metadata.get("sources", []),
            suggested_watch=signal.metadata.get("suggested_watch", []),
            signal=signal,
        )

    def _severity(self, signal: Signal) -> Severity | None:
        if signal.signal_type == "whale_transfer":
            if signal.value >= self.config.whale_threshold_usd * 2:
                return Severity.CRITICAL
            if signal.value >= self.config.whale_threshold_usd:
                return Severity.HIGH
            return None

        if signal.signal_type == "lp_pull":
            pct = signal.metadata.get("liquidity_change_pct", 0)
            if pct <= -2 * self.config.lp_pull_threshold_pct:
                return Severity.CRITICAL
            if pct <= -self.config.lp_pull_threshold_pct:
                return Severity.HIGH
            return None

        if signal.signal_type in {"governance_passed", "contract_upgrade"}:
            return Severity.MEDIUM

        if signal.signal_type in {"token_unlock_upcoming", "github_release"}:
            return Severity.LOW

        return None

    def _confidence(self, signal: Signal, severity: Severity) -> float:
        source_count = len(signal.metadata.get("sources", []))
        verified = 1.0 if signal.metadata.get("verified", False) else 0.7
        base = 0.55 + min(source_count, 3) * 0.1
        boost = 0.1 if severity in {Severity.HIGH, Severity.CRITICAL} else 0.0
        return min(1.0, base * verified + boost)

    def _impact_text(self, signal: Signal, severity: Severity) -> str:
        if severity in {Severity.HIGH, Severity.CRITICAL}:
            return "Potential near-term volatility. Verify treasury and liquidity context before acting."
        return "Track this event for context; immediate market impact is likely limited."
