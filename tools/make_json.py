# This code is bad, I even lost myself in it - but it works 😎 🤓

import glob
import json
import os
import re


keywords = {
    "Bip": "BIP",
    "Sql": "SQL",
    "Jsp": "JSP",
    "Lfi": "LFI",
    "Tlds": "TLDs",
    "Wp": "WP",
    "Vpn": "VPN",
    "Wpa": "WPA",
    "Us": "US",
    "Uri": "URI",
    "Http": "HTTP",
    "Os": "OS",
    "Beos": "BeOS",
    "Chromeos": "ChromeOS",
    "Ios": "iOS",
    "Hp": "HP",
    "Openbsd": "OpenBSD",
    "Sunos": "SunOS",
    "Webos": "webOS",
    "Itunes": "iTunes",
    "Xml": "XML",
    "Xss": "XSS",
}


class Wordlist:
    def __init__(self, name: str, href: str, lines: int, tags: list[type[str]]):
        self.name = name
        self.href = href
        self.lines = lines
        self.tags = tags


wordlists: list[type[Wordlist]] = []

for filename in glob.iglob("./wordlists/**/*", recursive=True):
    if os.path.isdir(filename):
        continue

    rel_path = os.path.relpath(filename)
    levels = rel_path.split(os.sep)
    folders = levels[1 : len(levels) - 1]
    name = levels[len(levels) - 1]
    name = name[: len(name) - 4].replace("_", " ").title()

    for keyword in keywords:
        name = re.sub(rf"\b{keyword}\b", keywords[keyword], name)

    href = "/".join(levels)

    lines = 0
    if name == "Rockyou":  # Can't count correctly for that one as it's a ZIP file
        lines = 14344392
    else:
        with open(rel_path, "rb") as f:
            lines = sum(1 for _ in f)

    tags: list[type[str]] = []
    for folder in folders:
        tags.append(folder.replace("_", "-"))

    wordlist = Wordlist(name, href, lines, tags)
    wordlists.append(wordlist)

with open("wordlists.json", "w", encoding="utf-8") as f:
    f.write(
        json.dumps(
            [wordlist.__dict__ for wordlist in sorted(wordlists, key=lambda w: w.name)],
            sort_keys=True,
            indent=4,
        )
    )
