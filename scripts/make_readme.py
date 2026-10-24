import re
from pathlib import Path

KEYWORDS = {
    "Beos": "BeOS",
    "Bip": "BIP",
    "Chromeos": "ChromeOS",
    "Html": "HTML",
    "Hp": "HP",
    "Http": "HTTP",
    "Iis": "IIS",
    "Ios": "iOS",
    "Itunes": "iTunes",
    "Js": "JS",
    "Jsp": "JSP",
    "Lfi": "LFI",
    "Openai": "OpenAI",
    "Openbsd": "OpenBSD",
    "Os": "OS",
    "Sql": "SQL",
    "Ssti": "SSTI",
    "Sunos": "SunOS",
    "Tlds": "TLDs",
    "Tv": "TV",
    "Uri": "URI",
    "Us": "US",
    "Usa": "USA",
    "Vpn": "VPN",
    "Wpa": "WPA",
    "Webos": "webOS",
    "Wp": "WP",
    "Xml": "XML",
    "Xss": "XSS",
    "Xxe": "XXE",
}

WORDLISTS_DIR = Path("wordlists")
README_FILE = Path("README.md")
ROCKYOU_LINES = 14_344_392
README_TEMPLATE = """<h1 align="center">
  Wordlists
</h1>

<h4 align="center">
  Yet another collection of wordlists. They are sorted by their content. Feel free to request to add new wordlists.
</h4>

<p align="center">
  <a href="//hub.docker.com/r/kkrypt0nn/wordlists"><img src="https://img.shields.io/docker/v/kkrypt0nn/wordlists/alpine-latest?logo=docker"></a>
  <a href="//hub.docker.com/r/kkrypt0nn/wordlists"><img src="https://img.shields.io/docker/v/kkrypt0nn/wordlists/debian-latest?logo=docker"></a>
  <a href="//hub.docker.com/r/kkrypt0nn/wordlists"><img src="https://img.shields.io/docker/v/kkrypt0nn/wordlists/scratch-latest?logo=docker"></a>
  <a href="//hub.docker.com/r/kkrypt0nn/wordlists"><img src="https://img.shields.io/docker/v/kkrypt0nn/wordlists/ubuntu-latest?logo=docker"></a>
</p>

<p align="center">
  <a href="//discord.gg/xj6y5ZaTMr"><img src="https://img.shields.io/discord/1358456011316396295?logo=discord"></a>
  <a href="//github.com/kkrypt0nn/wordlists"><img src="https://img.shields.io/github/repo-size/kkrypt0nn/wordlists"></a>
  <a href="//github.com/kkrypt0nn/wordlists/commits"><img src="https://img.shields.io/github/last-commit/kkrypt0nn/wordlists"></a>
  <a href="//github.com/kkrypt0nn/wordlists/contributors"><img src="https://img.shields.io/github/contributors/kkrypt0nn/wordlists"></a>
</p>

## 🐳 Docker Images

There are four Docker tags available for the [`kkrypt0nn/wordlists`](https://hub.docker.com/r/kkrypt0nn/wordlists) Docker repository:

- [`alpine-latest`](https://hub.docker.com/r/kkrypt0nn/wordlists/tags?name=alpine-latest)
- [`debian-latest`](https://hub.docker.com/r/kkrypt0nn/wordlists/tags?name=debian-latest)
- [`scratch-latest`](https://hub.docker.com/r/kkrypt0nn/wordlists/tags?name=scratch-latest)
- [`ubuntu-latest`](https://hub.docker.com/r/kkrypt0nn/wordlists/tags?name=ubuntu-latest)

These will have a `/wordlists` folder with all the wordlists in there for you to use them.

## 📦 HackTheBox Wordlists

[Hack The Box](https://hackthebox.com) is a platform designed for practicing penetration testing skills in a legal and controlled environment. It offers various challenges and real-world scenarios for users to sharpen their hacking abilities.

In the [`wordlists/htb`](https://github.com/kkrypt0nn/wordlists/tree/main/wordlists/htb) folder, you'll find a collection of custom wordlists I created specifically for use on HTB. As I got more into the platform and had fun solving challenges, these wordlists became invaluable for tasks like brute-forcing and enumeration. Feel free to use them for your own HTB adventures, and I hope they help you level up your hacking skills!

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


def format_name(name: str) -> str:
    name = Path(name).stem.replace("_", " ").title()
    for keyword, replacement in KEYWORDS.items():
        name = re.sub(rf"\b{keyword}\b", replacement, name)
    return name


def format_category(name: str) -> str:
    return "HTB" if name.lower() == "htb" else name.replace("_", " ").title()


def get_wordlist(path: Path) -> str:
    name = format_name(path.name)
    href = path.as_posix()
    if name == "Rockyou":
        lines = ROCKYOU_LINES
    else:
        with path.open("rb") as file:
            lines = sum(1 for _ in file)
    return f'<a href="{href}">{name}</a> - {lines:,} Lines'


def collect_wordlists() -> dict:
    wordlists = {}
    for path in WORDLISTS_DIR.rglob("*"):
        if not path.is_file():
            continue

        folders = path.relative_to(WORDLISTS_DIR).parts[:-1]
        wordlist = get_wordlist(path)

        if len(folders) == 1:
            category = format_category(folders[0])
            wordlists.setdefault(category, []).append(wordlist)
        elif len(folders) == 2:
            category = format_category(folders[0])
            subcategory = format_category(folders[1])
            wordlists.setdefault(category, {}).setdefault(subcategory, []).append(
                wordlist
            )
        else:
            raise ValueError(f"Unexpected directory structure: {path}")

    for category, value in wordlists.items():
        if isinstance(value, list):
            value.sort()
        else:
            value = dict(sorted(value.items()))
            for wordlists_in_category in value.values():
                wordlists_in_category.sort()

    return dict(sorted(wordlists.items()))


def generate_toggle_list(wordlists: dict) -> str:
    lines = [
        "<details>",
        "  <summary>Togglable Wordlists</summary>",
    ]

    for category, entries in wordlists.items():
        lines.extend(
            [
                "",
                "  <details>",
                f"    <summary>{category}</summary>",
            ]
        )
        if isinstance(entries, list):
            lines.append("    <ul>")
            lines.extend(f"      <li>{entry}</li>" for entry in entries)
            lines.extend(["    </ul>"])
        else:
            for subcategory, items in entries.items():
                lines.extend(
                    [
                        "",
                        "    <details>",
                        f"      <summary>{subcategory}</summary>",
                        "      <ul>",
                    ]
                )
                lines.extend(f"        <li>{item}</li>" for item in items)
                lines.extend(["      </ul>", "    </details>"])
        lines.append("  </details>")
    lines.append("</details>")
    return "\n".join(lines)


def generate_normal_list(wordlists: dict) -> str:
    lines = ["<ul>"]

    for category, entries in wordlists.items():
        lines.extend(
            [
                f"  <li>{category}</li>",
                "  <ul>",
            ]
        )
        if isinstance(entries, list):
            lines.extend(f"    <li>{entry}</li>" for entry in entries)
        else:
            for subcategory, items in entries.items():
                lines.extend(
                    [
                        f"    <li>{subcategory}</li>",
                        "      <ul>",
                    ]
                )
                lines.extend(f"        <li>{item}</li>" for item in items)
                lines.append("      </ul>")
        lines.append("  </ul>")
    lines.append("</ul>")
    return "\n".join(lines)


def main() -> None:
    wordlists = collect_wordlists()
    README_FILE.write_text(
        README_TEMPLATE.replace("[[TOGGLE]]", generate_toggle_list(wordlists)).replace(
            "[[LIST]]", generate_normal_list(wordlists)
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
