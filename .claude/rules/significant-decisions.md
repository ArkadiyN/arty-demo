# Significant-Decision Gate

Applies to **every agent** (main conversation and subagents), in every
workflow. Separate a decision from its execution **when the decision is
significant** — otherwise just proceed.

## When to pause

Pause and surface the decision only when **both** hold:

1. **It is significant** — either *hard to reverse* (commits, deletions,
   shared-file rewrites, schema/spec changes, outward or external actions,
   costly/irreversible subagent delegations) **or** it *materially changes
   direction or output*; and
1. **Confidence is genuinely low** — you do not have a clearly correct choice.

When both hold: STOP before acting. State the options and your recommendation,
then wait. Having a plausible default is **not** a licence to skip the
question.

## When NOT to pause (this is not "grill-me")

For low-stakes, reversible, or conventional choices, **pick the sensible
default, state it in one line so it can be corrected, and proceed.** Do not
interrogate every step. The goal is catching the few consequential forks, not
adding friction to routine work.

## Litmus

Would a wrong guess here cost more than a one-line question? If yes and you are
unsure — ask. If no — decide, note the choice, and keep moving.
