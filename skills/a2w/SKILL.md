---
name: a2w
description: Draft, rewrite, or review prose to remove generic, inflated, repetitive, and formulaic writing while preserving facts, intent, voice, and necessary technical detail. Use for reports, documentation, emails, articles, explanations, and other prose; do not apply its style rules to code or verbatim quotations.
license: Apache-2.0
metadata:
  version: "0.1.0"
  compatibility: "Agent Skills-compatible clients; optional checker requires Python 3.9+"
---

# A2W

A2W means Anti-AI Writer.

Produce writing that is specific, useful, and faithful to the available
evidence. The goal is editorial quality, not hiding AI use or defeating an AI
detector.

## Select a mode

Treat the first word after the skill invocation as a mode when it matches one
of these:

- `plan`: establish the writing contract, evidence needs, structure, and risks
  without drafting unless requested;
- `check`: report concrete issues and their locations without rewriting;
- `edit`: return revised prose while preserving meaning and evidence;
- `explain`: explain reported issues and possible corrections without applying
  them.

When no mode is supplied, infer the least invasive action from the request. Do
not silently rewrite text when the user asks only for evaluation.

## Establish the writing contract

Infer or preserve:

- purpose and audience;
- document type and requested length;
- author voice and level of formality;
- locale and spelling convention;
- facts, quotations, citations, results, uncertainty, and technical terms that
  must not change.

Do not impose first person, contractions, informality, Australian spelling, or
another stylistic preference unless the user, source text, or context supports
it.

## Draft or revise

Lead with the answer, result, or actual subject. Give each paragraph a distinct
job and use headings or lists only when they make the material easier to
navigate.

Prefer:

- concrete actors, actions, mechanisms, examples, quantities, and constraints;
- plain verbs and direct sentence construction;
- explicit priorities and trade-offs;
- natural variation that follows the content;
- wording that fits this author and this situation.

Remove text that merely announces importance, repeats the request, previews
obvious structure, paraphrases a point already made, or could be transferred
unchanged to an unrelated subject.

Never invent evidence, citations, quotations, personal experience, results,
opinions, or biographical details to make writing appear human. When the source
material is too thin to support a substantive rewrite, retain the limitation,
flag the gap, or ask for evidence instead of filling it with plausible prose.

## Review proportionately

For a short ordinary edit, review directly. For a substantial draft, suspected
formulaic prose, or an explicit anti-slop review, read
[references/patterns.md](references/patterns.md).

The optional checker provides diagnostic prompts:

```bash
python3 scripts/lint_prose.py <file>
```

Treat its findings as review cues, not errors or proof of AI authorship. A
phrase is acceptable when it is the clearest accurate wording in context.

## Fidelity pass

Before returning the prose:

1. Compare every factual claim, number, source, quotation, and stated result
   with the supplied material.
2. Preserve calibrated uncertainty and distinguish fact from inference.
3. Check that edits did not erase the author's distinctive but legitimate
   voice or literal domain terminology.
4. Cut repeated conclusions, filler, decorative formatting, and unnecessary
   sections.
5. Read representative paragraphs for cadence; fix mechanical repetition
   without introducing artificial quirks, fragments, or mistakes.

For academic work, improve clarity and help the user express work they
understand. Do not misrepresent authorship, fabricate participation, or help
evade an institution's disclosure or integrity requirements.
