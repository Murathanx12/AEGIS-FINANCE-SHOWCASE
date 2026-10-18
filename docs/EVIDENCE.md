# Aegis public showcase evidence, checked 18 October 2026

This packet is a selective public-safe derivative of a read-only local audit. It is not a production health check or investment certification. The Aegis runtime checkout is dirty and was not altered. Do not copy the original repository, runtime ledgers or raw receipts into the showcase.

## Verified development scale

- Local HEAD: `4e19219900c9de9fa35315fec63478783b6af3b5`, dated 9 October 2026.
- Reachable commits at HEAD: **1,990**, not more than 2,000. Earliest reachable commit: **28 March 2026**. More than six months of project history is supported. This checkout does not establish how many hours were spent or who authored each line.
- Tracked files at HEAD: **8,765**. This includes documentation and data; do not present it as a source-file count.
- Bounded production-source census: **1,180 files; 520,585 physical lines; 458,663 nonblank lines**. This measures source-tree scale, not originality, quality, developer productivity or independently reviewed code.
- Census roots: `backend/`, `engine/`, `frontend/src/`, `scripts/`, `tools/`, `nn_lab/`. Extensions: `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.sql`. Exclude paths containing `/tests/`, `/test_`, `/data/`, `/node_modules/`, `/.next/`, `/vendor/`, `/generated/`, and `.test.ts`, `.test.tsx`, `.spec.ts`, `.spec.tsx` suffixes. Count HEAD blobs, not dirty working-tree content. Python:489,532 lines; TSX:23,836; TS:7,053; CSS:164. These exclusions are path-based and do not certify that no generated code remains.

Reproduce commit metrics with `git rev-list --count HEAD`, `git log --reverse --format=%cs`, `git log -1 --format=%H`, and `git ls-tree -r --name-only HEAD`. For the source census, apply the rules above to that final path list and read `HEAD:<path>` blobs through `git cat-file --batch`; physical lines are `len(blob.decode('utf-8','replace').splitlines())`, nonblank lines retain `line.strip()`.

## Strong public positioning

**Aegis is a work-in-progress investment research platform that turns market information into recorded hypotheses, paper decisions and measurable outcomes.** Its strongest demonstrable portfolio story is engineering: collection, provenance, deterministic portfolio mechanics, forecast grading, persistent research memory and visible failures. Do not claim a successful finance model, market-beating skill, fully autonomous production quality, or a certified completed Beta.

Code and documentation support this architectural description:

1. Sensors and collection: news, analyst revisions, official/public information and browser research (`scripts/news_pull.py`, `backend/services/web_reader.py`, `scripts/pull_analyst_targets.py`).
2. Evidence and hypotheses: stored source references, world-state beliefs, theory cells and explanatory model output (`world_digest.py`, `world_state.py`, `scripts/hyp_theory_cells.py`).
3. Deterministic decisions: explicit contracts, ranking, sizing and risk constraints (`decision_contract.py`, `opportunity_funnel.py`, `scripts/sim_run.py`).
4. Paper execution and outcomes: paper sessions, frozen forecast ledgers and grading (`sim_session.py`, `forecast_ledger.py`, `forecast_grader.py`).
5. Review and memory: account comparison, regret attribution and persistent process knowledge (`book_dna.py`, `regret_ledger.py`, Optimus integration).

These are implemented components and design responsibilities, not a claim that every scheduled connection is currently qualified. Observed source rows do not prove that a model read every article. A data catalogue is not a proprietary corpus that can automatically be sold: publisher rights and licences remain separate.

## Current sanitized result packet

Use sibling `SHOWCASE_SNAPSHOT.json`. It explicitly allowlists five endpoint observations and small cohort aggregates from the latest available local receipt. It removes account numbers, holdings, cash balances, private environment references and raw bodies.

- Source generated: **17 October 2026 23:51:19 UTC**. Latest market mark: **16 October 2026**. These are dated snapshots, not a live feed.
- 367 attempted accounts; 362 priced. **307 have an own-window SPY comparison:20 ahead,287 behind.** Excluding control twins: **5 ahead,75 behind**. The 20 ahead include15 twins and5 strategy books, corresponding to about1.5 ex-ante effective bets under the project's estimate.
- Examples were chosen after observing results; include losses and cohort denominator next to any plot. Accounts have different inception windows and cannot be added together as one portfolio.

| Paper sleeve | Window start | Last mark | Return | Own-window SPY | Difference |
|---|---|---|---:|---:|---:|
| conservative-atr | 2026-06-17 | 2026-10-16 | +6.222% | +3.530% | +2.692pp |
| aggressive | 2026-06-08 | 2026-10-16 | +4.941% | +3.774% | +1.167pp |
| revision_flow_v0 | 2026-09-28 | 2026-10-16 | +0.008% | -0.664% | +0.672pp |
| hack2 | 2026-08-28 | 2026-10-16 | -4.177% | -0.772% | -3.405pp |
| mirror | 2026-06-16 | 2026-10-16 | -30.792% | +2.237% | -33.029pp |

**Paper only; not independently audited or evidence of investment skill.** No maximum drawdown is present in this endpoint receipt; leave it unknown rather than derive it from endpoints. No claim of cost-inclusive executable outperformance is established here. Internal `EARLY_EVIDENCE` is a sign-test label with documented substantial null pass rates, not independent validation. Project policy requires24 months before any skill claim. Free-data historical backtests are direction checks; CRSP-grade historical work remains historical, with no demonstrated general alpha in the checked public narrative.

Exact private source paths and hashes for audit, without copying source files:

- `backend/data/optimus/paper_accounts/roi_2026-10-17T235119Z.json`: SHA256 `00cd9c60f0d4622633fcd7820217b586c5f39ee72d823061e716db1634abc551`.
- `backend/data/optimus/paper_accounts/book_dna_2026-10-17T235119Z.json`: SHA256 `97b5f506f50e0123a1823c484284f59f986a56ae5846f7f4beba490a1ce9e8f7`.

To reproduce the sanitized extract: parse those JSON files with Python stdlib, index ROI `rows` and DNA `books` by `account`, select the five named accounts above, and copy only the keys represented in `SHOWCASE_SNAPSHOT.json`. Recompute each source SHA256 from original bytes. Compare aggregate `n_ahead_of_spy`, `n_behind_spy`, `n_ahead_twins`, `n_ahead_strategy` and `effective_bets_exante`. The same-window benchmark and entry convention differ by account and are retained in the sanitized rows. ROI equals `(equity/start_capital-1)*100`; use supplied three-decimal receipt rounding.

The existing `paper_results_live.svg` is pinned to6 October and materially stale: it shows revision_flow+7.139% and hack2+2.307%. **Do not publish it as current.** A new static endpoint comparison from the sanitized JSON is appropriate; a line plot would falsely imply time-series evidence unless separately supplied.

## Explicit copy allowlist

These original already-public identity assets contain schematic module paths rather than private datasets. They are MIT licensed under the source repository's `LICENSE` (Copyright2026 Murathanx12). Retain the licence and describe them as architecture illustrations for a work in progress, not scheduled qualification evidence.

| Source | SHA256 | Suitable use |
|---|---|---|
| `docs/assets/aegis_loop.svg` | `e44b8b479768c69e38ea758f8d029406e68d93fbcdff6c1aec46e82eeb645c4b` | animated overview |
| `docs/assets/architecture_pipeline.svg` | `7f1df0c8627a3a3ef53f09ce89e65fe47649b3951e1db2203dde84851e07f2dd` | implementation map |
| `docs/assets/gauntlet.svg` | `d692208c963d20fde8bff5cc6161094bb6d1faa708c8fe5cddcefffdcd0b4753` | research process |
| `docs/assets/og_preview.svg` | `9d0d7c2eb0a41b374a29e2f321ebe4371ba5973b62dc2d9e558b14ddcd507b1c` | preview source |
| `LICENSE` | MIT text | attribution |

The curated `SHOWCASE_SNAPSHOT.json` and newly authored sanitized documentation/graphics are suitable publication candidates. Do not copy the original README verbatim: its public result badges and headline results are old. Do not copy raw funding packs, entire receipts, `.env`, account metadata, holdings ledgers, local paths, private papers, portal adverts/documents, browser state, personal correspondence, or full Optimus/chat history. Avoid copying `docs/design/aegis_front_page.html`, because it embeds the old results.

## Verification boundary

Checked local Git objects, read-only files and exact receipt fields. Did not run finance tasks, recompute NAV, call brokers, inspect credentials, restart services, alter production, certify current deployments or rerun the whole finance test suite. Local `frontend/package.json` currently names Next16.2.1/React19.2.4; old orientation prose says Next14 and should not be copied. Documentation receipt dates do not substitute for new live deployment checks.
