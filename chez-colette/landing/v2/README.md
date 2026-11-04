# The landing page, second edition

`landing-v2.html` is the page for December (both books, the Christmas strip).
`landing-v2-january.html` is the same page after the season (the Home Bible alone).
Both come out of `v2/template.html`; nothing is edited in the built files.

## Putting it live on www.colette-dubois.com

The domain points at the Gumroad product, and the product's page is this HTML.

1. Gumroad → Products → *Colette's Home Bible* → the product page editor →
   the custom HTML / page-content field.
2. Replace everything there with the whole of `landing-v2.html`.
3. Save and publish. The domain shows the new page within a minute; the buy
   buttons open Gumroad's own checkout, because they carry
   `data-gumroad-action="buy"`, and every price on the page is filled in by
   Gumroad from the product's real price (`data-gumroad-field="price"`).

In January, paste `landing-v2-january.html` instead, and take the two Christmas
files out of the product's content.

## Rebuilding

    node v2/render-covers.cjs      # only if a cover changed
    python3 v2/build.py            # both pages, with a size and wiring check

Gumroad caps the field at 500,000 characters; the build fails if a page passes
it. The page makes no external request: three font subsets, the two covers,
the author photograph and five book pages are inlined.

## Assets

`v2/assets/` holds the inlined images. `christmas/` holds the Gumroad product
images of the two books together (`gumroad-cover-both-books.jpg`,
`gumroad-thumbnail-both-books.jpg`) and the script that renders them.
