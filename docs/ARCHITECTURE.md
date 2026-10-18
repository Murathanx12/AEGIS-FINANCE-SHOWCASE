# The research system

Aegis connects information acquisition, explicit hypotheses, quantitative decisions and measured outcomes. The model interprets; the engine computes. The stages form a loop because the outcome of one experiment should inform the next one.

## Source to decision

Source collection includes news, official/public information and analyst revisions. Source records retain provenance and processing state. World-state and theory components represent beliefs, scenarios, causal mechanisms and falsifiers. Forecast ledgers retain the original forecast and horizon before outcomes are observed.

Deterministic decision contracts separate direction and magnitude, rank opportunities and apply sizing/risk constraints. Paper execution records actions and holds. Outcome grading, benchmark comparisons and regret attribution test what happened afterward. Reviewed findings and explicit policy state can inform a subsequent experiment.

## Implementation map

| Responsibility | Representative implementation modules |
| --- | --- |
| Acquisition | `news_pull.py`, `web_reader.py`, `pull_analyst_targets.py` |
| Evidence | `world_digest.py`, `data_catalog.py`, `analyst_reputation.py` |
| Theory | `world_state.py`, `hyp_theory_cells.py` |
| Forecasts | `belief_state.py`, `forecast_ledger.py`, `nn_lab/nightly.py` |
| Decisions | `opportunity_funnel.py`, `decision_contract.py`, `sim_run.py` |
| Paper action | `sim_session.py`, `pc_broker.py` |
| Outcome | `daily_pass.py`, `forecast_grader.py` |
| Attribution | `book_dna.py`, `regret_ledger.py`, `decision_story.py` |
| Learning | `policy_state.py`, `hyp_lab.py`, `expected_return.py` |

The public renderer's original stage table contains the full relative paths. They were inspected in the private implementation; the public showcase does not contain or execute those financial modules.

## Interface and memory

The interface uses Next.js/React; the API and research routines use Python/FastAPI and project-specific quantitative components. The application frontend is a separate work-in-progress deployment, currently described by its owner as disconnected from its paused backend. This showcase makes no new service-health claim.

Optimus supplies selected project context and reusable guidance through retrieval/MCP. Its companion research worker uses a separate task ledger and original-document archive. Storing an article, reading its body, incorporating it in a forecast and demonstrating its contribution are different claims.

Architectural arrows describe responsibilities. They are not proof of every current scheduled connection, financial authorization or completed prospective validation.
