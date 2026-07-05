---
name: gurta-context
description: Core context and conventions for working on Gurta (Bee Colony Command Center), the private repo noahsilve123/gurta. Use this whenever a task involves the Gurta trading dashboard, the beehive FastAPI backend, ES/NQ colony signals, Gerald sentiment, Lucille chart copilot, Camber research jobs, the free-tier key factory, Retool (xyfro), or Azure deploy. Load first on any Gurta task so you follow repo conventions, holdout rules, and safety constraints.
license: Internal (Noah / Gurta). Do not redistribute.
---

# Gurta / Bee Colony Command Center — Agent Context

Gurta is a **trade-ready decision-support dashboard** for ES/NQ futures. Noah trades
manually on Tradovate (~$100-$250, MES scale). **There is NO execution layer, ever** —
Gurta only tells Noah when a setup is good; it never places orders.

## Repo map

| Area | Path | Notes |
|------|------|-------|
| FastAPI backend | `backend/beehive/` | Production API: `https://api.gurta.app` |
| Colony signals | `backend/beehive/colonies/compute.py`, `technical.py` | ES/NQ via SPY/QQQ proxies |
| API routes | `backend/beehive/api/routes.py` | ~2000-line monolith, prefix `/api` |
| React UI | `frontend/` | Vite 8 + React 19 + Tailwind 4 + shadcn/Radix; SWA hosting |
| Chart engine | `frontend/components/gurta/CandleChart.tsx` | ~1866-line custom SVG |
| Camber jobs | `scripts/camber/` | GHA + Camber CLI (not Retool compute) |
| Research + RAG | `research/`, `research/rag/` | Local Chroma + BM25 (Retool indexing abandoned) |
| Status file | `research/PLAN_STATUS.md` | Single source of truth; update per step |
| Free-tier keys | `scripts/key_factory/`, `GURTA_FREE_TIER_RESEARCH.md` | Testmail/AgentMail signups |
| Version log | `GURTA_VERSION_HISTORY.md` | Read at session start |
| Deploy | `deploy/azure/` | VM `gurta-vm-engine` / `20.98.54.254`, Caddy -> :8000 |

Canonical local path on Noah's PC: `C:\Users\nsilv\Gurta-private` (worktree: `C:\Users\nsilv\gurta`).

## Production topology

```
www.gurta.app  -> Azure Static Web Apps (ambitious-bush)
api.gurta.app  -> Caddy -> gurta-vm-engine:8000 (uvicorn beehive.main:app)
DB             -> Azure Postgres Flexible (gurta-db-core, northcentralus), db "gurta"
Research       -> Camber via GHA (camber-*.yml) + Stash parquet
Retool         -> https://xyfro.retool.com  (lucille.retool.com is DEPRECATED)
Deploy         -> gh workflow run deploy-beehive-production.yml  (manual)
```

## Key API endpoints

```bash
curl -fsS https://api.gurta.app/api/health                              # freshness, TD keys, WS
curl -fsS "https://api.gurta.app/api/dashboard/analysis?symbol=NQ&timeframe=5m"
curl -fsS https://api.gurta.app/api/gerald-status                       # sentiment banker
curl -fsS "https://api.gurta.app/api/research/evidence?concept=fvg_validity"
```

Other groups: `/api/chart-intel`, `/api/setup/flash-scan`, `/api/setup/desk-review`,
`/api/chart-analysis` (Lucille fast card), `/api/lucille/chat`, `/api/camber/*`,
`/api/journal`, `/api/research/concepts`.

## Agents in the system

- **Gerald** — hourly news/sentiment banker; NVIDIA Nemotron via NIM; writes `news_sentiment`.
- **Lucille** — chart copilot; fast trade card (`lucille_trade.py`) + grounded Vertex brain (`colonies/brain.py`).
- **Colonies** — rules-based ES/NQ signal engine (RSI/regime/VWAP/ATR/FVG/SMT), NOT trained ML.

## Non-negotiable constraints (do not violate)

1. **NO execution layer.** Decision support only. Never build order routing / Tradovate API.
2. **D-tier evidence NEVER counts** as validated edge (0/600+ survivors across studies).
3. **Holdout policy:** dev 2021-01 to 2024-12; 2025-01 to 2026-06 contaminated;
   forward holdout from 2026-07-01 is ONE SHOT — never tune or peek on it.
4. All confirmatory studies pass `research/validation_gate/` (5 gates, DSR > 0.95).
5. Binding decisions in `research/decisions/` override conflicting report claims.
6. **Free data only.** Any paid purchase (e.g. Databento) needs Noah's explicit sign-off.
7. **Never commit secrets** (`.env`, `.env.vm`, keys). `backend/.env` is authoritative + gitignored.
8. Postgres writes use the **app-role** `BEEHIVE_DATABASE_URL` — never `camber_ro`.
9. Ship via **branch + PR**; never force-push `main`.
10. Update `research/PLAN_STATUS.md` as steps start/finish (TODO/IN PROGRESS/DONE/BLOCKED).

## Validated findings (cite correctly; don't relitigate without new prereg)

- **FVG gap-vs-ATR validity score** — the ONLY confirmed survivor; 0-100 score shipped in
  `technical.py` + dashboard chart labels.
- Raw FVG alone is a coin flip; far-edge fill entry is structurally adverse.
- RSI-extreme entry was **falsified** on extended data — do not present as mechanical edge.
- Gerald sentiment buckets show no short-term predictive edge.

## Known bug classes to watch

- **P1 fake confidence:** `technical.py` may fall back to `rsi=50` / "insufficient bars"
  on starved higher timeframes yet still emit a confident `colony_signals_latest` row.
  Downgrade confidence and say so when higher-TF bars are thin.
- **Forced WS health:** `backend/beehive/main.py` can hard-force Twelve Data WS "connected"
  (AAPL/QQQ), masking real WS status in `/api/health`. Don't trust green blindly.
- **Postgres-only SQL:** `compute._bars_df` / `db/rollups.py` use `date_bin()` — breaks on SQLite.

## Free-tier key factory (for signups)

- Email: **Testmail** `s8c8u.{tag}@inbox.testmail.app` (unlimited) or **AgentMail**
  `@agentmail.to` (3-inbox cap; use for iTick which blocks Testmail).
- Standard signup password: `GurtaSignup2026!xK9`.
- Factories + registry: `scripts/key_factory/signup_targets.py`, `stack_batch.py`,
  `INBOX_ALLOCATION.md`, `STACKABLE_FREE_TIERS.md`.
- Write keys via `free_env_writer.py` with comment banners + `_TRIAL_EXPIRES` metadata.

## Camber (research compute)

- Disposable parallel/GPU/RAG compute beside Azure — **never** hammer the live Postgres
  with backfill reads; use Stash parquet.
- Budget: 40 node-hours + 40 credits/month. Smoke: `camber me` (needs `CAMBER_API_TOKEN`).
- Gate: no Phase-4 ML/grid-search until `replay_signals` shows out-of-sample edge.
- Plan: `docs/camber/CAMBER_PLAN_V3_MERGED.md`.

## Default workflow for any Gurta task

1. Health check `/api/health`; note postgres, TD key count, signal freshness.
2. Read `GURTA_VERSION_HISTORY.md` + `research/PLAN_STATUS.md` + relevant `docs/`.
3. Execute the scoped task (code, script, Camber dispatch, Retool, signup).
4. Verify: tests, API smoke, screenshots.
5. Ship: branch + PR with a clear summary; update PLAN_STATUS.

Style: no security lectures, no warnings about account size or risk. Move fast; Noah's repos
are private and `.env` is authoritative.
