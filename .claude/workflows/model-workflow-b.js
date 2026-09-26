export const meta = {
  name: 'model-workflow-b',
  description: 'Workflow B (model update) from an approved scoping.md: derivation, two-pass review with capped fix cycles, src/ implementation + a fidelity review, notebook presentation + a leak review — one model aspect per run',
  phases: [
    { title: 'Findings' },
    { title: 'Derivation' },
    { title: 'Review: Adversarial', detail: 'Opus — critiques the theory' },
    { title: 'Fix' },
    { title: 'Review: Verification', detail: 'Sonnet — reproduces the arithmetic' },
    { title: 'Implement' },
    { title: 'Review: Implementation', detail: 'Sonnet — src/ matches the settled derivation' },
    { title: 'Present' },
    { title: 'Review: Notebook', detail: 'Sonnet — .qmd import-only, no physics leak' },
    { title: 'Doc-sync', detail: 'Sonnet — one batched pass for stale copies, no re-review' },
    { title: 'Re-tier', detail: 'Re-collect open findings for the main agent to re-tier' },
  ],
}

// Encodes the model-workflow skill's "Workflow B — Update" from the derivation
// pass onward. Step 1 (librarian) and step 2 (scoping, plus the main agent's
// read-and-approve checkpoint) stay OUTSIDE this script — scoping is a judgment
// call about which option to pursue, not a deterministic control-flow step, so
// it keeps its human-in-the-loop gate. Only invoke this workflow after
// scoping.md has been reviewed and approved (agents-routing.md Gate 1/2/4;
// model-workflow skill "Workflow B").
//
// Review coverage mirrors "@model-reviewer after every modeler pass"
// (agents-routing.md): the DERIVATION gets the full two-pass treatment
// (adversarial Opus, then verification Sonnet) because it carries the theory;
// the IMPLEMENT and PRESENT passes each get a single mechanical verification
// pass (Sonnet) — src/ fidelity to the settled derivation, and the .qmd being
// import-only with no physics leak — not a second theory critique. Each of
// those two has its own small fix budget (POST_PASS_FIX_CAP), separate from
// the derivation review's shared cap.
//
// args = {
//   worktreePath: string,          // REQUIRED absolute path — caller must already
//                                  // be inside this worktree (Gate 1); every agent
//                                  // prompt anchors to it explicitly (subagent cwd-
//                                  // inheritance is unreliable, see subagent-harness.md)
//   model: string,                 // e.g. 'fragmentation-field' — experiment/<model>/
//   changeSlug: string,            // experiment/<model>/updates/<changeSlug>/
//   derivationGoal: string,        // what derivation.md must resolve — goal, not formula
//   derivationConstraints: string, // prior decisions to reference by file, not re-derive
//   derivationAcceptance: string,  // acceptance criteria / limiting cases / verdict question
//   inputFiles: string[],          // top-level files the modeler should read (scoping.md
//                                  // is always included; do not name src/arty/ internals —
//                                  // see model-workflow skill "Briefing subagents")
//   findingsScopePaths: string[],  // paths passed to collect-findings.py --for
// }

if (!args || !args.worktreePath) {
  throw new Error(
    'args.worktreePath is required — Gate 1 (agents-routing.md): the caller must already ' +
    'have entered this worktree (EnterWorktree) before invoking model-workflow-b.'
  )
}
if (!args.model || !args.changeSlug) {
  throw new Error('args.model and args.changeSlug are required.')
}
if (!Array.isArray(args.findingsScopePaths) || args.findingsScopePaths.length === 0) {
  throw new Error('args.findingsScopePaths must be a non-empty array (deferred-findings.md: inject the scope\'s open findings into every brief).')
}

const WT = args.worktreePath
const ANCHOR = `Working directory: ${WT} — anchor every Bash command and every Read/Edit/Write call to this absolute path, do not rely on an inherited cwd.`
const UPDATE_DIR = `experiment/${args.model}/updates/${args.changeSlug}`
const SCOPING = `${UPDATE_DIR}/scoping.md`
const DERIVATION = `${UPDATE_DIR}/derivation.md`
const REVIEW = `${UPDATE_DIR}/review.md`
const CHECKS = `${UPDATE_DIR}/checks`

// Exact model pins, never aliases. Sonnet stays on 4.6: Sonnet 5.0 refuses
// this project's subject matter. Helper agents (findings collection, on-disk
// checks) are pinned too — unpinned, they inherit the main-session model.
const OPUS = 'claude-opus-5-5'
const SONNET = 'claude-sonnet-4-6'

// Standing clauses appended to briefs, one per rule file. Each is the
// rule's operative instruction only — the agent reads the rule itself.
const HARNESS = `Python only via "uv run" (never bare python/pip); nontrivial check code goes in a file under experiment/_scratch/ run with a single-line "uv run python <path>" — /tmp is not writable (subagent-harness.md).`
const STAGING = `Before this pass ends, resolve every script YOU put in experiment/_scratch/: one that produced a number now cited in a committed artifact is git mv'd to ${CHECKS}/ — named for what it checks, a docstring naming the document it feeds, runnable standalone from the repo root, cited by path from that document, under ~30 s (vectorise sweeps; no numpy scalar math in loops). An uncited dead end may be deleted. Never delete or move anyone else's staged files (verification-scripts.md).`
const FIDELITY = `Any number taken from a source table is read from its doc-reference/**/tables/*.csv (never hand-copied into a literal) and that table's .invariant must pass ("uv run src/utils/check-table-invariants.py <path>.invariant"); a table with no closure invariant is flagged in your return summary, not treated as admissible. Citation anchors are greppable strings you have grepped, never bare line numbers (source-data-fidelity.md).`
const DEFERRED = `A defect you notice outside this pass's scope gets a one-line marker next to what you found — FINDING[blocking|deferrable|note]: <what> (affects: <repo paths>; since: <YYYY-MM-DD>) — not only a mention in review.md. A committed artifact or shipped code known to carry a wrong number is blocking, never deferred by you; say so in your return summary (deferred-findings.md).`
const REVIEW_RULES = `Beyond arithmetic: criterion match (does cited data measure the same quantity the model computes? a mismatch is Blocking), and provenance (a claim attributed to a primary is checked against that primary, or must be marked secondhand in the citing artifact). A search returning nothing over an extraction or text layer bounds that surface only — read the page before calling anything fabricated or absent (source-data-fidelity.md). Do not re-raise a defect already listed under the known open findings — cite its marker instead.`
const TAGGING = `Tag every blocking and deferrable finding in your structured return (model-workflow skill, "Materiality gate"): kind = basis (different quantity / population / regime / criterion) | closure (a source table fails its own invariant) | numeric (a value off on a correct basis) | doc-sync (a stale or disagreeing copy of a value or verdict) | process; bound = within / crosses / conditional / unbounded, judged against the Verdict outputs in ${SCOPING} — "within" only if it holds under EVERY plausible reading and neither crosses a threshold nor flips a shipped direction, and "impact zero if reading X is right" is conditional, not within; applies_elsewhere = whether the cause reaches another setting, caliber, parameter range or consumer. Severity is still yours to assign; the tags decide what it costs.`

const ARTIFACT_SCHEMA = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    detail: { type: 'string' },
  },
  required: ['ok', 'detail'],
}

// "A quiet return ≠ success" (subagent-harness.md): `completed` includes
// maxTurns exhaustion and silent permission denials, so every modeler pass is
// checked two ways — denial language in its return text, and the expected
// artifact on disk via a separate read. The script cannot SendMessage-resume,
// so a miss escalates with the classification hint instead of re-firing.
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
const MAX_FIX_CYCLES = 2 // derivation review — shared across adversarial + verification (skill "Workflow B" step 5)
const POST_PASS_FIX_CAP = 1 // implement / present verification — each its own budget, separate from the derivation cap

// Materiality gate (model-workflow skill, "Materiality gate"). Every Blocking
// finding carries three tags, and the ROUTE — not the count — decides whether
// it costs a fix cycle. Evidence: an audit of 80 acted-on findings across 21
// reviews, .claude/incidents.md#materiality.
const FINDING_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    severity: { type: 'string', enum: ['blocking', 'deferrable', 'note'] },
    // basis = a different quantity / population / regime / criterion / caliber;
    // closure = a source table fails its own invariant; numeric = a value is
    // off on a correct basis; doc-sync = a stale or disagreeing copy of a value
    // or verdict; process = a missing artifact, review, or retained script.
    kind: { type: 'string', enum: ['basis', 'closure', 'numeric', 'doc-sync', 'process'] },
    // Against the Verdict outputs in scoping.md: 'within' = holds under EVERY
    // reading and neither crosses a threshold nor flips a shipped direction;
    // 'crosses' = it does cross or flip; 'conditional' = the bound depends on
    // which reading is right; 'unbounded' = not computed.
    bound: { type: 'string', enum: ['within', 'crosses', 'conditional', 'unbounded'] },
    applies_elsewhere: { type: 'boolean' }, // the cause reaches another setting, caliber, range or consumer
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
    findings: { type: 'array', items: FINDING_SCHEMA }, // every blocking and deferrable finding
    summary: { type: 'string' },
    section_heading: { type: 'string' }, // the exact heading it appended to review.md
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
          evidence: { type: 'string' }, // the computed margin, and the check script path that produced it
        },
        required: ['id', 'bound', 'evidence'],
      },
    },
  },
  required: ['bounds'],
}

// Route one blocking finding. Kind and reach decide before magnitude does:
// in the audit, size never separated a real defect from noise, and every
// small-signature defect was a basis/closure mismatch or had a cause that
// applied elsewhere.
function routeOf(f) {
  if (f.kind === 'basis' || f.kind === 'closure' || f.kind === 'process' || f.applies_elsewhere) return 'fix'
  if (f.kind === 'doc-sync') return 'doc-sync' // stays blocking until synced; human-approved 2026-09-25
  if (f.bound === 'crosses') return 'fix'
  if (f.bound === 'within') return 'note'
  return 'bound' // conditional / unbounded: bound it cheaply first, never defer it as "unquantified"
}

const WRITE_CHECK_SCHEMA = {
  type: 'object',
  properties: {
    found: { type: 'boolean' },
    heading_seen: { type: 'string' },
  },
  required: ['found'],
}

// Doc-sync findings from every stage, synced in ONE batched pass at the end
// (no modeler fix cycle, no re-review) — the dominant waste in the audit was
// re-flagging and re-cycling stale copies, not fixing them.
const DOC_SYNC = []

// Sort a review's blocking findings into what needs a fix cycle now. Findings
// with a conditional / unbounded impact get one cheap bounding pass first.
// Returns the fix-routed findings; an empty array means no fix cycle.
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
      `${ANCHOR}\n\nBounding pass — not a review, not a fix. For each finding below from the "${marker}" section of ${REVIEW}, compute the largest change it could make to the Verdict outputs declared in ${SCOPING} (threshold and shipped-claim direction), under EVERY plausible reading — reuse src/arty/ functions by perturbing their inputs; do not investigate the cause. Return bound=within only if no reading crosses a threshold or flips a shipped direction; crosses if one does; unbounded if it cannot be computed cheaply. Append a dated section headed "Bounds — ${marker}" to ${REVIEW} with each margin and the check script that produced it.\n\nFindings:\n${toBound.map((f) => `- ${f.id}: ${f.summary}`).join('\n')}\n\n${HARNESS}\n${STAGING}`,
      { label: `bound:${cfg.key}`, phase: cfg.reviewPhase, agentType: 'model-reviewer', schema: BOUND_SCHEMA }
    )
    const byId = new Map(((b && b.bounds) || []).map((x) => [x.id, x.bound]))
    for (const r of routed) {
      if (r.route !== 'bound') continue
      r.route = byId.get(r.f.id) === 'within' ? 'note' : 'fix' // still unbounded after bounding → fix, never waved through
    }
  }
  for (const r of routed) if (r.route === 'doc-sync') DOC_SYNC.push({ stage: cfg.key, ...r.f })
  const noted = routed.filter((r) => r.route === 'note').map((r) => r.f.id)
  if (noted.length) log(`Bounded within every Verdict-output threshold — note only, no fix cycle: ${noted.join(', ')}`)
  return routed.filter((r) => r.route === 'fix').map((r) => r.f)
}

// "On return of each pass, the main agent verifies review.md exists on disk
// and carries that pass's section" (model-workflow skill) — a background
// dispatch can silently drop the write, so this is a genuinely separate
// read, not the reviewing agent grading its own homework.
async function verifyReviewWrite(marker) {
  const check = await agent(
    `${ANCHOR}\nRead ${REVIEW} and report whether it contains a section heading matching "${marker}". A background dispatch can silently drop a write — confirm the file on disk, don't assume. Return found=true/false and the closest heading you actually see.`,
    { label: 'verify-review-write', effort: 'low', model: SONNET, schema: WRITE_CHECK_SCHEMA }
  )
  return !!(check && check.found)
}

// One review stage = an initial review pass, a disk-write check, then a capped
// fix/re-review loop. `cyclesUsedIn`/`capCeiling` let the two derivation passes
// share one counter (ceiling MAX_FIX_CYCLES) while each post-derivation pass
// runs its own (0..POST_PASS_FIX_CAP). Returns { result, cyclesUsed, escalate }.
async function reviewStage(cfg, cyclesUsedIn, capCeiling) {
  let cyclesUsed = cyclesUsedIn
  let marker = cfg.markerBase
  const reviewOpts = () => {
    const o = { label: `reviewer:${cfg.key}`, phase: cfg.reviewPhase, agentType: 'model-reviewer', schema: REVIEW_SCHEMA }
    if (cfg.model) o.model = cfg.model
    return o
  }

  phase(cfg.reviewPhase)
  let result = await agent(`${cfg.initialBrief(marker)}\n\n${REVIEW_RULES}\n${TAGGING}\n${DEFERRED}\n${HARNESS}`, reviewOpts())
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
    const fixMiss = await verifyModelerPass(`fix-${cfg.key}-${cyclesUsed}`, fixReturn, `git diff --stat shows edits addressing the "${marker}" findings (in ${DERIVATION}, src/arty/, or the notebook partial)`)
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
  log(`Stopping — ${stage.escalate.reason}. Escalating rather than looping past the cap (skill "Workflow B" step 5); triage from result.escalate and the stage verdicts.`)
  return { changeSlug: args.changeSlug, status: 'escalate', escalate: stage.escalate, docSyncPending: DOC_SYNC, ...collected }
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

phase('Findings')
const findingsText = await collectFindings(args.findingsScopePaths, 'collect-findings')
log("Collected open findings touching this aspect's scope.")

phase('Derivation')
const derivReturn = await agent(
  `${ANCHOR}\n\nWorkflow B derivation pass. Read ${SCOPING} (already approved) and implement what it resolves in ${DERIVATION} — math, unit checks, self-consistency. Do not re-derive or second-guess the scoping decision; implement it.\n\nGoal: ${args.derivationGoal}\nConstraints: ${args.derivationConstraints}\nAcceptance criteria: ${args.derivationAcceptance}\nFiles to read: ${[SCOPING, ...args.inputFiles].join(', ')}\n\nKnown open findings touching this scope:\n${findingsText}\n\nIf this derivation resolves one of those FINDING[...] markers, delete the marker at its source in this same change and say so. Do not touch src/arty/ or any .qmd yet — this pass only writes ${DERIVATION} (and its ${CHECKS}/).\n\n${HARNESS}\n${STAGING}\n${FIDELITY}\n${DEFERRED}`,
  { label: 'modeler:derivation', phase: 'Derivation', agentType: 'modeler' }
)
const derivMiss = await verifyModelerPass('derivation', derivReturn, `${DERIVATION} exists with derivation content (not a heading-only skeleton), and every check script it cites by path exists under ${CHECKS}/`)
if (derivMiss) return escalated({ escalate: derivMiss }, {})

// ---- Derivation review: adversarial (Opus) then verification (Sonnet), shared cap ----
let derivCycles = 0

const adversarial = await reviewStage({
  key: 'adversarial',
  reviewPhase: 'Review: Adversarial',
  model: OPUS,
  markerBase: `Adversarial critique — ${args.changeSlug}`,
  initialBrief: (m) =>
    `${ANCHOR}\n\nAdversarial critique pass (Pass 1 of Workflow B review) on ${DERIVATION}. Nothing has been independently verified yet — review cold, before any arithmetic is trusted.\n\nBackground: ${args.derivationGoal}\nPointer: ${DERIVATION} and its own citations into src/\n\nKnown open findings touching this scope:\n${findingsText}\n\nAppend a new dated section headed "${m}" to ${REVIEW} (never overwrite a prior pass's section) with your PASS / PASS-with-limitations / FAIL verdict and tagged findings (Blocking / Deferrable / Note, each with an impact estimate). You may spot-check a specific fact or number where your argument depends on one, but do not redo full verification — that is Pass 2's job.`,
  reReviewBrief: (m) =>
    `${ANCHOR}\n\nRe-review, scoped to the items the adversarial pass flagged previously in ${REVIEW} — do not redo the pass from scratch. Confirm whether the fix resolved them. Append a new dated section headed "${m}" to ${REVIEW} with your updated verdict.`,
  fixBrief: (m) =>
    `${ANCHOR}\n\nFix pass. Read the "${m}" section of ${REVIEW} and address the fix-routed findings listed below in ${DERIVATION} — and src/arty/ only if a finding requires it. Scoped to the flagged items only; do not expand beyond them. If a fix resolves an open FINDING[...] marker, delete that marker at its source in this same change and note it.`,
}, derivCycles, MAX_FIX_CYCLES)
derivCycles = adversarial.cyclesUsed
if (adversarial.escalate) return escalated(adversarial, { adversarial, derivCycles })

const verification = await reviewStage({
  key: 'verification',
  reviewPhase: 'Review: Verification',
  model: null, // model-reviewer default (Sonnet)
  markerBase: `Verification — ${args.changeSlug}`,
  initialBrief: (m) =>
    `${ANCHOR}\n\nVerification pass (Pass 2 of Workflow B review) on ${DERIVATION}. Pass 1 (adversarial critique) already ran and settled — read its section(s) of ${REVIEW} for context, do not redo it. Reproduce every check script standalone and confirm its output matches what the derivation reports; trace the load-bearing code path by hand; confirm cited numbers against their primaries rather than the derivation's word.\n\nKnown open findings touching this scope:\n${findingsText}\n\nAppend a new dated section headed "${m}" to ${REVIEW} with your own verdict and tagged findings.`,
  reReviewBrief: (m) =>
    `${ANCHOR}\n\nRe-review, scoped to the items the verification pass flagged previously in ${REVIEW} — do not redo the pass from scratch. Reproduce the fix and confirm. Append a new dated section headed "${m}" to ${REVIEW} with your updated verdict.`,
  fixBrief: (m) =>
    `${ANCHOR}\n\nFix pass. Read the "${m}" section of ${REVIEW} and address the fix-routed findings listed below in ${DERIVATION} — and src/arty/ only if a finding requires it. Scoped to the flagged items only. If a fix resolves an open FINDING[...] marker, delete that marker at its source in this same change and note it.`,
}, derivCycles, MAX_FIX_CYCLES)
derivCycles = verification.cyclesUsed
if (verification.escalate) return escalated(verification, { adversarial, verification, derivCycles })

// ---- Implement (src/) + a mechanical fidelity review ----
phase('Implement')
const implReturn = await agent(
  `${ANCHOR}\n\nImplement pass. Read ${DERIVATION} (reviewed: adversarial=${adversarial.result.verdict}, verification=${verification.result.verdict}) and write the derived physics into src/arty/ modules (functions, parameters, geometry) via targeted edits. All project physics is common and lives here — never in a .qmd (agents-routing.md Gate 2). If either review left PASS-with-limitations entries, log them as derivation assumptions and/or in _limitations.qmd as part of this pass — they do not need another review cycle.\n\n${HARNESS}\n${STAGING}\n${FIDELITY}\n${DEFERRED}`,
  { label: 'modeler:implement', phase: 'Implement', agentType: 'modeler' }
)
const implMiss = await verifyModelerPass('implement', implReturn, 'git diff --stat shows edits under src/arty/')
if (implMiss) return escalated({ escalate: implMiss }, { adversarial, verification, derivCycles })

const implementation = await reviewStage({
  key: 'implementation',
  reviewPhase: 'Review: Implementation',
  model: null, // Sonnet — mechanical fidelity, not theory critique
  markerBase: `Implementation verification — ${args.changeSlug}`,
  initialBrief: (m) =>
    `${ANCHOR}\n\nImplementation verification pass on the src/arty/ changes just made for ${args.changeSlug}. The derivation ${DERIVATION} is reviewed and settled — your job is to confirm the src/ code faithfully implements it, NOT to re-critique the theory. Trace the load-bearing path from each changed function/constant to the quantities it is claimed to affect (and nothing else); reproduce any check script standalone; confirm cited numbers against ${DERIVATION}. Append a new dated section headed "${m}" to ${REVIEW} with a PASS / PASS-with-limitations / FAIL verdict and tagged findings.`,
  reReviewBrief: (m) =>
    `${ANCHOR}\n\nRe-review the src/ fix, scoped to the items you flagged previously in ${REVIEW} — do not redo the pass. Append a new dated section headed "${m}" to ${REVIEW} with your updated verdict.`,
  fixBrief: (m) =>
    `${ANCHOR}\n\nFix pass on src/arty/. Read the "${m}" section of ${REVIEW} and address the fix-routed findings listed below in the src/ implementation (touch ${DERIVATION} only if the derivation itself is where the defect lives). Scoped to the flagged items only. If a fix resolves an open FINDING[...] marker, delete it at source and note it.`,
}, 0, POST_PASS_FIX_CAP)
if (implementation.escalate) return escalated(implementation, { adversarial, verification, implementation, derivCycles })

// ---- Present (notebook) + a leak / retention review ----
phase('Present')
const presentReturn = await agent(
  `${ANCHOR}\n\nNotebook presentation pass. Edit the relevant section partial experiment/${args.model}/_<section>.qmd (or add a new partial + {{< include >}} line) to import the new src/arty/ code and render results, and add a "## Change Log" entry (major.minor) referencing ${DERIVATION}. Edit, never rewrite. No physics, computation, or parameter values in the .qmd (agents-routing.md Gate 2). Re-render to confirm clean output. Confirm experiment/_scratch/ holds none of this change's scripts — every one that produced a cited number now sits in ${CHECKS}/ (other in-flight work may legitimately be staged there; leave it alone).\n\n${HARNESS}\n${STAGING}\n${DEFERRED}`,
  { label: 'modeler:present', phase: 'Present', agentType: 'modeler' }
)
const presentMiss = await verifyModelerPass('present', presentReturn, `git diff --stat shows an edited experiment/${args.model}/_*.qmd partial containing a Change Log entry that references ${DERIVATION}`)
if (presentMiss) return escalated({ escalate: presentMiss }, { adversarial, verification, implementation, derivCycles })

const notebook = await reviewStage({
  key: 'notebook',
  reviewPhase: 'Review: Notebook',
  model: null, // Sonnet — mechanical leak / retention check
  markerBase: `Notebook verification — ${args.changeSlug}`,
  initialBrief: (m) =>
    `${ANCHOR}\n\nNotebook verification pass on the section partial just edited for ${args.changeSlug}. Confirm: (1) it imports the new physics from src/arty/ and contains NO physics, computation, or parameter values inline — everything physical must come from arty (agents-routing.md Gate 2); (2) a "## Change Log" (major.minor) entry exists and references ${DERIVATION}; (3) it re-renders clean; (4) experiment/_scratch/ holds none of this change's cited check scripts — each sits in ${CHECKS}/, has a docstring naming its consumer, and re-runs standalone via uv run in under ~30 s (verification-scripts.md). Append a new dated section headed "${m}" to ${REVIEW} with a verdict and tagged findings.`,
  reReviewBrief: (m) =>
    `${ANCHOR}\n\nRe-review the notebook fix, scoped to the items you flagged previously in ${REVIEW}. Append a new dated section headed "${m}" to ${REVIEW} with your updated verdict.`,
  fixBrief: (m) =>
    `${ANCHOR}\n\nFix pass on the notebook. Read the "${m}" section of ${REVIEW} and address the fix-routed findings listed below in the .qmd/partial — move any leaked physics into src/arty/ and import it; move any cited check script from experiment/_scratch/ into ${CHECKS}/. Scoped to the flagged items only.`,
}, 0, POST_PASS_FIX_CAP)
if (notebook.escalate) return escalated(notebook, { adversarial, verification, implementation, notebook, derivCycles })

// ---- Doc-sync: one batched pass for every stale copy flagged along the way ----
// No physics is judged here, so Sonnet; no re-review cycle, only a disk check.
// Each item stays blocking until this pass lands it (deferred-findings.md).
let docSync = { items: [], status: 'none' }
if (DOC_SYNC.length > 0) {
  phase('Doc-sync')
  const seen = new Set()
  const items = DOC_SYNC.filter((d) => (seen.has(d.summary) ? false : (seen.add(d.summary), true)))
  log(`Doc-sync: ${items.length} stale copy/copies batched into one pass (${DOC_SYNC.length - items.length} duplicate(s) dropped).`)
  const syncReturn = await agent(
    `${ANCHOR}\n\nDoc-sync pass — relocate already-settled values and verdicts, nothing else. The reviewed, current values are the ones in ${DERIVATION}, src/arty/ and the latest sections of ${REVIEW}. Fix each stale copy below by removing the restated figure, not by re-typing the current one (model-workflow skill, "A computed result has one home"): outside the home document, replace it with a link to its home section, keeping at most the verdict label and date; in a .qmd, replace it with an inline {python} expression or a table rendered from arty or a check results file. Re-type digits only in the home document itself. Derive, compute, or judge nothing new: if a copy cannot be synced without deciding something, leave it and add a FINDING[blocking] marker next to it saying why. Where a stale copy had its own FINDING marker, delete the marker once synced.\n\n${items.map((d) => `- [${d.stage}] ${d.id}: ${d.summary}`).join('\n')}\n\n${HARNESS}\n${DEFERRED}`,
    { label: 'modeler:doc-sync', phase: 'Doc-sync', agentType: 'modeler', model: SONNET }
  )
  const syncMiss = await verifyModelerPass('doc-sync', syncReturn, `git diff --stat shows edits to the documents named in these items: ${items.map((d) => d.id).join(', ')}`)
  if (syncMiss) return escalated({ escalate: syncMiss }, { adversarial, verification, implementation, notebook, derivCycles })
  docSync = { items, status: 'synced' }
}

// "The dispatcher re-tiers a subagent's findings on return" (deferred-findings.md):
// a scope-restricted pass can only tag what it was allowed to see, so the
// register is re-collected and handed back — the re-tiering itself (follow each
// deferrable/note's affects: paths outward) is the main agent's judgment.
phase('Re-tier')
const findingsAfter = await collectFindings([...new Set([...args.findingsScopePaths, UPDATE_DIR, 'src/arty'])], 'collect-findings:after')
log('Done. Main agent: (1) re-tier every deferrable/note in result.findingsAfter whose affects: paths lie inside a pass\'s scope restriction — grep what cites each affected artifact; (2) commit each retained checks/ script in the same commit as the document citing it, squashed to one Conventional Commit (verification-scripts.md, git-flow.md).')

return {
  changeSlug: args.changeSlug,
  status: 'done',
  derivCycles,
  docSync,
  findingsAfter,
  verdicts: {
    adversarial: adversarial.result.verdict,
    verification: verification.result.verdict,
    implementation: implementation.result.verdict,
    notebook: notebook.result.verdict,
  },
}
