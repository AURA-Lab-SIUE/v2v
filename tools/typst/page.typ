// v2v page-partial. Replaces orange-book's, so page geometry is ours.
//
// Emits the cover before anything else: this partial runs ahead of the body,
// which is why the cover lands on page one. include-before-body put it on page
// two, behind the title block.
#set page(
  paper: $if(papersize)$"$papersize$"$else$"us-letter"$endif$,
$if(margin)$
  margin: ($for(margin/pairs)$$margin.key$: $margin.value$,$endfor$),
$else$
  margin: (x: 1in, y: 1in),
$endif$
  numbering: $if(page-numbering)$"$page-numbering$"$else$none$endif$,
  columns: $if(columns)$$columns$$else$1$endif$,
  // Running head carrying the current chapter, with a hairline rule. Standard
  // in a printed textbook, and dropping orange-book lost the ones it provided.
  // Suppressed on chapter openers, where the chapter title is already the
  // largest thing on the page, and on any page with no chapter above it.
  header: context {
    let here-page = here().page()
    let chs = query(selector(heading.where(level: 1)).before(here()))
    let opens = chs.filter(h => h.location().page() == here-page)
    if chs.len() > 0 and opens.len() == 0 {
      set text(font: ("Newsreader",), size: 0.82em, fill: rgb("#6B6357"))
      chs.last().body
      v(-0.55em)
      line(length: 100%, stroke: 0.5pt + rgb("#E0DACE"))
    }
  },
)

// Cover. fit: "contain" over a page filled with the brand paper colour: the
// art is 1600x2560 and the page is squarer, so "cover" cropped the title off
// the top. The fill makes the letterboxing invisible.
#page(margin: 0pt, header: none, footer: none, numbering: none,
      fill: rgb("#FCFBF7"))[
  #align(center + horizon)[
    #image("images/cover.png", width: 100%, height: 100%, fit: "contain",
           alt: "Vibes to Variables, third edition, by Alex P. Leith. The cover shows the message-length distribution of the book's Twitch chat corpus: a tall bar at one word falling away into a long tail.")
  ]
]
