#!/usr/bin/env python3
"""Funniest One-Line Out-of-Office Reply.

The joke, in two beats:
  setup  -- I'm out until Monday, and my auto-reply is covering for me;
  punch  -- so the sender's email is now being ignored by two of us
            instead of one. The auto-reply, the thing meant to help,
            joins in the ignoring. That escalation is the whole laugh,
            and it still reads like a real out-of-office note: a return
            day, a covering arrangement, no setup the reader must learn.

Candidates I rejected, and why:
  - the auto-reply being "also out of office" is the same meta joke
    but lands softer, with no second person doing the ignoring;
  - "scream into the void" is vivid but the void is a stranger to an
    office inbox, and it drops the return day;
  - a laptop left at 3% is a nice image but the punch is about the
    laptop, not about being away.

The program assembles the chosen line from its two sentences, checks
it against the gate (UTF-8, one line, 1 to 160 characters), and writes
it to /output/entry.txt with one trailing newline. Standard library
only, no network, no randomness, no clock: every run is byte-identical.
"""

import os
import sys


SETUP = "I'm out of office until Monday."
PUNCH = "My auto-reply is covering for me, so your email is now being ignored by two of us."
MAX_CHARS = 160


def assemble_reply():
    sentences = [SETUP, PUNCH]
    reply = " ".join(sentences)
    reply = reply.strip()
    problems = []
    if not reply:
        problems.append("reply is empty")
    if len(reply) > MAX_CHARS:
        problems.append("reply is %d characters, over the %d limit" % (len(reply), MAX_CHARS))
    if "\n" in reply or "\r" in reply:
        problems.append("reply must be a single line")
    if "  " in reply:
        problems.append("reply has a double space")
    if not reply.endswith("."):
        problems.append("reply should end with a full stop")
    if "Monday" not in reply:
        problems.append("reply must name the return day, or it is not an out-of-office note")
    if problems:
        sys.stderr.write("invalid reply: " + "; ".join(problems) + "\n")
        raise SystemExit(1)
    return reply


def main():
    reply = assemble_reply()
    destination = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(destination, exist_ok=True)
    with open(os.path.join(destination, "entry.txt"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(reply + "\n")


if __name__ == "__main__":
    main()
