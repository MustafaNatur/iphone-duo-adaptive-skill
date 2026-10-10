#!/usr/bin/env python3
"""Build a before/after contact sheet (single HTML file, images embedded).

Usage: python3 contact_sheet.py <baseline-dir> <after-dir> -o contact-sheet.html

Both dirs use the layout <pose>/<display>-<screen>.png written by capture.sh.
"""
import argparse
import base64
import html
import os


def collect(root):
    out = {}
    if not root or not os.path.isdir(root):
        return out
    for pose in sorted(os.listdir(root)):
        pdir = os.path.join(root, pose)
        if not os.path.isdir(pdir):
            continue
        for f in sorted(os.listdir(pdir)):
            if f.lower().endswith(".png"):
                out[(pose, f[:-4])] = os.path.join(pdir, f)
    return out


def img(path):
    if not path:
        return '<div class="missing">not captured</div>'
    data = base64.b64encode(open(path, "rb").read()).decode()
    return f'<img loading="lazy" src="data:image/png;base64,{data}" alt="{html.escape(os.path.basename(path))}">'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline")
    ap.add_argument("after", nargs="?")
    ap.add_argument("-o", "--out", default="contact-sheet.html")
    a = ap.parse_args()
    before, after = collect(a.baseline), collect(a.after)
    keys = sorted(set(before) | set(after))
    poses = sorted({k[0] for k in keys})

    rows = []
    for pose in poses:
        rows.append(f"<h2>{html.escape(pose)}</h2>")
        for key in [k for k in keys if k[0] == pose]:
            rows.append(f'<section><h3>{html.escape(key[1])}</h3><div class="pair">'
                        f'<figure><figcaption>Before</figcaption>{img(before.get(key))}</figure>'
                        f'<figure><figcaption>After</figcaption>{img(after.get(key))}</figure>'
                        f"</div></section>")

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>iPhone Duo Before / After</title>
<style>
:root {{ --bg:#fff; --fg:#1d1d1f; --muted:#6e6e73; --card:#f5f5f7; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#000; --fg:#f5f5f7; --muted:#a1a1a6; --card:#1c1c1e; }} }}
body {{ margin:0; padding:16px; background:var(--bg); color:var(--fg); font:15px -apple-system, system-ui, sans-serif; }}
h1 {{ font-size:22px; }} h2 {{ margin-top:32px; border-bottom:1px solid var(--muted); }} h3 {{ font-size:15px; color:var(--muted); }}
.pair {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
figure {{ margin:0; background:var(--card); border-radius:12px; padding:8px; }}
figcaption {{ font-size:12px; color:var(--muted); margin-bottom:6px; }}
img {{ width:100%; height:auto; display:block; border-radius:8px; }}
.missing {{ padding:40px 8px; text-align:center; color:var(--muted); }}
@media (max-width:600px) {{ .pair {{ grid-template-columns:1fr; }} }}
</style></head><body>
<h1>iPhone Duo — before / after</h1>
<p>{len(keys)} captures across {len(poses)} poses. Poses not listed were not captured.</p>
{''.join(rows)}
</body></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w").write(doc)
    print(a.out)


if __name__ == "__main__":
    main()
