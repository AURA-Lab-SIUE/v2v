#set page(
  paper: $if(papersize)$"$papersize$"$else$"us-letter"$endif$,
$if(margin-geometry)$
  // Margins handled by marginalia.setup below
$elseif(margin)$
  margin: ($for(margin/pairs)$$margin.key$: $margin.value$,$endfor$),
$else$
  margin: (x: 1.25in, y: 1.25in),
$endif$
  numbering: $if(page-numbering)$"$page-numbering$"$else$none$endif$,
  columns: $if(columns)$$columns$$else$1$endif$,
)
$if(logo)$
#set page(background: align($logo.location$, box(inset: $logo.inset$, image("$logo.path$", width: $logo.width$$if(logo.alt)$, alt: "$logo.alt$"$endif$))))
$endif$
$if(margin-geometry)$
// Configure marginalia page geometry (functions defined in definitions.typ)
#show: marginalia.setup.with(
  inner: (
    far: $margin-geometry.inner.far$,
    width: $margin-geometry.inner.width$,
    sep: $margin-geometry.inner.separation$,
  ),
  outer: (
    far: $margin-geometry.outer.far$,
    width: $margin-geometry.outer.width$,
    sep: $margin-geometry.outer.separation$,
  ),
  top: $if(margin.top)$$margin.top$$else$1.25in$endif$,
  bottom: $if(margin.bottom)$$margin.bottom$$else$1.25in$endif$,
  book: false,
  clearance: $margin-geometry.clearance$,
)
$endif$

// --- v2v cover page -------------------------------------------------------
// Appended to Quarto's stock page partial. This partial runs BEFORE the body,
// which is the whole point: include-before-body put the cover on page two,
// after the title block, and overriding the show-partial failed outright.
// Emitting a page here gives the real textbook order: cover, title page,
// contents. Alt text is mandatory because this PDF is tagged.
// fit: "cover" filled the page and CROPPED the art: the cover is 1600x2560
// (0.625) against US Letter (0.773), so the title lost its top and the edition
// line went off the bottom. "contain" shows all of it, and filling the page
// with the brand paper colour makes the letterboxing invisible because the
// cover's own background is that same colour.
#page(margin: 0pt, header: none, footer: none, numbering: none,
      fill: rgb("#FCFBF7"))[
  #align(center + horizon)[
  #image("images/cover.png", width: 100%, height: 100%, fit: "contain",
         alt: "Vibes to Variables, third edition, by Alex P. Leith. The cover shows the message-length distribution of the book's Twitch chat corpus: a tall bar at one word falling away into a long tail.")
  ]
]
