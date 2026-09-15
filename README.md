# A2W

A2W (Anti-AI Writer) is an evidence-first writing skill for AI agents. It
checks and edits formulaic prose while preserving facts, meaning, technical
terms, and the author's legitimate voice.

The project targets Agent Skills-compatible clients, including Codex, Claude
Code, and Kiro.

## Status

Pre-release. The portable skill is under `skills/a2w`.

## Modes

```text
$a2w plan <writing task>
$a2w check <file or prose>
$a2w edit <file or prose>
$a2w explain <file or prose>
```

Claude Code and Kiro use `/a2w` instead of `$a2w`.

## Install from GitHub

After this repository is published, install it into a project with:

```bash
npx skills add <github-owner>/a2w --skill a2w \
  -a codex -a claude-code -a kiro-cli -y
```

Add `-g` for a global installation.

## Local checker

```bash
python3 skills/a2w/scripts/lint_prose.py path/to/document.md
```

Findings are editorial review prompts. They are not evidence of AI authorship.

## Licence

MIT License. You may use, copy, modify, and redistribute A2W, including for
commercial use, as long as the copyright and licence notice remain included.
See `LICENSE`.
