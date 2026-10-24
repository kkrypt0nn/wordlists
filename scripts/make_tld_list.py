from pathlib import Path

import requests

TLDS_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
OUTPUT_FILE = Path("wordlists/discovery/tlds.txt")
USER_AGENT = "Krypton's Wordlists (https://github.com/kkrypt0nn/wordlists)"


def get_tlds() -> list[str]:
    response = requests.get(
        TLDS_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )
    response.raise_for_status()

    return response.text.splitlines()[1:]


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(get_tlds()) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
