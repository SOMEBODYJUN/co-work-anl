# RA10 visual crops

All crops were generated directly from page 1 of `co-work-anl/input/pdf/实分析10(1).pdf` with `pdftoppm -r 600` and PIL. The full-page review images are `../ra10-page-1.jpg` through `../ra10-page-7.jpg`; the contact sheet is `../ra10-all-pages-contact.jpg`.

## P1 issue crops

- `RA10-P001-U01-directed.png`: source pixel box `(x=120..4830, y=620..3050)` in the 4959×7017 600-dpi render. Includes the heading, uncertain proposition, blue `proof`, and the first formula context.
- `RA10-P001-U01-tight.png`: source pixel box `(x=120..4830, y=1170..2120)`. Keeps the proposition line and local context at high resolution.

## “42区” crop

`region-42-p1-r2c2.png` is the documented **42-region** crop: the page is split into a 3-row × 2-column review grid, and this file is row 2, column 2 (`r2c2`), source box `(x=2479..4959, y=2339..4678)`. A quick-review JPEG is provided as `region-42-p1-r2c2-preview.jpg`. The crop label is descriptive so downstream recovery can map it to the project’s external region index without changing the source image.

## Full 42-region set

`../regions/` contains all 42 source review regions (`p0001`–`p0007`, six `r*c*` tiles per page), copied from the project’s region render. `../regions-42-contact.jpg` is a compact contact sheet of the complete set. The single `region-42-p1-r2c2.*` crop above is the targeted p1 tile used in the candidate record; it is not a claim that the external ledger’s numeric index is `42`.
