# A2W

A2W (Anti-AI Writer) is an evidence-first writing skill for AI agents. It
reviews and edits formulaic prose while preserving facts, meaning, technical
terms, and the author's legitimate voice.

The project targets Agent Skills-compatible clients, including Codex, Claude
Code, and Kiro.

## Status

Current pre-release: **v0.2.0**. The portable skill is under `skills/a2w`.

## Version history

| Version | Date | Changes |
|---|---|---|
| 0.2.0 | 2026-09-15 | Renamed `check` to `review`. Review findings now include a brief explanation, so the separate `explain` command was removed. |
| 0.1.0 | 2026-09-15 | Initial pre-release with `plan`, `check`, `edit`, and `explain`, plus the deterministic prose checker. |

## How A2W activates

When A2W is installed globally, an agent can select it automatically for
requests involving reports, documentation, articles, emails, explanations, or
other prose:

```text
Write a technical report about this project.
Draft an email to my lecturer.
Rewrite this README so it is clearer.
```

An explicit command guarantees that A2W is used and selects a specific mode.
Codex uses `$a2w`; Claude Code and Kiro use `/a2w`.

```text
# Codex
$a2w review report.md

# Claude Code or Kiro
/a2w review report.md
```

Text after the command tells A2W which mode to use and what content or file to
work with.

## Commands

### `plan`

Use `plan` before writing a substantial document. A2W identifies the audience,
purpose, evidence, constraints, structure, and likely writing risks. A2W drafts
only when the request also asks for a draft.

```text
$a2w plan a 1,500-word university report about my IoT weather pipeline
```

```text
/a2w plan a migration guide for developers moving from API v1 to v2
```

The plan should cover:

- who will read the document;
- what the reader needs to learn or decide;
- which facts, results, quotations, and sources are available;
- which information is still missing;
- a proportionate section structure;
- terminology, locale, tone, and length requirements.

`plan` does not invent evidence to fill gaps. It identifies what the author
needs to provide.

### `review`

Use `review` for diagnosis without rewriting. A2W reports specific problems,
points to the affected passage, briefly explains why each problem matters, and
suggests a direction for improvement.

```text
$a2w review report.md
```

```text
/a2w review "This platform provides a complete solution for modern teams..."
```

A review can identify:

- generic claims that could describe an unrelated project;
- unsupported significance, authority, numbers, or conclusions;
- repeated ideas and unnecessary summaries;
- canned openings and mechanical transitions;
- excessive headings, bullets, bold text, or structural symmetry;
- inflated wording, stacked hedges, and empty filler;
- uniform sentence or paragraph rhythm;
- changes that could damage technical accuracy or the author's voice.

`review` leaves the source unchanged. Each finding should contain:

```text
Location: paragraph 3
Issue: Generic claim
Reason: The sentence does not identify a benefit or supporting result.
Direction: Add the measured interval, stored fields, or dashboard outcome.
```

### `edit`

Use `edit` to revise prose. A2W removes formulaic writing while preserving
facts, quotations, citations, uncertainty, technical terms, and legitimate
voice.

```text
$a2w edit README.md
```

```text
/a2w edit this email for a professional but direct tone:
<paste email>
```

During an edit, A2W:

1. establishes the audience, purpose, format, and requested voice;
2. protects facts and other content that must not change;
3. replaces vague claims with supplied specifics where possible;
4. removes repetition, filler, puffery, and unnecessary structure;
5. checks the revision against the original for factual drift.

If the source lacks evidence, A2W keeps the limitation visible or asks for the
missing information. A2W never creates statistics, citations, quotations,
results, opinions, or personal experiences.

When working in an agent with file access, ask for a preview if you do not want
the file changed:

```text
$a2w edit report.md and show the proposed revision without modifying the file
```

### No mode

The mode can be omitted:

```text
$a2w rewrite this project summary for a technical audience
```

When no recognised mode is supplied, A2W infers the least invasive action from
the request. A request to review should not silently become a rewrite.

## Planned profile commands

These commands are planned and are not implemented in the current release:

```text
/a2w setup
/a2w profile show
/a2w profile edit
/a2w profile reset
```

The planned setup flow will create an optional project profile under
`.a2w/profile.yaml`. Profiles will describe the audience, role, locale,
formality, formatting preferences, and writing characteristics that A2W should
preserve. The core skill will continue to work without a profile.

## Install from GitHub

Install A2W into the current project for Codex, Claude Code, and Kiro:

```bash
npx skills add Hee1ko/a2w --skill a2w \
  -a codex -a claude-code -a kiro-cli -y
```

Install it globally by adding `-g`:

```bash
npx skills add Hee1ko/a2w --skill a2w \
  -a codex -a claude-code -a kiro-cli -g -y
```

## Local checker

The bundled checker performs deterministic phrase and rhythm checks:

```bash
python3 skills/a2w/scripts/lint_prose.py path/to/document.md
```

It can report canned openings, throat-clearing, inflated wording, formulaic
contrasts, repeated sentence openings, and unusually uniform rhythm. Findings
are editorial review prompts. They are not errors or evidence of AI authorship.

The checker does not rewrite files:

```text
Advisory findings (review in context):
- line 4: throat-clearing phrase
- line 9: unsupported significance claim
```

## Writing safeguards

A2W follows these rules in every mode:

- preserve supplied facts, numbers, quotations, citations, and results;
- distinguish verified facts from inference and uncertainty;
- preserve necessary technical terminology;
- do not invent personal experience or biographical details;
- do not deliberately add mistakes or awkward phrasing to appear human;
- treat pattern matches as review prompts rather than forbidden words;
- respect academic integrity and disclosure requirements.

## Licence

MIT License. You may use, copy, modify, and redistribute A2W, including for
commercial use, as long as the copyright and licence notice remain included.
See `LICENSE`.
