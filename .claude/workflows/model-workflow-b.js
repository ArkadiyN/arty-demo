export const meta = {
  name: 'model-workflow-b',
  description: 'Workflow B (model update) from an approved scoping.md: derivation, two-pass review with capped fix cycles, src/ implementation, notebook presentation — one model aspect per run',
  phases: [
    { title: 'Findings' },
    { title: 'Derivation' },
    { title: 'Review: Adversarial', detail: 'Opus — critiques the theory' },
    { title: 'Fix' },
    { title: 'Review: Verification', detail: 'Sonnet — reproduces the arithmetic' },
    { title: 'Implement' },
    { title: 'Present' },
  ],
}

// Encodes the model-workflow skill's "Workflow B — Update" steps 3-7
// (derivation onward). Step 1 (librarian) and step 2 (scoping, plus the
// main agent's read-and-approve checkpoint) stay OUTSIDE this script —
// scoping is a judgment call about which option to pursue, not a
// deterministic control-flow step, so it keeps its human-in-the-loop gate.
// Only invoke this workflow after scoping.md has been reviewed and
// approved (agents-routing.md Gate 1/2/4; model-workflow skill "Workflow B").
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

const WT = args.worktreePath
const ANCHOR = `Working directory: ${WT} — anchor every Bash command and every Read/Edit/Write call to this absolute path, do not rely on an inherited cwd.`
const UPDATE_DIR = `experiment/${args.model}/updates/${args.changeSlug}`
const SCOPING = `${UPDATE_DIR}/scoping.md`
const DERIVATION = `${UPDATE_DIR}/derivation.md`
const REVIEW = `${UPDATE_DIR}/review.md`
const MAX_FIX_CYCLES = 2 // shared across both review passes — model-workflow skill "Workflow B" step 5

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'PASS-with-limitations', 'FAIL'] },
    blocking_count: { type: 'integer' },
    deferrable_count: { type: 'integer' },
    note_count: { type: 'integer' },
    summary: { type: 'string' },
    section_heading: { type: 'string' }, // the exact heading it appended to review.md
  },
  required: ['verdict', 'blocking_count', 'summary', 'section_heading'],
}

const WRITE_CHECK_SCHEMA = {
  type: 'object',
  properties: {
    found: { type: 'boolean' },
    heading_seen: { type: 'string' },
  },
  required: ['found'],
}

function needsFix(r) {
  return !r || r.verdict === 'FAIL' || r.blocking_count > 0
}

// "On return of each pass, the main agent verifies review.md exists on disk
// and carries that pass's section" (model-workflow skill) — a background
// dispatch can silently drop the write, so this is a genuinely separate
// read, not the reviewing agent grading its own homework.
async function verifyReviewWrite(marker) {
  const check = await agent(
    `${ANCHOR}\nRead ${REVIEW} and report whether it contains a section heading matching "${marker}". A background dispatch can silently drop a write — confirm the file on disk, don't assume. Return found=true/false and the closest heading you actually see.`,
    { label: 'verify-review-write', effort: 'low', schema: WRITE_CHECK_SCHEMA }
  )
  return !!(check && check.found)
}

phase('Findings')
const findingsText = await agent(
  `${ANCHOR}\nFrom the repo root, run exactly: uv run python src/utils/collect-findings.py --for ${args.findingsScopePaths.join(' ')}\nReturn its stdout verbatim, nothing else.`,
  { label: 'collect-findings', effort: 'low' }
)
log("Collected open findings touching this aspect's scope.")

phase('Derivation')
await agent(
  `${ANCHOR}\n\nWorkflow B derivation pass. Read ${SCOPING} (already approved) and implement what it resolves in ${DERIVATION} — math, unit checks, self-consistency. Do not re-derive or second-guess the scoping decision; implement it.\n\nGoal: ${args.derivationGoal}\nConstraints: ${args.derivationConstraints}\nAcceptance criteria: ${args.derivationAcceptance}\nFiles to read: ${[SCOPING, ...args.inputFiles].join(', ')}\n\nKnown open findings touching this scope:\n${findingsText}\n\nDo not touch src/arty/ or any .qmd yet — this pass only writes ${DERIVATION}. Any in-flight check script goes to experiment/_scratch/ for now (it moves to this change's checks/ folder once the number it produced is cited).`,
  { label: 'modeler:derivation', phase: 'Derivation', agentType: 'modeler' }
)

let cyclesUsed = 0
let escalate = null

// ---- Pass 1: adversarial critique (Opus) ----
phase('Review: Adversarial')
let pass1Marker = `Adversarial critique — ${args.changeSlug}`
let pass1 = await agent(
  `${ANCHOR}\n\nAdversarial critique pass (Pass 1 of Workflow B review) on ${DERIVATION}. Nothing has been independently verified yet — review cold, before any arithmetic is trusted.\n\nBackground: ${args.derivationGoal}\nPointer: ${DERIVATION} and its own citations into src/\n\nAppend a new dated section headed "${pass1Marker}" to ${REVIEW} (never overwrite a prior pass's section) with your PASS / PASS-with-limitations / FAIL verdict and tagged findings (Blocking / Deferrable / Note, each with an impact estimate). You may spot-check a specific fact or number where your argument depends on one, but do not redo full verification — that is Pass 2's job.`,
  { label: 'reviewer:adversarial', phase: 'Review: Adversarial', agentType: 'model-reviewer', model: 'opus', schema: REVIEW_SCHEMA }
)
if (!(await verifyReviewWrite(pass1Marker))) {
  log('Adversarial review section missing from review.md on disk — treating as a dropped write, not a pass.')
  escalate = { stage: 'adversarial-review', reason: 'review.md write not found on disk', lastResult: pass1 }
}

while (!escalate && needsFix(pass1) && cyclesUsed < MAX_FIX_CYCLES) {
  cyclesUsed++
  phase('Fix')
  log(`Fix cycle ${cyclesUsed}/${MAX_FIX_CYCLES} — addressing adversarial-pass findings.`)
  await agent(
    `${ANCHOR}\n\nFix pass. Read the "${pass1Marker}" section of ${REVIEW} and address its Blocking findings (and, at your judgment, Deferrable ones) in ${DERIVATION} — and src/arty/ only if a finding requires it. Scoped to the flagged items only; do not expand beyond them.`,
    { label: `modeler:fix-${cyclesUsed}`, phase: 'Fix', agentType: 'modeler' }
  )
  phase('Review: Adversarial')
  pass1Marker = `Adversarial critique re-review ${cyclesUsed} — ${args.changeSlug}`
  pass1 = await agent(
    `${ANCHOR}\n\nRe-review, scoped to the items the adversarial pass flagged previously in ${REVIEW} — do not redo the pass from scratch. Confirm whether the fix resolved them. Append a new dated section headed "${pass1Marker}" to ${REVIEW} with your updated verdict.`,
    { label: `reviewer:adversarial-reverify-${cyclesUsed}`, phase: 'Review: Adversarial', agentType: 'model-reviewer', model: 'opus', schema: REVIEW_SCHEMA }
  )
  if (!(await verifyReviewWrite(pass1Marker))) {
    escalate = { stage: `adversarial-re-review-${cyclesUsed}`, reason: 'review.md write not found on disk', lastResult: pass1 }
  }
}

if (!escalate && needsFix(pass1)) {
  escalate = {
    stage: 'adversarial-review',
    reason: `still ${pass1.verdict} with ${pass1.blocking_count} blocking finding(s) after ${MAX_FIX_CYCLES} fix cycle(s)`,
    lastResult: pass1,
  }
}

// ---- Pass 2: verification (Sonnet, model-reviewer default) ----
let pass2 = null
if (!escalate) {
  phase('Review: Verification')
  let pass2Marker = `Verification — ${args.changeSlug}`
  pass2 = await agent(
    `${ANCHOR}\n\nVerification pass (Pass 2 of Workflow B review) on ${DERIVATION}. Pass 1 (adversarial critique) already ran and settled — read its section(s) of ${REVIEW} for context, do not redo it. Reproduce every check script standalone and confirm its output matches what the derivation reports; trace the load-bearing code path by hand; confirm cited numbers against their primaries rather than the derivation's word.\n\nAppend a new dated section headed "${pass2Marker}" to ${REVIEW} with your own verdict and tagged findings.`,
    { label: 'reviewer:verification', phase: 'Review: Verification', agentType: 'model-reviewer', schema: REVIEW_SCHEMA }
  )
  if (!(await verifyReviewWrite(pass2Marker))) {
    escalate = { stage: 'verification-review', reason: 'review.md write not found on disk', lastResult: pass2 }
  }

  while (!escalate && needsFix(pass2) && cyclesUsed < MAX_FIX_CYCLES) {
    cyclesUsed++
    phase('Fix')
    log(`Fix cycle ${cyclesUsed}/${MAX_FIX_CYCLES} — addressing verification-pass findings.`)
    await agent(
      `${ANCHOR}\n\nFix pass. Read the "${pass2Marker}" section of ${REVIEW} and address its Blocking findings (and, at your judgment, Deferrable ones) in ${DERIVATION} — and src/arty/ only if a finding requires it. Scoped to the flagged items only.`,
      { label: `modeler:fix-${cyclesUsed}`, phase: 'Fix', agentType: 'modeler' }
    )
    phase('Review: Verification')
    pass2Marker = `Verification re-review ${cyclesUsed} — ${args.changeSlug}`
    pass2 = await agent(
      `${ANCHOR}\n\nRe-review, scoped to the items the verification pass flagged previously in ${REVIEW} — do not redo the pass from scratch. Reproduce the fix and confirm. Append a new dated section headed "${pass2Marker}" to ${REVIEW} with your updated verdict.`,
      { label: `reviewer:verification-reverify-${cyclesUsed}`, phase: 'Review: Verification', agentType: 'model-reviewer', schema: REVIEW_SCHEMA }
    )
    if (!(await verifyReviewWrite(pass2Marker))) {
      escalate = { stage: `verification-re-review-${cyclesUsed}`, reason: 'review.md write not found on disk', lastResult: pass2 }
    }
  }

  if (!escalate && needsFix(pass2)) {
    escalate = {
      stage: 'verification-review',
      reason: `still ${pass2.verdict} with ${pass2.blocking_count} blocking finding(s) after ${MAX_FIX_CYCLES} total fix cycle(s)`,
      lastResult: pass2,
    }
  }
}

if (escalate) {
  log(`Stopping — ${escalate.reason}. Escalating rather than looping a third time (the fix-cycle cap is shared across both review passes, per model-workflow skill "Workflow B" step 5).`)
  return { changeSlug: args.changeSlug, status: 'escalate', cyclesUsed, escalate, pass1, pass2 }
}

// ---- Implement + present (both PASS or PASS-with-limitations) ----
phase('Implement')
await agent(
  `${ANCHOR}\n\nImplement pass. Read ${DERIVATION} (reviewed: adversarial=${pass1.verdict}, verification=${pass2.verdict}) and write the derived physics into src/arty/ modules (functions, parameters, geometry) via targeted edits. All project physics is common and lives here — never in a .qmd. If either review left PASS-with-limitations entries, log them as derivation assumptions and/or in _limitations.qmd as part of this pass — they do not need another review cycle.`,
  { label: 'modeler:implement', phase: 'Implement', agentType: 'modeler' }
)

phase('Present')
await agent(
  `${ANCHOR}\n\nNotebook presentation pass. Edit the relevant section partial experiment/${args.model}/_<section>.qmd (or add a new partial + {{< include >}} line) to import the new src/arty/ code and render results, and add a "## Change Log" entry (major.minor) referencing ${DERIVATION}. Edit, never rewrite. Re-render to confirm clean output. Confirm experiment/_scratch/ is empty — every check script that produced a cited number now sits in this change's checks/ folder.`,
  { label: 'modeler:present', phase: 'Present', agentType: 'modeler' }
)

return {
  changeSlug: args.changeSlug,
  status: 'done',
  cyclesUsed,
  pass1Verdict: pass1.verdict,
  pass2Verdict: pass2.verdict,
}
