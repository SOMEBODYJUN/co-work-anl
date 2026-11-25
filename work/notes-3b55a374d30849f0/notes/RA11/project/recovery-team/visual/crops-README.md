# RA11 visual crop README

All target crops were cut from the existing 800-dpi full-page renders in `autonomous-recovery/crops/` (full page dimensions 6612×9356), using coordinates first identified on the 400-dpi page images. Coordinates below are **400-dpi page pixels**; the actual PNG dimensions are doubled. No crop contains edits or markup added by this reviewer.

| crop | source page | 400-dpi bbox `[x0,y0,x1,y1]` | render | purpose |
|---|---|---:|---:|---|
| `target-crops/RA11-P001-U01-formula-800dpi.png` | `p0001` | `[80,700,2900,1800]` | 800 dpi | partition formula, endpoint index and nearby inequalities |
| `target-crops/RA11-P001-U01-grid-800dpi.png` | `p0001` | `[2400,650,3306,1800]` | 800 dpi | right-side dyadic grid/axis and terminal index adjacency |
| `target-crops/RA11-P005-U01-tail-800dpi.png` | `p0005` | `[40,500,3260,1900]` | 800 dpi | full Egoroff tail-set line across the page |
| `target-crops/RA11-P005-U01-left-tail-800dpi.png` | `p0005` | `[0,500,1800,1600]` | 800 dpi | left page-edge overbar and start of union |
| `target-crops/RA11-P005-U01-right-tail-800dpi.png` | `p0005` | `[1400,500,3260,1600]` | 800 dpi | right continuation, braces, threshold condition and measure line |

The 800-dpi view resolved the visible strokes for both issues; escalation to 1200 dpi was not necessary.

## Complete visual inventory

`../blind-read.md` contains the first-pass full-page record and one row for each of all 84 overlap regions, including physical page number, manifest bbox, and content/blank observation. `region-sheets/` contains page-by-page 6-tile contact sheets used during the pass.
