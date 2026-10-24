import json
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

WORDLISTS_DIR = Path("./wordlists")
OUTPUT_FILE = Path("wordlists.json")
ROCKYOU_LINES = 14_344_392


class Wordlist:
    def __init__(
        self,
        name: str,
        href: str,
        lines: int,
        tags: list[str],
        sources: list[str],
    ):
        self.name = name
        self.href = href
        self.lines = lines
        self.tags = tags
        self.sources = sources


def format_name(filename: str) -> str:
    name = Path(filename).stem.replace("_", " ").title()
    for keyword, replacement in KEYWORDS.items():
        name = re.sub(rf"\b{keyword}\b", replacement, name)
    return name


def count_lines(path: Path, name: str) -> int:
    if name == "Rockyou":
        return ROCKYOU_LINES
    with path.open("rb") as file:
        return sum(1 for _ in file)


def get_sources() -> dict[str, list[str]]:
    sources = {}
    notice = Path("NOTICE.md").read_text(encoding="utf-8")
    pattern = re.compile(
        r"\[`(?P<path>[^`]+)`\]\(wordlists/(?P<file>[^)]+)\)" r".*?(?=\n|$)"
    )

    for match in pattern.finditer(notice):
        line = match.group(0)
        path = f"wordlists/{match.group('file')}"
        urls = re.findall(
            r"\[(?:Source(?:\s+\d+)?)\]\((<?https?://[^)\s>]+>?)\)",
            line,
        )
        sources[path] = [url.strip("<>") for url in urls]
    return sources


def get_wordlist(path: Path, sources: dict[str, list[str]]) -> Wordlist:
    relative_path = path.relative_to(WORDLISTS_DIR.parent)
    folders = path.relative_to(WORDLISTS_DIR).parts[:-1]
    return Wordlist(
        name=format_name(path.name),
        href=relative_path.as_posix(),
        lines=count_lines(path, format_name(path.name)),
        tags=[folder.replace("_", "-") for folder in folders],
        sources=sources.get(relative_path.as_posix(), ["Not known"]),
    )


def main() -> None:
    sources = get_sources()
    wordlists = [
        get_wordlist(path, sources)
        for path in WORDLISTS_DIR.rglob("*")
        if path.is_file()
    ]
    wordlists.sort(key=lambda wordlist: wordlist.name)

    OUTPUT_FILE.write_text(
        json.dumps(
            [wordlist.__dict__ for wordlist in wordlists],
            sort_keys=True,
            indent=4,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
