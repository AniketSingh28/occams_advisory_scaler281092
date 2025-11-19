# scraper/scrape.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time, json, os

BASE = "https://www.occamsadvisory.com/"
HEADERS = {"User-Agent": "OccamsOnboardBot/1.0 (+contact:you@example.com)"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "occams_pages.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

seen = set()
to_visit = [BASE]
pages = []

while to_visit:
    url = to_visit.pop(0)
    if url in seen:
        continue

    seen.add(url)

    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code != 200:
            print("skip", url, "status", r.status_code)
            continue
    except Exception as e:
        print("error fetching", url, e)
        continue

    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text = "\n\n".join([p for p in paragraphs if p])

    if not text:
        continue

    pages.append({
        "url": url,
        "title": title,
        "text": text
    })

    print("scraped", url)

    # discover internal links
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        parsed = urlparse(href)

        if parsed.netloc.endswith("occamsadvisory.com"):
            if href not in seen and href not in to_visit:
                to_visit.append(href)

    time.sleep(0.5)

# save results
with open(OUT, "w", encoding="utf8") as f:
    json.dump(pages, f, indent=2, ensure_ascii=False)

print("saved", OUT)
