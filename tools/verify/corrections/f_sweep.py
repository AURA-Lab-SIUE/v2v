import io, pathlib, sys
R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
E = {
 "chapters/_v3-draft/chapter12-quantitative-content-analysis.qmd": [
   ("fifty channels drawn from across the platform's volume distribution",
    "228 channels drawn from across the platform's volume distribution"),
 ],
 "chapters/_v3-draft/chapter15-existing-data.qmd": [
   ("The package documents 157,080 messages across 50 channels, sampled from a 1.6 GB database dump of Twitch chat captured in November 2018, with the random seed recorded, eight named anchor channels, and the remaining 42 drawn as a stratified random sample by chat-volume decile.",
    "The package documents 157,080 messages across 228 channels, sampled from a 1.6 GB database dump of Twitch chat captured in November 2018, with the random seed recorded, eight named anchor channels, a census of every non-gaming channel in the population, and a matched draw of gaming channels stratified by chat-volume decile."),
   ("**The row and channel counts hold.** 157,080 messages, 50 channels, all eight anchors present, and no duplicate identifiers.",
    "**The row and channel counts hold.** 157,080 messages, 228 channels, all eight anchors present, and no duplicate identifiers."),
 ],
 "chapters/_v3-draft/chapter24-preparing-describing-visualizing.qmd": [
   ("how did the audience for these fifty channels move",
    "how did the audience for these 228 channels move"),
 ],
}
for name, edits in E.items():
    p = R / name
    t = io.open(p, encoding="utf-8").read()
    o = t
    for a, b in edits:
        if a not in t:
            if b in t: continue
            sys.exit("[%s] NOT FOUND: %r" % (name, a[:90]))
        t = t.replace(a, b)
    if t != o:
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("patched", name.split("/")[-1])
