"""Versioned, offline references for judging the standing of a math problem.

These comparisons concern the *problem before its resolution*. They supply no
evidence that a manuscript's result is new, correct or as broad as the problem.
"""
from __future__ import annotations

VERSION = "vibemathed-v2-2026-08-06"
METHODOLOGY = "https://vibemathed.com/methodology"
RUBRIC = "https://vibemathed.com/significance-prompt.md"
RUBRIC_SHA256 = "d289f532078f0c313ed452f185ec775c358af674ae75108d87ad61844b23b530"
DATASET = "https://vibemathed.com/api/dataset"
DATA_LICENSE = "https://vibemathed.com/data-license"

# VibeMathed's v2 prompt fixes the IDs and scores. Display titles below come
# from the corresponding snapshot rows. Only editorial metadata is retained;
# no claimed resolutions, validation statuses, or third-party text are used.
_ANCHORS = (
    ("jacobian-conjecture", 65, "Jacobian Conjecture"),
    ("cycle-double-cover-conjecture", 55, "Cycle Double Cover Conjecture"),
    ("connes-rigidity-conjecture", 45, "Connes' Rigidity Conjecture"),
    ("erdos-planar-unit-distance", 40, "Erdős's Planar Unit Distance Conjecture"),
    ("feiges-conjecture", 35, "Feige's Conjecture"),
    (
        "kannan-tetali-vempala-conjecture",
        30,
        "Kannan–Tetali–Vempala conjecture (bipartite/binary-matrix case)",
    ),
    ("banks-martin-primitive-sets", 25, "The Banks-Martin Conjecture on Primitive Sets"),
    (
        "babai-frankl-oddtown-composite",
        20,
        "Babai and Frankl's Oddtown Question for Composite Moduli",
    ),
    ("erdos-1196-primitive-sets", 15, "Erdős Problem #1196: Primitive Sets"),
    ("erdos-1217", 10, "Erdős Problem #1217"),
    ("graffiti-residue-common-divisor", 5, "Graffiti's Residue Problem for Common-Divisor Graphs"),
)


def anchor_catalog() -> dict:
    """Return fresh JSON-serializable metadata; loading it never uses the network."""
    return {
        "version": VERSION,
        "methodology": METHODOLOGY,
        "rubric": RUBRIC,
        "rubric_sha256": RUBRIC_SHA256,
        "attribution": "VibeMathed (vibemathed.com), editorial data under CC BY 4.0",
        "license_url": DATA_LICENSE,
        "dataset_check": {
            "url": DATASET,
            "generated_utc": "2026-11-24T05:44:46.020Z",
            "matched_count": len(_ANCHORS),
            "score_discrepancies": [],
        },
        "calibration_scope": (
            "Compare the underlying problem's standing before the work. Identify the exact "
            "statement and keep the manuscript's proven scope separate. Never infer scope "
            "or verification from a related entry, title, or search hit."
        ),
        "anchors": [
            {
                "id": slug,
                "score": score,
                "title": title,
                "url": f"https://vibemathed.com/problem/{slug}",
            }
            for slug, score, title in _ANCHORS
        ],
        "scale_reference": {
            "id": "riemann-hypothesis",
            "score": 100,
            "title": "Riemann Hypothesis",
            "url": "https://www.claymath.org/millennium/riemann-hypothesis/",
            "role": "rubric ceiling; not one of the eleven catalog anchors",
        },
    }
