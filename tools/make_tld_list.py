import requests


def get_content(url: str) -> str:
    response = requests.get(
        url=url,
        headers={
            "User-Agent": "Krypton's Wordlists (https://github.com/kkrypt0nn/wordlists)"
        },
    )
    return response.text


def main() -> None:
    content = get_content("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
    with open("./wordlists/discovery/tlds.txt", "w+", encoding="utf-8") as manuf_file:
        manuf_file.write(content)


if __name__ == "__main__":
    main()
