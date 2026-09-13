// v2v show-partial. Replaces orange-book's, so the book renders through
// Quarto's own Typst template with front matter we control.
//
// Why: orange-book drew chapter decoration with `outset`, deliberately pushing
// a coloured banner past the text block, which read as a bug on every chapter
// opener and on the Contents page; it also gave each chapter a title page that
// was otherwise blank, and a title block tinted pink. None of that is standard
// textbook practice and none of it was reachable through Quarto's options.
//
// What has to be reimplemented: Quarto's book filter emits `#part[...]` for
// part dividers and `#show: appendices.with(...)` for appendices, both of which
// were orange-book functions. They are defined here. orange-book's
// numbering.typ is deliberately NOT overridden, because its chapter-based
// figure numbering (Figure 2.3 rather than Figure 17) is what a textbook wants.

// Part divider: a right-hand page carrying only the part name, which is the
// conventional book treatment.
#let part-counter = counter("v2v-part")
#let part(title) = {
  pagebreak(weak: true)
  part-counter.step()
  // No "Part I" eyebrow: the source titles already read "Part I: Foundation",
  // so a counter line above them just said it twice.
  block(above: 32%, below: 0pt)[
    #block[
      #set text(font: ("Archivo",), weight: 800, size: 2.4em, fill: rgb("#191B1E"))
      #title
    ]
    #v(0.6em)
    #line(length: 30%, stroke: 2pt + rgb("#C41425"))
  ]
  pagebreak(weak: true)
}

// Appendices: a show rule. Restarts chapter numbering at A and flips the state
// that numbering.typ reads to switch figures to A.1 form.
#let appendices(title, hide-parent: false, doc) = {
  state("appendix-state", none).update("appendix")
  counter(heading).update(0)
  set heading(numbering: "A.1.1")
  doc
}

// Title page. Deliberately plain: the cover already carries the data figure, so
// this page does the job a title page does in a printed book, which is to state
// the work, the author, the edition and the licence.
#page(numbering: none)[
  #v(22%)
  #block[
    #set text(font: ("Archivo",), weight: 800, size: 2.6em, fill: rgb("#191B1E"))
    $if(title)$$title$$endif$
  ]
  #v(0.5em)
  #line(length: 28%, stroke: 2.5pt + rgb("#C41425"))
  #v(0.9em)
  #block[
    #set text(font: ("Newsreader",), size: 1.15em, fill: rgb("#6B6357"))
    $if(subtitle)$$subtitle$$endif$
  ]
  #v(3.2em)
  #block[
    #set text(font: ("Archivo",), weight: 600, size: 1.15em, fill: rgb("#191B1E"))
    $for(by-author)$$it.name.literal$$sep$, $endfor$
  ]
  #v(1fr)
  // About-the-cover note. It lives here rather than on the cover itself: a
  // cover should carry the work's identity, not its methods note. Written in
  // the partial rather than in index.qmd because Quarto's conditional-content
  // divs do not process in that file, so a `when-format` block leaked its raw
  // `:::` markers onto the website.
  #block(width: 78%)[
    #set text(font: ("Newsreader",), size: 0.88em, fill: rgb("#6B6357"))
    #set par(justify: false, leading: 0.62em)
    *About the cover.* The shape on the front is real data from this book: the
    distribution of message lengths across all 35,267 messages in the Twitch
    chat corpus of November 2018, counted in words. A tall bar at one word falls
    away into a long tail running out past a hundred. You meet the same
    distribution again in Chapter 12, drawn properly and read carefully. It is
    on the cover because it is the honest shape of the thing this book is about:
    most of what people say in a livestream chat is very short, and a method
    that assumes otherwise will mislead you.
  ]
  #v(1.4em)
  #block[
    #set text(font: ("Newsreader",), size: 0.92em, fill: rgb("#6B6357"))
    Third Edition
    #linebreak()
    $if(date)$$date$$endif$
    #linebreak()
    Licensed CC BY 4.0
  ]
]

#show: doc => article(
// authors deliberately not passed: see note above.
$if(lang)$
  lang: "$lang$",
$endif$
$if(region)$
  region: "$region$",
$endif$
$if(mainfont)$
  font: ("$mainfont$",),
$elseif(brand.typography.base.family)$
  font: $brand.typography.base.family$,
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
$if(brand.typography.headings.family)$
  heading-family: $brand.typography.headings.family$,
$endif$
$if(brand.typography.headings.weight)$
  heading-weight: $brand.typography.headings.weight$,
$endif$
$if(brand.typography.headings.color)$
  heading-color: $brand.typography.headings.color$,
$endif$
$if(section-numbering)$
  sectionnumbering: "$section-numbering$",
$endif$
$if(codefont)$
  codefont: ($for(codefont)$"$codefont$",$endfor$),
$elseif(brand.typography.monospace.family)$
  codefont: $brand.typography.monospace.family$,
$endif$
$if(linkcolor)$
  linkcolor: [$linkcolor$],
$endif$
$if(toc)$
  toc: $toc$,
$endif$
$if(toc-title)$
  toc_title: [$toc-title$],
$endif$
  toc_depth: $toc-depth$,
  doc,
)
