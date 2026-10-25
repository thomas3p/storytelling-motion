"""Download the OFL fonts the pipeline uses (Prompt, Mitr, Kanit) from the google/fonts repository into a folder.

usage: python get_fonts.py <dest folder, e.g. projects/<ep>/hf/assets/fonts>
Fonts are SIL Open Font License; the licence text is saved next to them. Existing files are kept.
"""
import os, sys, urllib.request

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FILES = ["prompt/Prompt-Bold.ttf", "prompt/Prompt-Medium.ttf", "mitr/Mitr-SemiBold.ttf", "mitr/Mitr-Medium.ttf", "kanit/Kanit-Bold.ttf"]
LICENCES = {"prompt/OFL.txt": "OFL-Prompt.txt", "mitr/OFL.txt": "OFL-Mitr.txt", "kanit/OFL.txt": "OFL-Kanit.txt"}


def fetch(url, out):
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return False
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "storytelling-motion"}), timeout=60) as r:
        data = r.read()
    with open(out, "wb") as f:
        f.write(data)
    return True


def main(dest):
    os.makedirs(dest, exist_ok=True)
    for f in FILES:
        got = fetch(BASE + f, os.path.join(dest, os.path.basename(f)))
        print(("downloaded " if got else "kept ") + os.path.basename(f))
    for src, name in LICENCES.items():
        fetch(BASE + src, os.path.join(dest, name))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
