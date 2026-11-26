"""Render the original P6 hand strokes outside its clipped left edge."""

import hashlib
import json
from pathlib import Path

import fitz
import numpy as np


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    proposal = Path(__file__).resolve().parent
    project = proposal.parents[1]
    source = project / "source.pdf"
    source_hash = sha256(source.read_bytes())
    original_media = fitz.Rect(0, 0, 595, 842)
    expanded_media = fitz.Rect(-9, 0, 595, 842)
    clip = fitz.Rect(0, 433.02, 100, 471)
    original_form_bbox = "[0 0 2380 3368]"
    expanded_form_bbox = "[-36 0 2380 3368]"
    original_form_clip = b"0 0 2380 3368 re\nW* n\n"
    expanded_form_clip = b"-36 0 2416 3368 re\nW* n\n"
    dpi = 1200
    render_options = {
        "dpi": dpi,
        "clip": clip,
        "colorspace": fitz.csRGB,
        "alpha": False,
    }

    with fitz.open(source) as document:
        page = document[5]
        assert page.mediabox == original_media
        (xref, name, _, _) = page.get_xobjects()[0]
        assert (xref, name) == (33, "FXX1")
        assert document.xref_get_key(xref, "BBox") == ("array", original_form_bbox)
        original_stream = document.xref_stream(xref)
        assert original_stream.count(original_form_clip) == 1
        original_paths = original_stream.split(b"\nf\n")
        drawings = page.get_drawings()
        off_page_path_indices = [
            drawing["seqno"]
            for drawing in drawings
            if drawing["rect"].x0 < 0 and 433 < drawing["rect"].y0 < 471
        ]
        assert off_page_path_indices == [2, 4, 5]
        path_evidence = [
            {
                "fill_path_index": i,
                "original_bbox_pdf_pt_top_left": list(drawings[i]["rect"]),
                "path_bytes": len(original_paths[i]),
                "path_sha256": sha256(original_paths[i]),
            }
            for i in off_page_path_indices
        ]

        page.set_mediabox(expanded_media)
        media_only = page.get_pixmap(**render_options)

        expanded_stream = original_stream.replace(original_form_clip, expanded_form_clip, 1)
        document.xref_set_key(xref, "BBox", expanded_form_bbox)
        document.update_stream(xref, expanded_stream)
        stored_stream = document.xref_stream(xref)
        assert stored_stream.replace(expanded_form_clip, original_form_clip, 1) == original_stream
        stored_paths = stored_stream.split(b"\nf\n")
        for i in off_page_path_indices:
            assert stored_paths[i] == original_paths[i]

        page = document.reload_page(page)
        expanded = page.get_pixmap(**render_options)

    assert sha256(source.read_bytes()) == source_hash
    assert (media_only.width, media_only.height) == (expanded.width, expanded.height)
    raster_shape = expanded.height, expanded.width, 3
    left_edge_x = round(-expanded_media.x0 * dpi / 72)
    before = np.frombuffer(media_only.samples, dtype=np.uint8).reshape(raster_shape)
    after = np.frombuffer(expanded.samples, dtype=np.uint8).reshape(raster_shape)
    changed_y, changed_x = np.nonzero((before != after).any(axis=2))
    first_ink_before = np.nonzero((before != 255).any(axis=2))[1].min()
    first_ink_after = np.nonzero((after != 255).any(axis=2))[1].min()
    # Extending the clip also changes edge coverage in the first two in-page columns.
    assert int(changed_x.max()) <= left_edge_x + 1
    assert first_ink_after < left_edge_x <= first_ink_before

    expanded_path = proposal / "crops/p0006-supplement-left-fully-unclipped-1200.png"
    media_only_path = proposal / "crops/p0006-supplement-left-media-only-1200.png"
    expanded.save(expanded_path)
    media_only.save(media_only_path)
    record = {
        "source_file": "source.pdf",
        "source_sha256": source_hash,
        "page_id": "p0006",
        "render_clip_shifted_pdf_pt": list(clip),
        "render_dpi": dpi,
        "media_original_pdf_pt": list(original_media),
        "media_expanded_pdf_pt": list(expanded_media),
        "form_xref": xref,
        "form_bbox_original": original_form_bbox,
        "form_bbox_expanded": expanded_form_bbox,
        "form_stream_clip_original": original_form_clip.decode().strip(),
        "form_stream_clip_expanded": expanded_form_clip.decode().strip(),
        "form_stream_original_sha256": sha256(original_stream),
        "form_stream_expanded_sha256": sha256(stored_stream),
        "drawing_paths_unchanged": path_evidence,
        "original_px_x0_in_expanded_crop": left_edge_x,
        "baseline_min_ink_x": int(first_ink_before),
        "expanded_min_ink_x": int(first_ink_after),
        "changed_pixel_count": int(len(changed_x)),
        "changed_bbox_px_half_open": [
            int(changed_x.min()),
            int(changed_y.min()),
            int(changed_x.max()) + 1,
            int(changed_y.max()) + 1,
        ],
        "changed_pixel_count_outside_media": int((changed_x < left_edge_x).sum()),
        "path": str(expanded_path.relative_to(project)),
        "sha256": sha256(expanded_path.read_bytes()),
        "media_only_path": str(media_only_path.relative_to(project)),
        "media_only_sha256": sha256(media_only_path.read_bytes()),
        "note": "仅在内存改变裁框，未保存 PDF 或改写绘画路径。像素变化局限在左裁边与相邻两列抗锯齿像素。这些是页外补证。",
    }
    (proposal / "supplemental-outside-page-evidence.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
