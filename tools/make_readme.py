# This code is bad, I even lost myself in it - but it works 😎 🤓

import glob
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
    "Xxe": "XXE",
}
wordlists = {}

readme_template = """<h1 align="center">
  Wordlists
</h1>

<h4 align="center">
  Yet another collection of wordlists. They are sorted by their content. Feel free to request to add new wordlists.
</h4>

<p align="center">
  <a href="//hub.docker.com/r/kkrypt0nn/wordlists"><img src="https://img.shields.io/docker/v/kkrypt0nn/wordlists/alpine-latest?logo=docker"></a>
  <a href="//hub.docker.com/r/kkrypt0nn/wordlists"><img src="https://img.shields.io/docker/v/kkrypt0nn/wordlists/debian-latest?logo=docker"></a>
  <a href="//hub.docker.com/r/kkrypt0nn/wordlists"><img src="https://img.shields.io/docker/v/kkrypt0nn/wordlists/ubuntu-latest?logo=docker"></a>
  <a href="//github.com/kkrypt0nn/wordlists"><img src="https://img.shields.io/github/repo-size/kkrypt0nn/wordlists"></a>
  <a href="//github.com/kkrypt0nn/wordlists/commits"><img src="https://img.shields.io/github/last-commit/kkrypt0nn/wordlists"></a>
  <a href="//github.com/kkrypt0nn/wordlists/contributors"><img src="https://img.shields.io/github/contributors/kkrypt0nn/wordlists"></a>
</p>

## 🐳 Docker Images

There are three Docker images available with for the three main OS images:

- `alpine-latest`
- `debian-latest`
- `ubuntu-latest`

These will have a `/wordlists` folder with all the wordlists in there for you to use them.

## 🌍 Contributing

If you have a wordlist that you wish to see here, please post them [here](https://github.com/kkrypt0nn/wordlists/issues).

If you already have a wordlist ready to be added, make sure to [open a pull request](https://github.com/kkrypt0nn/wordlists/pulls).

## 📜 Wordlists

[[TOGGLE]]

<hr>

[[LIST]]

## ⚠️ Disclaimer

These wordlists are intended solely for ethical and legal purposes, such as security research, legally authorized penetration testing, and educational use. Unauthorized or illegal use is strictly prohibited.

By using this repository, you agree to follow all applicable laws and abide by the [Terms of Use](https://github.com/kkrypt0nn/wordlists/blob/main/TERMS_OF_USE.md).

## 🏁 Sources

The wordlists in this repository are not all made by myself. Therefore, starting February 2025, I will try my best to provide the source of each wordlist, as well as add the potential license/copyright notice of the wordlist in the [NOTICE.md](NOTICE.md) file. Considering this repository is quite old, I may not have the source for all of them, but as mentioned I will try my best.

The wordlists that are made by myself, for example all the stressing generated wordlists or wordlists gathered from words on websites, will have **no** license, as I believe there is no point in adding licenses for things you can generate yourself.

> _If you feel like I have used your wordlist and it is missing in the [NOTICE.md](NOTICE.md) file, feel free to open an issue/pull request._
"""

for filename in glob.iglob("./wordlists/**/*", recursive=True):
    if os.path.isdir(filename):
        continue

    rel_path = os.path.relpath(filename)
    levels = rel_path.split(os.sep)
    folders = levels[1 : len(levels) - 1]
    wordlist = levels[len(levels) - 1]
    wordlist = wordlist[: len(wordlist) - 4].replace("_", " ").title()

    for keyword in keywords:
        wordlist = re.sub(rf"\b{keyword}\b", keywords[keyword], wordlist)

    href = "/".join(levels)

    if wordlist == "Rockyou":  # Can't count correctly for that one as it's a ZIP file
        wordlist = f'<a href="{href}">{wordlist}</a> - 14,344,392 Lines'
    else:
        with open(rel_path, "rb") as f:
            wordlist = f'<a href="{href}">{wordlist}</a> - {sum(1 for _ in f):,} Lines'

    # Here is where I got lost myself to be fair
    match len(levels) - 2:
        case 1:
            folder = folders[0].replace("_", " ").title()
            if folder not in wordlists:
                wordlists[folder] = [wordlist]
            else:
                wordlists[folder].append(wordlist)
        case 2:
            for i in range(0, len(folders)):
                folder = folders[i].replace("_", " ").title()
                if folder not in wordlists:
                    if i == 0:
                        wordlists[folder] = {}
                    else:
                        previous_folder = folders[i - 1].replace("_", " ").title()
                        if folder not in wordlists[previous_folder]:
                            wordlists[previous_folder][folder] = [wordlist]
                        else:
                            wordlists[previous_folder][folder].append(wordlist)
                else:
                    if i == 1:
                        previous_folder = folders[i - 1].replace("_", " ").title()
                        if folder not in wordlists[previous_folder]:
                            wordlists[previous_folder][folder] = [wordlist]
                        else:
                            wordlists[previous_folder][folder].append(wordlist)
        case other:
            print("Invalid level length")
            exit(1337)

sorted_keys = sorted(list(wordlists.keys()))
wordlists = {key: wordlists[key] for key in sorted_keys}

# Sort User Agents as well
sorted_user_agents_keys = sorted(list(wordlists["User Agents"].keys()))
wordlists["User Agents"] = {
    key: wordlists["User Agents"][key] for key in sorted_user_agents_keys
}

# Sort the values
for key in wordlists:
    if isinstance(wordlists[key], list):
        wordlists[key].sort()
    elif isinstance(wordlists[key], dict):
        for subkey in wordlists[key]:
            wordlists[key][subkey].sort()


# Make the togglable list of wordlists
togglable_list = """<details>
  <summary>Togglable Wordlists</summary>"""
for category in wordlists:
    current_category = f"""
  <details>
    <summary>{category}</summary>"""

    if isinstance(wordlists[category], list):
        current_category += """
    <ul>"""
        for wordlist in wordlists[category]:
            current_category += f"""
      <li>{wordlist}</li>"""
        current_category += """
    </ul>"""

    if isinstance(wordlists[category], dict):
        for subcategory in wordlists[category]:
            current_category += f"""
    <details>
      <summary>{subcategory}</summary>
      <ul>"""
            for wordlist in wordlists[category][subcategory]:
                current_category += f"""
        <li>{wordlist}</li>"""
            current_category += """
      </ul>
    </details>"""

    current_category += """
  </details>"""
    togglable_list += current_category
togglable_list += """
</details>"""


# Make the normal list of wordlists
normal_list = "<ul>"
for category in wordlists:
    current_category = f"""
  <li>{category}</li>
  <ul>"""

    if isinstance(wordlists[category], list):
        for wordlist in wordlists[category]:
            current_category += f"""
    <li>{wordlist}</li>"""

    if isinstance(wordlists[category], dict):
        for subcategory in wordlists[category]:
            current_category += f"""
    <li>{subcategory}</li>"""
            current_category += f"""
      <ul>"""
            for wordlist in wordlists[category][subcategory]:
                current_category += f"""
        <li>{wordlist}</li>"""
            current_category += f"""
      </ul>"""

    current_category += """
  </ul>"""
    normal_list += current_category

normal_list += """
</ul>"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(
        readme_template.replace("[[TOGGLE]]", togglable_list).replace(
            "[[LIST]]", normal_list
        )
    )
