"""Search freesound.org for CC0 sounds (no login) and optionally fetch HQ previews.

search:   python fs_search.py search "<query>" [max_dur] [min_dur]
download: python fs_search.py get <sound_id> <out.mp3>
Only CC0 results are listed. Prints id, user, duration, downloads, title.
"""
import html, re, sys, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0"}

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()

def players(page):
    for m in re.finditer(r'<div\s+class="bw-player"(.*?)tabindex', page, re.S):
        a = dict(re.findall(r'data-([\w-]+)="([^"]*)"', m.group(1)))
        yield a

if sys.argv[1] == "search":
    q = sys.argv[2]; maxd = float(sys.argv[3]) if len(sys.argv) > 3 else 9e9; mind = float(sys.argv[4]) if len(sys.argv) > 4 else 0
    url = "https://freesound.org/search/?" + urllib.parse.urlencode({"q": q, "f": 'license:"Creative Commons 0"', "s": "Downloads desc"})
    page = fetch(url).decode("utf-8")
    for a in players(page):
        d = float(a.get("duration", 0))
        if mind <= d <= maxd:
            print(f'{a["sound-id"]:>7} {a["username"][:16]:16} {d:6.1f}s dl={a.get("num-downloads","?"):>6} {html.unescape(a["title"])[:70]}')
elif sys.argv[1] == "get":
    sid, out = sys.argv[2], sys.argv[3]
    page = fetch(f"https://freesound.org/s/{sid}/").decode("utf-8")
    assert "Creative Commons 0" in page or "creativecommons.org/publicdomain/zero" in page, "not CC0"
    a = next(players(page))
    mp3 = a["mp3"].replace("-lq.mp3", "-hq.mp3")
    open(out, "wb").write(fetch(mp3))
    print(out, f"https://freesound.org/s/{sid}/ (CC0)", html.unescape(a["title"]))
