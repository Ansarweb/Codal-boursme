import re
import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://t.me/s/codal"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Connecting to Codal...")

response = requests.get(
    SOURCE_URL,
    headers=headers,
    timeout=40
)

response.raise_for_status()

print("HTTP:", response.status_code)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

messages = soup.select(
    ".tgme_widget_message"
)

print("POSTS FOUND:", len(messages))

# جدیدترین چند پست را بررسی می‌کنیم
messages = messages[-10:]

for message in messages:

    data_post = message.get(
        "data-post",
        ""
    )

    if "/" not in data_post:
        continue

    try:
        post_id = int(
            data_post.rsplit("/", 1)[1]
        )
    except Exception:
        continue

    text_element = message.select_one(
        ".tgme_widget_message_text"
    )

    text = ""

    if text_element:
        text = text_element.get_text(
            "\n",
            strip=True
        )

    print()
    print("=" * 60)
    print("POST:", post_id)
    print("=" * 60)

    print(text[:1000])

    # -------------------------
    # لینک‌های موجود
    # -------------------------

    links = message.select("a[href]")

    found = []

    for link in links:

        href = link.get("href", "")

        if not href:
            continue

        if (
            ".pdf" in href.lower()
            or ".xlsx" in href.lower()
            or ".xls" in href.lower()
            or ".zip" in href.lower()
        ):
            found.append(href)

    # لینک‌های عمومی
    if found:

        print()
        print("ATTACHMENTS:")

        for url in found:
            print(url)

    else:

        print()
        print("NO DIRECT PDF/EXCEL LINK FOUND")

print()
print("=" * 60)
print("ATTACHMENT TEST FINISHED")
print("=" * 60)
