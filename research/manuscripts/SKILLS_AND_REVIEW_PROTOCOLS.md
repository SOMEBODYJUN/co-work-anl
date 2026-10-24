# Review and writing tools used for the manuscript pass

This file records the open-source skill snapshots used in the current review
round. The repositories themselves stay outside this research repository; this
manifest makes the round reproducible without mixing third-party Git history
into the mathematical assets.

| Purpose | Repository | Pinned commit | Files used in this round |
| --- | --- | --- | --- |
| Mathematical manuscript structure and prose | [math-paper-skills](https://github.com/haruhisa-enomoto/math-paper-skills) | `eb54308071a4dfef0ce4561e4b5009bd835ecdf8` | `write-research-paper`, `read-research-paper`, `polish-math-prose` |
| Proof correctness audit | [math-proof-review](https://github.com/XunZhiyang/math-proof-review) | `a14305f7b1c0cf68401fd00e8964248c41cdee42` | `SKILL.md`, `protocol/review-protocol.md`, proof-sanity scripts |
| Whole-paper referee checklist | [paper-review-skill](https://github.com/guruvamsi-policharla/paper-review-skill) | `5c4811fff4a35752dcdeda180c191d4a8ba5613b` | `skills/paper-review/SKILL.md` |
| General humanization pass | [humanize](https://github.com/harshaneel/humanize) | `9c3dec34dc8e0ed9d26de14a869900a714da8f9e` | humanization rules and academic-register safeguards |
| Academic-register humanization | [Academic-Humanizer](https://github.com/mbagoezmiftah/Academic-Humanizer) | `6899e8dad48cab45634fa8dd9daa1c3fd9d3bc60` | `SKILL.md` |

The proof-review protocol requires a constructive pass and an independent
adversarial pass. Referee reports in this directory therefore record what was
actually re-derived, what remains plausible but unverified, and what is only an
expository suggestion. A prose pass may remove repetition or template-like
phrasing, but it must preserve labels, formulas, quantifiers, hypotheses, and
claim status. Humanization is never evidence of mathematical correctness or
of journal acceptance.

The clones can be recreated from the manifest with:

```sh
git clone https://github.com/haruhisa-enomoto/math-paper-skills.git
git clone https://github.com/XunZhiyang/math-proof-review.git
git clone https://github.com/guruvamsi-policharla/paper-review-skill.git
git clone https://github.com/harshaneel/humanize.git
git clone https://github.com/mbagoezmiftah/Academic-Humanizer.git
```
