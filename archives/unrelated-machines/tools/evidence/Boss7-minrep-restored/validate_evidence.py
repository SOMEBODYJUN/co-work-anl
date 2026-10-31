#!/usr/bin/env python3
"""Check preserved evidence and scalar arithmetic; not a proof verifier."""
import hashlib
import json
from decimal import Decimal, getcontext
from pathlib import Path

import fitz
from PIL import Image


def main():
    directory = Path(__file__).resolve().parent
    pdf = directory / "original/manurangsi_minrep_degree_1807_00936v1.pdf"
    raw = pdf.read_bytes()
    assert len(raw) == 134108
    assert hashlib.sha256(raw).hexdigest() == "259edd7e850da816ddb5c318287a7a3a525ccc8963f07918787156384d7153d8"
    with fitz.open(pdf) as document:
        assert len(document) == 9
    extracted = (directory / "original/manurangsi-v1-layout.txt").read_text()
    for phrase in ["Theorem 1", "Theorem 2", "Corollary 3", "Theorem 4", "Corollary 5", "Theorem 6", "Lemma 7", "Proposition 8", "Lemma 9", "Lemma 10", "Proposition 11", "Proposition", "Discussions and Open Questions", "References"]:
        assert phrase in extracted, phrase
    images = sorted((directory / "rendered").glob("*.png"))
    assert len(images) == 11
    for path in images:
        with Image.open(path) as picture:
            picture.verify()
        with Image.open(path) as picture:
            picture.load()
    getcontext().prec = 60
    coefficient = Decimal("0.3") - Decimal("0.2") * Decimal("2.5").ln()
    assert coefficient > Decimal("0.1")
    delta_exponent = Decimal("0.0001") * coefficient
    assert delta_exponent > Decimal("0.00001")
    # Gamma=(5/4)*2^-11*g^-2, so this is the ratio to g.
    downstream_gap_ratio = Decimal("0.03") * (Decimal(2048) / Decimal("1.25")).sqrt()
    assert downstream_gap_ratio > 1
    output = {
        "status": "PASS",
        "meaning": "Evidence integrity and scalar arithmetic only; no formal theorem validation or production algorithm run.",
        "source_pdf_sha256": hashlib.sha256(raw).hexdigest(),
        "source_pdf_bytes": len(raw),
        "source_pdf_pages": 9,
        "decoded_png_count": len(images),
        "sharp_tail_coefficient": str(coefficient),
        "coefficient_of_Delta_n": str(delta_exponent),
        "minzer_zheng_local_parameter_repair_gap_divided_by_g": str(downstream_gap_ratio),
    }
    (directory / "validation.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
