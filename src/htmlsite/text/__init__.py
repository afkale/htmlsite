import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    rg = r"\!\[([^!\[*]*)\]\(([^!\[*]*)\)"
    return __extract_rg(rg, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    rg = r"(?<!\!)\[([^!\[*]*)\]\(([^!\[*]*)\)"
    return __extract_rg(rg, text)


def __extract_rg(rg: str, text: str) -> list[tuple[str, str]]:
    pattern = re.compile(rg)
    matches = pattern.finditer(text)

    result = []
    for match_num, match in enumerate(matches, start=1):
        result.append(match.groups())
    return result
