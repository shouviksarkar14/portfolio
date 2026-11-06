"""Rebuild switchboard/index.html from the Switch Board artifact's HTML.

Usage: python3 tools/build_switchboard.py <artifact.html> switchboard/index.html

The source is the private Switch Board artifact on claude.ai (download its HTML).
Everything before the "connect" block is kept as is; the connect block, which
reads the private database, is replaced with tools/switchboard-demo-db.js
(an in-browser store seeded with fictional sample data).
"""
import pathlib, sys

src_path, out_path = sys.argv[1], sys.argv[2]
here = pathlib.Path(__file__).parent
src = open(src_path, encoding="utf-8").read()
i = src.index("/* ---------- connect ---------- */")
out = src[:i] + (here / "switchboard-demo-db.js").read_text(encoding="utf-8")
out = out.replace("<title>Switch Board</title>", "<title>Switch Board · demo</title>", 1)
tag = '<script defer src="/_vercel/insights/script.js"></script>'
j = out.rfind("</body>")
out = out[:j] + tag + "\n" + out[j:]
open(out_path, "w", encoding="utf-8").write(out)
print("ok", len(out))
