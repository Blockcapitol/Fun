# Web3 Revenue Agent Pack

This repository contains **three practical Web3 AI agents** focused on legitimate and sustainable revenue workflows:

1. **Alpha Research + Alerts Agent** (subscription-ready signal engine)
2. **Grant + Bounty Hunter Agent** (opportunity matching + application drafting)
3. **DeFi Yield Ops Agent** (non-custodial yield recommendations with explicit confirmation guardrails)

## What is implemented

### 1) Alpha Alerts Agent
- Ingest-ready `Signal` model for events such as whale transfers, LP pulls, governance events, unlock notices, and releases.
- Rule-based severity scoring (`low` → `critical`).
- Confidence scoring using source count + verification metadata.
- Explainable `Alert` output suitable for Telegram/Discord delivery.

### 2) Grant + Bounty Hunter Agent
- Team profile modeling for skills, chain focus, and portfolio.
- Grant/bounty ranking logic (fit score + payout weighting + deadline filtering).
- Structured application draft generator for rapid submissions.

### 3) DeFi Yield Ops Agent
- Policy constraints for lockup, TVL, and smart contract risk.
- Opportunity shortlist and ranking.
- Recommendations that enforce **manual transaction confirmation** (no auto-signing).

## Project structure

- `src/models.py` — shared domain models.
- `src/agents/alpha_alerts.py` — Alpha agent implementation.
- `src/agents/grant_bounty.py` — Grant/Bounty agent implementation.
- `src/agents/yield_ops.py` — Yield Ops implementation.
- `src/run_alpha.py` — Alpha bot entrypoint.
- `src/run_grant_bounty.py` — Grant/Bounty bot entrypoint.
- `src/run_yield_ops.py` — Yield Ops bot entrypoint.
- `src/main.py` — combined demo runner.
- `tests/test_agents.py` — unit tests for all three agents.

## Run locally

```bash
pytest
python src/main.py
```

## Docker usage (each bot is dockerized)

### Build images individually

```bash
docker build -f Dockerfile.alpha -t web3-agents/alpha-alerts:latest .
docker build -f Dockerfile.grant_bounty -t web3-agents/grant-bounty:latest .
docker build -f Dockerfile.yield_ops -t web3-agents/yield-ops:latest .
```

### Run each bot individually

```bash
docker run --rm web3-agents/alpha-alerts:latest
docker run --rm web3-agents/grant-bounty:latest
docker run --rm web3-agents/yield-ops:latest
```

### Build/run all with docker compose

```bash
docker compose build
docker compose up
```

## Next steps to production

- Add real collectors (RPC/indexers, governance feeds, GitHub releases, treasury trackers).
- Add persistent storage for alerts/opportunity state.
- Add delivery connectors (Telegram bot, Discord webhook, email).
- Add billing + entitlements (Stripe + feature gates).
- Add observability and SLOs for latency and false-positive rate.
