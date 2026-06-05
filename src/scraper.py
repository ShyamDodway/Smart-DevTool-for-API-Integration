import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def clean_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    cleaned_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(cleaned_lines)


def is_internal_link(base_url: str, link: str) -> bool:
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(link).netloc

    return base_domain == link_domain


def get_links_from_page(base_url: str, html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")

    links = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]

        full_url = urljoin(base_url, href)

        if is_internal_link(base_url, full_url):
            clean_url = full_url.split("#")[0]

            if clean_url not in links:
                links.append(clean_url)

    return links


def scrape_single_page(url: str) -> tuple[str, list]:
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    html = response.text
    text = clean_text_from_html(html)
    links = get_links_from_page(url, html)

    return text, links


def scrape_api_docs(url: str, max_pages: int = 5) -> str:
    visited = set()
    to_visit = [url]

    all_text = []

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        try:
            text, links = scrape_single_page(current_url)

            visited.add(current_url)

            all_text.append(
                f"\n\n--- Source URL: {current_url} ---\n\n{text}"
            )

            for link in links:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)

        except Exception:
            continue

    return "\n\n".join(all_text)

