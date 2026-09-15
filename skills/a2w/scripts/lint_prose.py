#!/usr/bin/env python3
"""A2W advisory checks for formulaic prose. Findings are not authorship evidence."""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from pathlib import Path


PHRASES = {
    "canned opening": (
        r"\bin today'?s (?:rapidly |ever[- ]?)?(?:changing|evolving|fast[- ]paced)\b",
        r"\bthis (?:article|report|essay|response) (?:will|aims to)\b",
        r"\b(?:let us|let's) (?:delve|dive|explore|unpack)\b",
    ),
    "throat-clearing": (
        r"\bit is (?:important|worth) (?:to )?(?:note|noting|remembering)\b",
        r"\bat its core\b",
        r"\bwhen it comes to\b",
        r"\bthe fact that\b",
        r"\bin order to\b",
        r"\bhere'?s the thing\b",
        r"\blet'?s be clear\b",
    ),
    "significance inflation": (
        r"\bplays? a (?:pivotal|crucial|vital|significant) role\b",
        r"\bstands? as a testament\b",
        r"\bunderscores? (?:the|its) importance\b",
        r"\bmarks? a significant milestone\b",
        r"\b(?:game[- ]changing|transformative|cutting[- ]edge)\b",
    ),
    "stock abstraction": (
        r"\b(?:ever[- ]evolving|dynamic) landscape\b",
        r"\bin the realm of\b",
        r"\b(?:intricate|multifaceted) tapestry\b",
        r"\ba myriad of\b",
        r"\ba plethora of\b",
    ),
    "inflated wording": (
        r"\b(?:leverage|utili[sz]e)\b",
        r"\bfacilitate\b",
        r"\bshowcase\b",
        r"\b(?:robust|seamless|comprehensive) solution\b",
        r"\bserves as\b",
    ),
    "formulaic contrast": (
        r"\bnot (?:only|just) .{1,100}\bbut (?:also )?\b",
        r"\bit (?:is|isn't|is not|was|wasn't|was not) (?:just )?.{1,100}[;,.] "
        r"(?:it is|it's|it was)\b",
    ),
    "conclusion label": (
        r"\bin conclusion\b",
        r"\bkey takeaway\b",
        r"\bto sum up\b",
    ),
}

SENTENCE_RE = re.compile(r"(?<=[.!?])(?:[\"')\]]*)\s+")
WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def phrase_findings(text: str) -> list[str]:
    findings: list[str] = []
    for category, patterns in PHRASES.items():
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                excerpt = re.sub(r"\s+", " ", match.group(0)).strip()
                findings.append(
                    f"line {line_number(text, match.start())}: "
                    f"{category}: {excerpt!r}"
                )
    return findings


def sentence_metrics(text: str) -> list[str]:
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    sentences = [
        sentence.strip()
        for sentence in SENTENCE_RE.split(prose)
        if len(WORD_RE.findall(sentence)) >= 3
    ]
    lengths = [len(WORD_RE.findall(sentence)) for sentence in sentences]
    findings: list[str] = []

    if len(lengths) >= 6:
        mean = statistics.mean(lengths)
        deviation = statistics.pstdev(lengths)
        if mean >= 8 and deviation / mean < 0.22:
            findings.append(
                "rhythm: sentence lengths are unusually uniform "
                f"(mean {mean:.1f} words, standard deviation {deviation:.1f}); "
                "review cadence without forcing artificial variation"
            )

    starts: dict[str, list[int]] = {}
    for index, sentence in enumerate(sentences, start=1):
        words = [word.lower() for word in WORD_RE.findall(sentence)]
        if len(words) >= 2:
            starts.setdefault(" ".join(words[:2]), []).append(index)
    for start, positions in sorted(starts.items()):
        if len(positions) >= 3:
            findings.append(
                f"repetition: {len(positions)} sentences begin with "
                f"{start!r} (sentences {', '.join(map(str, positions))})"
            )

    return findings


def paragraph_metrics(text: str) -> list[str]:
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
        and not paragraph.lstrip().startswith(("#", "```", "|"))
    ]
    lengths = [len(WORD_RE.findall(paragraph)) for paragraph in paragraphs]
    if len(lengths) < 5 or statistics.mean(lengths) < 20:
        return []
    mean = statistics.mean(lengths)
    deviation = statistics.pstdev(lengths)
    if deviation / mean < 0.18:
        return [
            "structure: paragraph lengths are unusually uniform "
            f"(mean {mean:.1f} words, standard deviation {deviation:.1f})"
        ]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report advisory anti-slop findings for a prose file."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="UTF-8 text/Markdown file; omit to read standard input",
    )
    args = parser.parse_args()

    try:
        text = (
            Path(args.file).read_text(encoding="utf-8")
            if args.file
            else sys.stdin.read()
        )
    except (OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    findings = (
        phrase_findings(text) + sentence_metrics(text) + paragraph_metrics(text)
    )
    if not findings:
        print("No advisory patterns found.")
        return 0

    print("Advisory findings (review in context):")
    for finding in findings:
        print(f"- {finding}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
