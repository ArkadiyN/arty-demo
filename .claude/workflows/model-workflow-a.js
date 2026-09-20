export const meta = {
  name: 'model-workflow-a',
  description: 'Workflow A (assessment) from an approved question doc: optional src/ implementation, notebook, two-pass review with capped fix cycles — the main model is never modified',
  phases: [
    { title: 'Findings' },
    { title: 'Implement (if needed)' },
    { title: 'Notebook' },
    { title: 'Review: Adversarial', detail: 'Opus — critiques the theory' },
    { title: 'Fix' },
    { title: 'Review: Verification', detail: 'Sonnet — reproduces the arithmetic' },
  ],
}

// Encodes the model-workflow skill's "Workflow A — Assessment" steps 3-5
// (src/ implementation onward). Steps 1 (librarian, if needed) and 2 (the
// question doc, plus the main agent's read-and-approve checkpoint) stay
// OUTSIDE this script, same reasoning as model-workflow-b.js: picking the
// thread folder and writing the problem statement / verdict criterion is a
// judgment call, not a deterministic control-flow step. Step 6 (linking the
// challenge from the parent .qmd and updating challenges/README.md) is a
// documentation-index edit, not physics — it stays a plain main-agent edit
// after this workflow returns, not a modeler dispatch (Gate 2 does not
// apply: no physical quantity is being authored).
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

const WT = args.worktreePath
const ANCHOR = `Working directory: ${WT} — anchor every Bash command and every Read/Edit/Write call to this absolute path, do not rely on an inherited cwd.`
const THREAD_DIR = `experiment/${args.model}/challenges/${args.thread}`
const NOTEBOOK = `${THREAD_DIR}/${args.questionSlug}.qmd`
const REVIEW = `${THREAD_DIR}/review.md`
const MAX_FIX_CYCLES = 2 // shared across both review passes — same cap as Workflow B, applies identically here

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'PASS-with-limitations', 'FAIL'] },
    blocking_count: { type: 'integer' },
    deferrable_count: { type: 'integer' },
    note_count: { type: 'integer' },
    summary: { type: 'string' },
    section_heading: { type: 'string' },
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

if (args.needsSrcImplementation) {
  phase('Implement (if needed)')
  await agent(
    `${ANCHOR}\n\nWorkflow A src/ implementation pass. Read ${args.questionDocPath} (already approved) — it needs a physical or derived quantity that src/arty/ does not yet return. Add it there via targeted edits, following what the question doc resolves. Do not write the notebook yet — this pass only touches src/arty/.\n\nGoal: ${args.implementGoal}\n\nKnown open findings touching this scope:\n${findingsText}`,
    { label: 'modeler:implement', phase: 'Implement (if needed)', agentType: 'modeler' }
  )
} else {
  log('needsSrcImplementation=false — skipping the src/ pass, going straight to the notebook.')
}

phase('Notebook')
await agent(
  `${ANCHOR}\n\nWorkflow A notebook pass. Read ${args.questionDocPath} and write the thin ${NOTEBOOK} that imports from arty, runs the numerical study it specifies, and renders the verdict. No physics in the .qmd — everything physical comes from src/arty/. Any check script goes to experiment/_scratch/ for now (it moves to ${THREAD_DIR}/checks/ once the number it produces is cited). Re-render to confirm clean output.\n\nKnown open findings touching this scope:\n${findingsText}`,
  { label: 'modeler:notebook', phase: 'Notebook', agentType: 'modeler' }
)

let cyclesUsed = 0
let escalate = null

// ---- Pass 1: adversarial critique (Opus) ----
phase('Review: Adversarial')
let pass1Marker = `Adversarial critique — ${args.thread}/${args.questionSlug}`
let pass1 = await agent(
  `${ANCHOR}\n\nAdversarial critique pass (Pass 1 of Workflow A review) on ${NOTEBOOK}. Nothing has been independently verified yet — review cold.\n\nBackground: this assesses whether the question in ${args.questionDocPath} matters; the main model is not modified by this workflow.\nPointer: ${NOTEBOOK} and its own citations into src/\n\nAppend a new dated section headed "${pass1Marker}" to ${REVIEW} (never overwrite a prior pass's section) with your PASS / PASS-with-limitations / FAIL verdict and tagged findings (Blocking / Deferrable / Note, each with an impact estimate). You may spot-check a specific fact or number where your argument depends on one, but do not redo full verification.`,
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
    `${ANCHOR}\n\nFix pass. Read the "${pass1Marker}" section of ${REVIEW} and address its Blocking findings (and, at your judgment, Deferrable ones) in ${NOTEBOOK} — and src/arty/ only if a finding requires it. Scoped to the flagged items only.`,
    { label: `modeler:fix-${cyclesUsed}`, phase: 'Fix', agentType: 'modeler' }
  )
  phase('Review: Adversarial')
  pass1Marker = `Adversarial critique re-review ${cyclesUsed} — ${args.thread}/${args.questionSlug}`
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
  let pass2Marker = `Verification — ${args.thread}/${args.questionSlug}`
  pass2 = await agent(
    `${ANCHOR}\n\nVerification pass (Pass 2 of Workflow A review) on ${NOTEBOOK}. Pass 1 (adversarial critique) already ran and settled — read its section(s) of ${REVIEW} for context, do not redo it. Reproduce every check script standalone and confirm its output matches what the notebook reports; trace the load-bearing code path by hand; confirm cited numbers against their primaries rather than the notebook's word.\n\nAppend a new dated section headed "${pass2Marker}" to ${REVIEW} with your own verdict and tagged findings.`,
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
      `${ANCHOR}\n\nFix pass. Read the "${pass2Marker}" section of ${REVIEW} and address its Blocking findings (and, at your judgment, Deferrable ones) in ${NOTEBOOK} — and src/arty/ only if a finding requires it. Scoped to the flagged items only.`,
      { label: `modeler:fix-${cyclesUsed}`, phase: 'Fix', agentType: 'modeler' }
    )
    phase('Review: Verification')
    pass2Marker = `Verification re-review ${cyclesUsed} — ${args.thread}/${args.questionSlug}`
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
  log(`Stopping — ${escalate.reason}. Escalating rather than looping a third time (the fix-cycle cap is shared across both review passes).`)
  return { thread: args.thread, questionSlug: args.questionSlug, status: 'escalate', cyclesUsed, escalate, pass1, pass2 }
}

log('Review passed. Remaining step (outside this workflow): the main agent links the challenge from the parent .qmd "Challenges" section if reader-relevant, and updates challenges/README.md (and the thread README, if it has one) with the verdict — a documentation-index edit, not a modeler dispatch.')

return {
  thread: args.thread,
  questionSlug: args.questionSlug,
  status: 'done',
  cyclesUsed,
  pass1Verdict: pass1.verdict,
  pass2Verdict: pass2.verdict,
}
