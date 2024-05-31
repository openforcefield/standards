import pathlib
import re
from urllib.request import Request, urlopen

import pytest


def find_markdown_files() -> list[str]:
    return [*pathlib.Path(".").rglob("docs/standards/**/*.md")]


def find_links(files: list[str]) -> list[str]:
    return [
        element
        for sublist in [
            re.findall(
                "http[s]?://(?:[0-9a-zA-Z]|[-/.%:_])+",
                open(file.as_posix()).read(),
            )
            for file in files
        ]
        for element in sublist
    ]


@pytest.mark.parametrize("link", find_links(find_markdown_files()))
def test_readme_links(link):
    """Test URLs in README are reachable"""
    # Some websites do not accept requests that don't specify the
    # client and the type of accepted documents so we add fake info
    # to avoid the response being an error.
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/xhtml+xml,text/html,application/xml;q=0.9,*/*;q=0.8",
    }

    # Some DOI-based links are now behind DDoS protections, so skip them
    if "doi.org" in link:
        pytest.skip("DOI links are behind DDoS protection and do not resolve")

    if "ccl.net" in link:
        pytest.skip("CCL is ... old :)")

    if "rdkit.org" in link:
        pytest.skip("gives a 406")

    request = Request(link, headers=headers)

    # Try to connect 5 times, keeping track of exceptions so useful feedback can be provided.
    success = False
    exception = None
    for retry in range(5):  # noqa: B007
        try:
            urlopen(request)
            success = True
            break
        except Exception as e:
            exception = e
    if not (success):
        raise exception
