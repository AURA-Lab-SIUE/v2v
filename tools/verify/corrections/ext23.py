"""Extend Chapter 23.

Two gaps. The chapter argues that ideology works by appearing ordinary and that
the ordinary is therefore where you look, then never demonstrates a reading of
anything ordinary; its only worked evidence is a participation distribution,
which is the quantitative half. And it says to choose an object without saying
how to bound a corpus when the candidate objects are everything nobody thought
worth examining.

The worked reading added here is of the platform's own category taxonomy, which
has the rare property of being both genuinely ordinary and fully measurable in
this book's data. It also happens to be the thing that constrained the book's own
sampling design, which makes the methodological consequence demonstrable rather
than asserted.
"""
import io
import pathlib
import sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter23-critical-cultural-analysis.qmd")
t = io.open(p, encoding="utf-8").read()

WORKED = '''## A reading of something nobody reads

Participation was the structural claim. Here is the close reading, on an object chosen because it is as ordinary as objects get: the list of categories a platform offers a streamer to describe what they are doing.

Nobody reads a category taxonomy. It is a dropdown. It is also a classification system, and a classification system is a statement about what kinds of thing exist and which distinctions are worth making. That makes it exactly the sort of object this tradition goes looking for.

The corpus contains **117 distinct categories** across 90,245 stream snapshots. Sort them into two piles and the shape appears immediately.

**106 of the 117 are named games.** Fortnite, Hearthstone, League of Legends, World of Warcraft, each with its own entry, each distinguishable from every other.

**Eleven are not.** Just Chatting, Art, Music & Performing Arts, ASMR, Talk Shows & Podcasts, IRL, Food & Drink, Travel & Outdoors, Science & Technology, Sports & Fitness, Makers & Crafting. Eleven bins for everything a person might do on camera that is not playing a specific piece of software.

Now the distribution across them, which is where the asymmetry stops being a curiosity.

Of the **226 channels** in the corpus with a recorded category, **112 have a non-game category as their modal one**: half the channels. Those half are sorted into eleven bins, while the other half are sorted into a hundred and six. And the bins are not used evenly. **Just Chatting alone is the modal category for 75 of those 112 channels, two thirds of them**, and accounts for **24.4 percent of every snapshot in the file**. The next largest non-game bin, Talk Shows & Podcasts, holds 13 channels.

**So the taxonomy is fine-grained exactly where a game publisher exists and coarse everywhere else.** A streamer playing one of two similar shooters is in two different categories. A streamer teaching a language, a streamer doing therapy-adjacent talk, a streamer co-watching a football match and a streamer sitting in silence doing their taxes are all in Just Chatting.

The reading does not require a claim about anyone's intent, and it is stronger without one. Categories that name games are discoverable, sponsorable, and attachable to a publisher's marketing and a tournament calendar. There is a commercial architecture that makes the distinction between two shooters worth maintaining and no equivalent architecture behind the distinction between language teaching and tax paperwork. The taxonomy is not a neutral description of what happens on the platform; it is a description shaped by what the platform is organized to sell, and the half of the activity that does not fit that shape is legible mainly as a residue.

**"Just Chatting" is the name of that residue**, and residual categories are a general feature worth recognizing. Any classification that has one has told you what it was built to see. *Other*, *Miscellaneous*, *Non-traditional*, *General* on a form, *Unclassifiable* in a codebook: the residual bin is where the scheme's purpose is visible, because it is everything the purpose did not need distinguished.

Which raises the question this tradition always turns back on the researcher.

**This book inherited that taxonomy and could not escape it.** Chapter 7's sampling design compares gaming against non-gaming channels, and "non-gaming" is not a category the world came with. It is the eleven bins, which is to say it is the platform's residue with a research label on it. Two thirds of the non-gaming stratum is Just Chatting, and Chapter 25 reports that Just Chatting behaves almost exactly like gaming on the measure the study cares about. A comparison whose treatment group is mostly the residual bin is a comparison partly about the bin.

That is not a reason to abandon the study. It is a reason to say so in the write-up, and it is the thing a critical reading of an ordinary object bought that no amount of careful measurement would have. **The analytic categories a study uses are frequently a platform's commercial categories with academic names on them, and noticing that is method rather than editorializing.**

'''

ARCHIVE = '''## Bounding the reading

"Look at the ordinary" is good advice and useless as an instruction, because the ordinary is everything. Critical work still needs a defensible answer to what you read and why, and the answer is not a sample in Chapter 7's sense.

**Build a corpus around a claim rather than a topic.** Not "Twitch's community guidelines" but "how the guidelines define harassment, across every revision between two dates". The second has an edge, and the edge is what makes it possible to say you looked at all of it.

**Take every instance inside the boundary, not a selection.** Where the set is small enough, a census removes the objection that you chose the passages that suited you. Chapter 16's saturation logic applies when it is not: read until new material stops changing the reading, and say where that happened.

**Include the material that resists.** Deliberately, and name it in the methods. This is the same move Chapter 21 asks for in a cross-source check and it does more work here, because the framework is doing more predicting.

**Fix and date everything.** A platform's policy page, category list and default settings are revised silently and continuously, and the version you read is evidence that will not exist next year. Archive it, record the retrieval date, and deposit the archive with the paper. Chapter 27's materials section governs; the difference here is that nobody else will have kept a copy.

**Say what you could not get.** Internal documents, moderation logs, the recommendation system. Political economy in particular is frequently reasoning from the outside of an organization that does not publish what would settle the question, and the honest version of that analysis says which claims rest on inference rather than on documents.

'''

if "## A reading of something nobody reads" not in t:
    anchor = "## Doing it"
    if anchor not in t:
        sys.exit("[ch23] worked-reading anchor not found")
    t = t.replace(anchor, WORKED + anchor, 1)

if "## Bounding the reading" not in t:
    anchor = "## The two failure modes"
    if anchor not in t:
        sys.exit("[ch23] archive anchor not found")
    t = t.replace(anchor, ARCHIVE + anchor, 1)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ch23 extended")
