import asyncio
import re
import urllib.parse
from bs4 import BeautifulSoup
import httpx
from apify import Actor

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

def clean_text(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()

async def enrich_website(client: httpx.AsyncClient, website_url: str):
    if not website_url or not website_url.startswith("http"):
        return {"email": "", "linkedin": "", "facebook": "", "instagram": ""}

    data = {"email": "", "linkedin": "", "facebook": "", "instagram": ""}
    try:
        resp = await client.get(website_url, headers=HEADERS, timeout=8.0)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            emails = EMAIL_REGEX.findall(resp.text)
            valid_emails = [
                e for e in emails 
                if not e.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg"))
            ]
            if valid_emails:
                data["email"] = valid_emails[0]

            for a in soup.find_all("a", href=True):
                href = a["href"].lower()
                if "linkedin.com/company" in href and not data["linkedin"]:
                    data["linkedin"] = a["href"]
                elif "facebook.com/" in href and not any(x in href for x in ["sharer", "share.php"]) and not data["facebook"]:
                    data["facebook"] = a["href"]
                elif "instagram.com/" in href and not data["instagram"]:
                    data["instagram"] = a["href"]
    except Exception:
        pass
    return data

async def scrape_directory_page(client: httpx.AsyncClient, query: str, location: str, page: int, enrich: bool):
    encoded_terms = urllib.parse.quote(query)
    encoded_loc = urllib.parse.quote(location)
    url = f"https://www.yellowpages.com/search?search_terms={encoded_terms}&geo_location_terms={encoded_loc}&page={page}"

    response = await client.get(url, headers=HEADERS, timeout=15.0)
    if response.status_code != 200:
        Actor.log.warning(f"Page {page} status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select(".result, .srp-listing")
    leads = []

    for card in cards:
        name_el = card.select_one(".business-name, .info h2 a")
        if not name_el:
            continue

        name = clean_text(name_el.get_text())
        phone_el = card.select_one(".phone")
        phone = clean_text(phone_el.get_text()) if phone_el else ""

        website_el = card.select_one("a.track-visit-website")
        website = website_el["href"] if website_el and website_el.has_attr("href") else ""

        street_el = card.select_one(".street-address")
        locality_el = card.select_one(".locality")
        street = clean_text(street_el.get_text()) if street_el else ""
        locality = clean_text(locality_el.get_text()) if locality_el else ""
        full_address = f"{street}, {locality}".strip(", ")

        rating_el = card.select_one(".rating span, .result-rating")
        rating = clean_text(rating_el.get_text()) if rating_el else "N/A"

        lead = {
            "business_name": name,
            "category": query,
            "target_location": location,
            "phone": phone,
            "website": website,
            "address": full_address,
            "rating": rating,
            "email": "",
            "linkedin": "",
            "facebook": "",
            "instagram": "",
        }

        if enrich and website:
            enrichment = await enrich_website(client, website)
            lead.update(enrichment)

        leads.append(lead)

    return leads

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        search_query = actor_input.get("searchQuery", "Dentists")
        location = actor_input.get("location", "Austin, TX")
        max_results = int(actor_input.get("maxResults", 10))
        extract_socials = actor_input.get("extractSocials", True)

        Actor.log.info(f"Starting Scraper: '{search_query}' in '{location}' (Target: {max_results} leads, Enrichment: {extract_socials})")

        collected_leads = []
        page = 1

        async with httpx.AsyncClient(follow_redirects=True) as client:
            while len(collected_leads) < max_results:
                Actor.log.info(f"Fetching directory page {page}...")
                try:
                    leads = await scrape_directory_page(client, search_query, location, page, extract_socials)
                except Exception as err:
                    Actor.log.error(f"Error fetching page {page}: {err}")
                    break

                if not leads:
                    Actor.log.info("No more listings available.")
                    break

                for item in leads:
                    collected_leads.append(item)
                    await Actor.push_data(item)
                    if len(collected_leads) >= max_results:
                        break

                page += 1
                await asyncio.sleep(1.0)

        Actor.log.info(f"Completed! Harvested & pushed {len(collected_leads)} enriched leads to dataset.")

if __name__ == "__main__":
    asyncio.run(main())
