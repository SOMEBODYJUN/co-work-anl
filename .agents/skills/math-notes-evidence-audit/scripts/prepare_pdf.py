#!/usr/bin/env python3
"""Render every physical PDF page and an overlapping 2 × 3 region inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil

import fitz
from PIL import Image


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def region_boxes(width: int, height: int, overlap: float) -> list[tuple[int, int, list[int]]]:
    """Integer boxes include the entire page; padding is shared by adjacent cells."""
    pad_x = math.ceil(width / 2 * overlap / 2)
    pad_y = math.ceil(height / 3 * overlap / 2)
    result = []
    for row in range(3):
        for column in range(2):
            x0 = max(0, column * width // 2 - pad_x)
            x1 = min(width, max(x0 + 1, (column + 1) * width // 2 + pad_x))
            y0 = max(0, row * height // 3 - pad_y)
            y1 = min(height, max(y0 + 1, (row + 1) * height // 3 + pad_y))
            result.append((row + 1, column + 1, [x0, y0, x1, y1]))
    return result


def prepare(pdf_path: Path, output: Path, dpi: int = 220, overlap: float = 0.08) -> Path:
    if not 36 <= dpi <= 1200:
        raise ValueError("dpi must be between 36 and 1200")
    if not 0 <= overlap <= 0.45:
        raise ValueError("overlap must be between 0 and 0.45")
    pdf_path = pdf_path.resolve()
    output = output.resolve()
    # Do not silently replace an earlier review's image inventory.
    if output.exists() and any(output.iterdir()):
        raise ValueError("output directory must be new or empty")
    with fitz.open(pdf_path) as document:
        if document.needs_pass:
            raise ValueError("encrypted PDF requires an unlocked input")
        count = document.page_count
        if count == 0:
            raise ValueError("PDF has no pages")
        output.mkdir(parents=True, exist_ok=True)
        (output / "pages").mkdir()
        (output / "regions").mkdir()
        source = output / "source.pdf"
        shutil.copyfile(pdf_path, source)
        manifest = {
            "schema_version": "1.0",
            "source_pdf": {"path": "source.pdf", "sha256": sha256_file(source),
                           "original_name": pdf_path.name, "page_count": count},
            "render": {"dpi": dpi, "columns": 2, "rows": 3,
                       "overlap_fraction": overlap, "pymupdf_version": fitz.VersionBind},
            "pages": [],
        }
        for number, page in enumerate(document, 1):
            page_id = f"p{number:04d}"
            pixmap = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB, alpha=False)
            full = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            page_path = Path("pages") / f"{page_id}.png"
            full.save(output / page_path)
            entry = {"id": page_id, "number": number, "width_px": full.width,
                     "height_px": full.height,
                     "image": {"path": page_path.as_posix(),
                               "sha256": sha256_file(output / page_path),
                               "bbox_px": [0, 0, full.width, full.height]},
                     "regions": []}
            for row, column, bbox in region_boxes(full.width, full.height, overlap):
                region_id = f"{page_id}-r{row}c{column}"
                relative = Path("regions") / f"{region_id}.png"
                crop = full.crop(bbox)
                crop.save(output / relative)
                histogram = crop.convert("L").histogram()
                # This hint is deliberately never a blank-page decision.
                candidate = sum(histogram[:235]) / (crop.width * crop.height) <= 0.00001
                entry["regions"].append({
                    "id": region_id, "row": row, "column": column, "bbox_px": bbox,
                    "image": {"path": relative.as_posix(),
                              "sha256": sha256_file(output / relative)},
                    "blank_candidate": candidate, "blank_status": "unreviewed",
                })
            manifest["pages"].append(entry)
        destination = output / "manifest.json"
        destination.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=220)
    parser.add_argument("--overlap", type=float, default=0.08,
                        help="fraction of one cell shared across a boundary (default 0.08)")
    args = parser.parse_args()
    try:
        print(prepare(args.pdf, args.out, args.dpi, args.overlap))
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(1, f"prepare_pdf: {error}\n")


if __name__ == "__main__":
    main()
