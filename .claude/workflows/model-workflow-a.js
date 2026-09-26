export const meta = {
  name: 'model-workflow-a',
  description: 'Workflow A (assessment) from an approved question doc: optional src/ implementation + fidelity review, notebook, two-pass review with capped fix cycles — the main model is never modified',
  phases: [
    { title: 'Findings' },
    { title: 'Implement (if needed)' },
    { title: 'Review: Implementation', detail: 'Sonnet — src/ matches the question doc' },
    { title: 'Notebook' },
    { title: 'Review: Adversarial', detail: 'Opus — critiques the theory' },
    { title: 'Fix' },
    { title: 'Review: Verification', detail: 'Sonnet — reproduces the arithmetic, checks .qmd leak' },
    { title: 'Doc-sync', detail: 'Sonnet — one batched pass for stale copies, no re-review' },
    { title: 'Re-tier', detail: 'Re-collect open findings for the main agent to re-tier' },
  ],
}

// Encodes the model-workflow skill's "Workflow A — Assessment" from the
// optional src/ implementation pass onward. Steps 1 (librarian, if needed) and
// 2 (the question doc, plus the main agent's read-and-approve checkpoint) stay
// OUTSIDE this script, same reasoning as model-workflow-b.js: picking the
// thread folder and writing the problem statement / verdict criterion is a
// judgment call, not a deterministic control-flow step. The final step (linking
// the challenge from the parent .qmd and updating challenges/README.md) is a
// documentation-index edit, not physics — it stays a plain main-agent edit
// after this workflow returns, not a modeler dispatch (Gate 2 does not apply:
// no physical quantity is being authored).
//
// Review coverage mirrors "@model-reviewer after every modeler pass"
// (agents-routing.md): the NOTEBOOK is the assessment's published deliverable,
// so it gets the full two-pass treatment (adversarial Opus, then verification
// Sonnet). The optional src/ implementation pass gets a single mechanical
// fidelity review (Sonnet) with its own small fix budget (POST_PASS_FIX_CAP).
//
// args = {
//   worktreePath: string,        // REQUIRED absolute path — caller must already
//                                // be inside this worktree (Gate 1)
//   model: string,               // e.g. 'fragmentation-field' — experiment/<model>/
//   thread: string,              // challenges/<thread>/
//   questionDocPath: string,     // the approved <question>.md (or a single
//                                // self-contained <question>.qmd — see below)
//   questionSlug: string,        // the .qmd this run writes/confirms, e.g. 'gravity'
//   needsSrcImplementation: bool,// true if the assessment needs physics not yet
//                                // in src/arty/ (skill step 3)
//   implementGoal: string,       // only read when needsSrcImplementation — what
//                                // src/arty/ must gain, per the question doc
//   findingsScopePaths: string[],// paths passed to collect-findings.py --for
// }

if (!args || !args.worktreePath) {
  throw new Error(
    'args.worktreePath is required — Gate 1 (agents-routing.md): the caller must already ' +
    'have entered this worktree (EnterWorktree) before invoking model-workflow-a.'
  )
}
if (!args.model || !args.thread || !args.questionDocPath || !args.questionSlug) {
  throw new Error('args.model, args.thread, args.questionDocPath and args.questionSlug are required.')
}
if (!Array.isArray(args.findingsScopePaths) || args.findingsScopePaths.length === 0) {
  throw new Error('args.findingsScopePaths must be a non-empty array (deferred-findings.md: inject the scope\'s open findings into every brief).')
}

const WT = args.worktreePath
const ANCHOR = `Working directory: ${WT} — anchor every Bash command and every Read/Edit/Write call to this absolute path, do not rely on an inherited cwd.`
const THREAD_DIR = `experiment/${args.model}/challenges/${args.thread}`
const NOTEBOOK = `${THREAD_DIR}/${args.questionSlug}.qmd`
const REVIEW = `${THREAD_DIR}/review.md`
const CHECKS = `${THREAD_DIR}/checks`

// Exact model pins, never aliases — see model-workflow-b.js (Sonnet 5.0
// refuses this project's subject matter; helpers would otherwise inherit).
const OPUS = 'claude-opus-5-5'
const SONNET = 'claude-sonnet-4-6'

// Standing clauses appended to briefs, one per rule file — same text as
// model-workflow-b.js (scripts must be self-contained, so it is duplicated).
const HARNESS = `Python only via "uv run" (never bare python/pip); nontrivial check code goes in a file under experiment/_scratch/ run with a single-line "uv run python <path>" — /tmp is not writable (subagent-harness.md).`
const STAGING = `Before this pass ends, resolve every script YOU put in experiment/_scratch/: one that produced a number now cited in a committed artifact is git mv'd to ${CHECKS}/ — named for what it checks, a docstring naming the document it feeds, runnable standalone from the repo root, cited by path from that document, under ~30 s (vectorise sweeps; no numpy scalar math in loops). An uncited dead end may be deleted. Never delete or move anyone else's staged files (verification-scripts.md).`
const FIDELITY = `Any number taken from a source table is read from its doc-reference/**/tables/*.csv (never hand-copied into a literal) and that table's .invariant must pass ("uv run src/utils/check-table-invariants.py <path>.invariant"); a table with no closure invariant is flagged in your return summary, not treated as admissible. Citation anchors are greppable strings you have grepped, never bare line numbers (source-data-fidelity.md).`
const DEFERRED = `A defect you notice outside this pass's scope gets a one-line marker next to what you found — FINDING[blocking|deferrable|note]: <what> (affects: <repo paths>; since: <YYYY-MM-DD>) — not only a mention in review.md. A committed artifact or shipped code known to carry a wrong number is blocking, never deferred by you; say so in your return summary (deferred-findings.md).`
const REVIEW_RULES = `Beyond arithmetic: criterion match (does cited data measure the same quantity the model computes? a mismatch is Blocking), and provenance (a claim attributed to a primary is checked against that primary, or must be marked secondhand in the citing artifact). A search returning nothing over an extraction or text layer bounds that surface only — read the page before calling anything fabricated or absent (source-data-fidelity.md). Do not re-raise a defect already listed under the known open findings — cite its marker instead.`
const TAGGING = `Tag every blocking and deferrable finding in your structured return (model-workflow skill, "Materiality gate"): kind = basis (different quantity / population / regime / criterion) | closure (a source table fails its own invariant) | numeric (a value off on a correct basis) | doc-sync (a stale or disagreeing copy of a value or verdict) | process; bound = within / crosses / conditional / unbounded, judged against the verdict criterion and Verdict outputs in ${args.questionDocPath} — "within" only if it holds under EVERY plausible reading and neither crosses a threshold nor flips a shipped direction, and "impact zero if reading X is right" is conditional, not within; applies_elsewhere = whether the cause reaches another setting, caliber, parameter range or consumer. Severity is still yours to assign; the tags decide what it costs.`

const ARTIFACT_SCHEMA = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    detail: { type: 'string' },
  },
  required: ['ok', 'detail'],
}

// "A quiet return ≠ success" (subagent-harness.md) — see model-workflow-b.js.
const DENIAL_RE = /permission (was )?denied|auto-denied|not (allowed|permitted) to run|requires approval|blocked by (the )?(harness|permission)/i

async function verifyModelerPass(stage, returned, expectation) {
  if (typeof returned === 'string' && DENIAL_RE.test(returned)) {
    return { stage, reason: 'modeler return carries permission-denial language — the pass likely did not complete (subagent-harness.md background-mode gotcha)', returned }
  }
  const check = await agent(
    `${ANCHOR}\nIndependently confirm on disk: ${expectation}. Use ls / wc -c / git status --short / git diff --stat — do not trust any agent's summary. Return ok=true only if the artifact is present and more than a heading-only stub; put what you actually saw in detail.`,
    { label: `verify-artifact:${stage}`, effort: 'low', model: SONNET, schema: ARTIFACT_SCHEMA }
  )
  if (check && check.ok) return null
  return {
    stage,
    reason: `expected artifact missing or stub on disk (${check ? check.detail : 'no check result'}). Classify before re-dispatching: tool_uses >= maxTurns with mostly Read/grep = over-read (re-dispatch fresh, narrower); real results but no write = productive exhaustion (one warm-cache SendMessage resume is permitted); neither = crash (subagent-harness.md)`,
    returned,
  }
}

// collect-findings.py --for takes ONE scope; extra positional paths are
// silently ignored (pre-commit filenames), so each scope is its own command.
function collectFindings(paths, label) {
  const cmds = paths.map((p) => `uv run python src/utils/collect-findings.py --for ${p}`).join('\n')
  return agent(
    `${ANCHOR}\nFrom the repo root, run each of these as its own separate Bash call (do not chain them):\n${cmds}\nReturn the stdouts verbatim, concatenated in order, with duplicate lines removed — nothing else.`,
    { label, effort: 'low', model: SONNET }
  )
}
const MAX_FIX_CYCLES = 2 // notebook review — shared across adversarial + verification (same cap as Workflow B)
const POST_PASS_FIX_CAP = 1 // src/ implementation verification — its own budget

// Materiality gate — same schemas and routing as model-workflow-b.js
// (model-workflow skill, "Materiality gate"; .claude/incidents.md#materiality).
const FINDING_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    severity: { type: 'string', enum: ['blocking', 'deferrable', 'note'] },
    kind: { type: 'string', enum: ['basis', 'closure', 'numeric', 'doc-sync', 'process'] },
    bound: { type: 'string', enum: ['within', 'crosses', 'conditional', 'unbounded'] },
    applies_elsewhere: { type: 'boolean' },
    summary: { type: 'string' },
  },
  required: ['id', 'severity', 'kind', 'bound', 'applies_elsewhere', 'summary'],
}

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'PASS-with-limitations', 'FAIL'] },
    blocking_count: { type: 'integer' },
    deferrable_count: { type: 'integer' },
    note_count: { type: 'integer' },
    findings: { type: 'array', items: FINDING_SCHEMA },
    summary: { type: 'string' },
    section_heading: { type: 'string' },
  },
  required: ['verdict', 'blocking_count', 'findings', 'summary', 'section_heading'],
}

const BOUND_SCHEMA = {
  type: 'object',
  properties: {
    bounds: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          bound: { type: 'string', enum: ['within', 'crosses', 'unbounded'] },
          evidence: { type: 'string' },
        },
        required: ['id', 'bound', 'evidence'],
      },
    },
  },
  required: ['bounds'],
}

function routeOf(f) {
  if (f.kind === 'basis' || f.kind === 'closure' || f.kind === 'process' || f.applies_elsewhere) return 'fix'
  if (f.kind === 'doc-sync') return 'doc-sync' // stays blocking until synced; human-approved 2026-09-25
  if (f.bound === 'crosses') return 'fix'
  if (f.bound === 'within') return 'note'
  return 'bound'
}

const WRITE_CHECK_SCHEMA = {
  type: 'object',
  properties: {
    found: { type: 'boolean' },
    heading_seen: { type: 'string' },
  },
  required: ['found'],
}

const DOC_SYNC = []

// See model-workflow-b.js triage(): returns the fix-routed findings.
async function triage(result, cfg, marker) {
  if (!result) return [{ id: 'no-result', kind: 'process', summary: 'review pass returned nothing' }]
  const blocking = (result.findings || []).filter((f) => f.severity === 'blocking')
  if (blocking.length === 0) {
    return result.verdict === 'FAIL' ? [{ id: 'untagged-fail', kind: 'process', summary: 'FAIL verdict with no tagged blocking finding' }] : []
  }
  const routed = blocking.map((f) => ({ f, route: routeOf(f) }))
  const toBound = routed.filter((r) => r.route === 'bound').map((r) => r.f)
  if (toBound.length > 0) {
    log(`Bounding ${toBound.length} finding(s) with conditional/unbounded impact before deciding on a fix cycle (${cfg.key}).`)
    const b = await agent(
      `${ANCHOR}\n\nBounding pass — not a review, not a fix. For each finding below from the "${marker}" section of ${REVIEW}, compute the largest change it could make to the verdict criterion / Verdict outputs declared in ${args.questionDocPath} (threshold and shipped-claim direction), under EVERY plausible reading — reuse src/arty/ functions by perturbing their inputs; do not investigate the cause. Return bound=within only if no reading crosses the threshold or flips a shipped direction; crosses if one does; unbounded if it cannot be computed cheaply. Append a dated section headed "Bounds — ${marker}" to ${REVIEW} with each margin and the check script that produced it.\n\nFindings:\n${toBound.map((f) => `- ${f.id}: ${f.summary}`).join('\n')}\n\n${HARNESS}\n${STAGING}`,
      { label: `bound:${cfg.key}`, phase: cfg.reviewPhase, agentType: 'model-reviewer', schema: BOUND_SCHEMA }
    )
    const byId = new Map(((b && b.bounds) || []).map((x) => [x.id, x.bound]))
    for (const r of routed) {
      if (r.route !== 'bound') continue
      r.route = byId.get(r.f.id) === 'within' ? 'note' : 'fix'
    }
  }
  for (const r of routed) if (r.route === 'doc-sync') DOC_SYNC.push({ stage: cfg.key, ...r.f })
  const noted = routed.filter((r) => r.route === 'note').map((r) => r.f.id)
  if (noted.length) log(`Bounded within the verdict threshold — note only, no fix cycle: ${noted.join(', ')}`)
  return routed.filter((r) => r.route === 'fix').map((r) => r.f)
}

async function verifyReviewWrite(marker) {
  const check = await agent(
    `${ANCHOR}\nRead ${REVIEW} and report whether it contains a section heading matching "${marker}". A background dispatch can silently drop a write — confirm the file on disk, don't assume. Return found=true/false and the closest heading you actually see.`,
    { label: 'verify-review-write', effort: 'low', model: SONNET, schema: WRITE_CHECK_SCHEMA }
  )
  return !!(check && check.found)
}

// One review stage = an initial review pass, a disk-write check, then a capped
// fix/re-review loop. `cyclesUsedIn`/`capCeiling` let the two notebook passes
// share one counter (ceiling MAX_FIX_CYCLES) while the src/ implementation pass
// runs its own (0..POST_PASS_FIX_CAP). Returns { result, cyclesUsed, escalate }.
async function reviewStage(cfg, cyclesUsedIn, capCeiling) {
  let cyclesUsed = cyclesUsedIn
  let marker = cfg.markerBase

  phase(cfg.reviewPhase)
  const o0 = { label: `reviewer:${cfg.key}`, phase: cfg.reviewPhase, agentType: 'model-reviewer', schema: REVIEW_SCHEMA }
  if (cfg.model) o0.model = cfg.model
  let result = await agent(`${cfg.initialBrief(marker)}\n\n${REVIEW_RULES}\n${TAGGING}\n${DEFERRED}\n${HARNESS}`, o0)
  if (!(await verifyReviewWrite(marker))) {
    return { result, cyclesUsed, escalate: { stage: cfg.key, reason: 'review.md write not found on disk', lastResult: result } }
  }
  let fixItems = await triage(result, cfg, marker)

  while (fixItems.length > 0 && cyclesUsed < capCeiling) {
    cyclesUsed++
    phase('Fix')
    log(`Fix cycle ${cyclesUsed} (${cfg.key}, cap ${capCeiling}) — ${fixItems.map((f) => f.id).join(', ')}.`)
    const scopeLine = `Address ONLY these fix-routed findings: ${fixItems.map((f) => `${f.id} (${f.summary})`).join('; ')}. Any other finding in that section is routed elsewhere (a note, or the end-of-run doc-sync batch) — leave it.`
    const fixReturn = await agent(`${cfg.fixBrief(marker, cyclesUsed)}\n${scopeLine}\n\n${HARNESS}\n${STAGING}\n${FIDELITY}\n${DEFERRED}`, { label: `modeler:fix-${cfg.key}-${cyclesUsed}`, phase: 'Fix', agentType: 'modeler' })
    const fixMiss = await verifyModelerPass(`fix-${cfg.key}-${cyclesUsed}`, fixReturn, `git diff --stat shows edits addressing the "${marker}" findings (in ${NOTEBOOK} or src/arty/)`)
    if (fixMiss) return { result, cyclesUsed, escalate: fixMiss }
    marker = `${cfg.markerBase} — re-review ${cyclesUsed}`
    phase(cfg.reviewPhase)
    const o = { label: `reviewer:${cfg.key}-reverify-${cyclesUsed}`, phase: cfg.reviewPhase, agentType: 'model-reviewer', schema: REVIEW_SCHEMA }
    if (cfg.model) o.model = cfg.model
    result = await agent(`${cfg.reReviewBrief(marker)}\n\n${TAGGING}\n${DEFERRED}\n${HARNESS}`, o)
    if (!(await verifyReviewWrite(marker))) {
      return { result, cyclesUsed, escalate: { stage: `${cfg.key}-re-review-${cyclesUsed}`, reason: 'review.md write not found on disk', lastResult: result } }
    }
    fixItems = await triage(result, cfg, marker)
  }

  const escalate = fixItems.length > 0
    ? { stage: cfg.key, reason: `${fixItems.length} fix-routed finding(s) still open after ${cyclesUsed} fix cycle(s): ${fixItems.map((f) => f.id).join(', ')}`, lastResult: result }
    : null
  return { result, cyclesUsed, escalate }
}

function escalated(stage, collected) {
  log(`Stopping — ${stage.escalate.reason}. Escalating rather than looping past the cap; triage from result.escalate and the stage verdicts.`)
  return { thread: args.thread, questionSlug: args.questionSlug, status: 'escalate', escalate: stage.escalate, docSyncPending: DOC_SYNC, ...collected }
}

phase('Findings')
const findingsText = await collectFindings(args.findingsScopePaths, 'collect-findings')
log("Collected open findings touching this aspect's scope.")

// ---- Optional src/ implementation + a mechanical fidelity review ----
let implementation = null
if (args.needsSrcImplementation) {
  phase('Implement (if needed)')
  const implReturn = await agent(
    `${ANCHOR}\n\nWorkflow A src/ implementation pass. Read ${args.questionDocPath} (already approved) — it needs a physical or derived quantity that src/arty/ does not yet return. Add it there via targeted edits, following what the question doc resolves. Do not write the notebook yet — this pass only touches src/arty/.\n\nGoal: ${args.implementGoal}\n\nKnown open findings touching this scope:\n${findingsText}\n\nIf this pass resolves one of those FINDING[...] markers, delete the marker at its source in this same change and say so.\n\n${HARNESS}\n${STAGING}\n${FIDELITY}\n${DEFERRED}`,
    { label: 'modeler:implement', phase: 'Implement (if needed)', agentType: 'modeler' }
  )
  const implMiss = await verifyModelerPass('implement', implReturn, 'git diff --stat shows edits under src/arty/')
  if (implMiss) return escalated({ escalate: implMiss }, {})

  implementation = await reviewStage({
    key: 'implementation',
    reviewPhase: 'Review: Implementation',
    model: null, // Sonnet — mechanical fidelity, not theory critique
    markerBase: `Implementation verification — ${args.thread}/${args.questionSlug}`,
    initialBrief: (m) =>
      `${ANCHOR}\n\nImplementation verification pass on the src/arty/ additions just made for this assessment. Confirm the code faithfully provides what ${args.questionDocPath} specifies — trace the load-bearing path from each new function/constant to the quantity it is claimed to produce; reproduce any check script standalone; confirm cited numbers. This is mechanical fidelity-checking, not a critique of whether the assessment matters. Append a new dated section headed "${m}" to ${REVIEW} with a PASS / PASS-with-limitations / FAIL verdict and tagged findings.`,
    reReviewBrief: (m) =>
      `${ANCHOR}\n\nRe-review the src/ fix, scoped to the items you flagged previously in ${REVIEW} — do not redo the pass. Append a new dated section headed "${m}" to ${REVIEW} with your updated verdict.`,
    fixBrief: (m) =>
      `${ANCHOR}\n\nFix pass on src/arty/. Read the "${m}" section of ${REVIEW} and address the fix-routed findings listed below in the src/ implementation. Scoped to the flagged items only. If a fix resolves an open FINDING[...] marker, delete it at source and note it.`,
  }, 0, POST_PASS_FIX_CAP)
  if (implementation.escalate) return escalated(implementation, { implementation })
} else {
  log('needsSrcImplementation=false — skipping the src/ pass and its review, going straight to the notebook.')
}

// ---- Notebook (the published deliverable) ----
phase('Notebook')
const nbReturn = await agent(
  `${ANCHOR}\n\nWorkflow A notebook pass. Read ${args.questionDocPath} and write the thin ${NOTEBOOK} that imports from arty, runs the numerical study it specifies, and renders the verdict. No physics in the .qmd — everything physical comes from src/arty/ (agents-routing.md Gate 2). Re-render to confirm clean output.\n\nKnown open findings touching this scope:\n${findingsText}\n\nIf writing this notebook resolves one of those FINDING[...] markers, delete the marker at its source in this same change and say so.\n\n${HARNESS}\n${STAGING}\n${FIDELITY}\n${DEFERRED}`,
  { label: 'modeler:notebook', phase: 'Notebook', agentType: 'modeler' }
)
const nbMiss = await verifyModelerPass('notebook', nbReturn, `${NOTEBOOK} exists with real content, and every check script it cites by path exists under ${CHECKS}/`)
if (nbMiss) return escalated({ escalate: nbMiss }, { implementation })

// ---- Notebook review: adversarial (Opus) then verification (Sonnet), shared cap ----
let nbCycles = 0

const adversarial = await reviewStage({
  key: 'adversarial',
  reviewPhase: 'Review: Adversarial',
  model: OPUS,
  markerBase: `Adversarial critique — ${args.thread}/${args.questionSlug}`,
  initialBrief: (m) =>
    `${ANCHOR}\n\nAdversarial critique pass (Pass 1 of Workflow A review) on ${NOTEBOOK}. Nothing has been independently verified yet — review cold.\n\nBackground: this assesses whether the question in ${args.questionDocPath} matters; the main model is not modified by this workflow.\nPointer: ${NOTEBOOK} and its own citations into src/\n\nKnown open findings touching this scope:\n${findingsText}\n\nAppend a new dated section headed "${m}" to ${REVIEW} (never overwrite a prior pass's section) with your PASS / PASS-with-limitations / FAIL verdict and tagged findings (Blocking / Deferrable / Note, each with an impact estimate). You may spot-check a specific fact or number where your argument depends on one, but do not redo full verification.`,
  reReviewBrief: (m) =>
    `${ANCHOR}\n\nRe-review, scoped to the items the adversarial pass flagged previously in ${REVIEW} — do not redo the pass from scratch. Confirm whether the fix resolved them. Append a new dated section headed "${m}" to ${REVIEW} with your updated verdict.`,
  fixBrief: (m) =>
    `${ANCHOR}\n\nFix pass. Read the "${m}" section of ${REVIEW} and address the fix-routed findings listed below in ${NOTEBOOK} — and src/arty/ only if a finding requires it. Scoped to the flagged items only. If a fix resolves an open FINDING[...] marker, delete that marker at its source in this same change and note it.`,
}, nbCycles, MAX_FIX_CYCLES)
nbCycles = adversarial.cyclesUsed
if (adversarial.escalate) return escalated(adversarial, { implementation, adversarial, nbCycles })

const verification = await reviewStage({
  key: 'verification',
  reviewPhase: 'Review: Verification',
  model: null, // model-reviewer default (Sonnet)
  markerBase: `Verification — ${args.thread}/${args.questionSlug}`,
  initialBrief: (m) =>
    `${ANCHOR}\n\nVerification pass (Pass 2 of Workflow A review) on ${NOTEBOOK}. Pass 1 (adversarial critique) already ran and settled — read its section(s) of ${REVIEW} for context, do not redo it. Reproduce every check script standalone and confirm its output matches what the notebook reports; trace the load-bearing code path by hand; confirm cited numbers against their primaries rather than the notebook's word. Also confirm the .qmd is import-only — NO physics, computation, or parameter values inline (agents-routing.md Gate 2) — and that every check script it cites lives in ${CHECKS}/, not experiment/_scratch/, has a docstring naming its consumer, and re-runs standalone via uv run in under ~30 s (verification-scripts.md).\n\nAppend a new dated section headed "${m}" to ${REVIEW} with your own verdict and tagged findings.`,
  reReviewBrief: (m) =>
    `${ANCHOR}\n\nRe-review, scoped to the items the verification pass flagged previously in ${REVIEW} — do not redo the pass from scratch. Reproduce the fix and confirm. Append a new dated section headed "${m}" to ${REVIEW} with your updated verdict.`,
  fixBrief: (m) =>
    `${ANCHOR}\n\nFix pass. Read the "${m}" section of ${REVIEW} and address the fix-routed findings listed below in ${NOTEBOOK} — move any leaked physics into src/arty/ and import it; move any cited check script from experiment/_scratch/ into ${CHECKS}/; and src/arty/ only if a finding requires it. Scoped to the flagged items only.`,
}, nbCycles, MAX_FIX_CYCLES)
nbCycles = verification.cyclesUsed
if (verification.escalate) return escalated(verification, { implementation, adversarial, verification, nbCycles })

// ---- Doc-sync: one batched pass for stale copies (see model-workflow-b.js) ----
let docSync = { items: [], status: 'none' }
if (DOC_SYNC.length > 0) {
  phase('Doc-sync')
  const seen = new Set()
  const items = DOC_SYNC.filter((d) => (seen.has(d.summary) ? false : (seen.add(d.summary), true)))
  log(`Doc-sync: ${items.length} stale copy/copies batched into one pass (${DOC_SYNC.length - items.length} duplicate(s) dropped).`)
  const syncReturn = await agent(
    `${ANCHOR}\n\nDoc-sync pass — relocate already-settled values and verdicts, nothing else. The reviewed, current values are the ones in ${NOTEBOOK}, src/arty/ and the latest sections of ${REVIEW}. Fix each stale copy below by removing the restated figure, not by re-typing the current one (model-workflow skill, "A computed result has one home"): outside the home document, replace it with a link to its home section, keeping at most the verdict label and date; in a .qmd, replace it with an inline {python} expression or a table rendered from arty or a check results file. Re-type digits only in the home document itself. Derive, compute, or judge nothing new: if a copy cannot be synced without deciding something, leave it and add a FINDING[blocking] marker next to it saying why. Where a stale copy had its own FINDING marker, delete the marker once synced.\n\n${items.map((d) => `- [${d.stage}] ${d.id}: ${d.summary}`).join('\n')}\n\n${HARNESS}\n${DEFERRED}`,
    { label: 'modeler:doc-sync', phase: 'Doc-sync', agentType: 'modeler', model: SONNET }
  )
  const syncMiss = await verifyModelerPass('doc-sync', syncReturn, `git diff --stat shows edits to the documents named in these items: ${items.map((d) => d.id).join(', ')}`)
  if (syncMiss) return escalated({ escalate: syncMiss }, { implementation, adversarial, verification, nbCycles })
  docSync = { items, status: 'synced' }
}

// Dispatcher re-tier (deferred-findings.md) — see model-workflow-b.js.
phase('Re-tier')
const findingsAfter = await collectFindings([...new Set([...args.findingsScopePaths, THREAD_DIR, 'src/arty'])], 'collect-findings:after')

log('Review passed. Remaining steps (outside this workflow): (1) re-tier every deferrable/note in result.findingsAfter whose affects: paths lie inside a pass\'s scope restriction — grep what cites each affected artifact (deferred-findings.md); (2) the main agent links the challenge from the parent .qmd "Challenges" section if reader-relevant, and updates challenges/README.md (and the thread README, if it has one) with the verdict — a documentation-index edit, not a modeler dispatch; (3) commit each retained checks/ script in the same commit as the document citing it, squashed to one Conventional Commit (verification-scripts.md, git-flow.md).')

return {
  thread: args.thread,
  questionSlug: args.questionSlug,
  status: 'done',
  nbCycles,
  docSync,
  findingsAfter,
  verdicts: {
    implementation: implementation ? implementation.result.verdict : 'n/a (no src/ pass)',
    adversarial: adversarial.result.verdict,
    verification: verification.result.verdict,
  },
}
