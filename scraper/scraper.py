from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from models.models import Story


def scrape_stories(db):
    saved = 0
    skipped = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://news.ycombinator.com")

        soup = BeautifulSoup(page.content(), "html.parser")
        stories = soup.find_all("tr", class_="athing submission")

        for story in stories[:10]:
            titleline = story.find("span", class_="titleline")
            link = titleline.find("a")
            title = link.text
            url = link["href"]

            existing = db.query(Story).filter(Story.url == url).first()
            if not existing:
                new_story = Story(
                    title=title,
                    url=url,
                    source="Hacker News"
                )
                db.add(new_story)
                saved += 1
            else:
                skipped += 1

        db.commit()
        browser.close()

    return saved, skipped
