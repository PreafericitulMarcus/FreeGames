import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

API = (
    "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    "?locale=en-US&country=US"
)


def fetch_free_epic_games():
    response = requests.get(API, timeout=10)
    response.raise_for_status()
    data = response.json()
    games = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])

    free_games = []

    for game in games:
        promotions = game.get("promotions") or {}
        offer_windows = [] # this may be null in the page
        offer_windows.extend(promotions.get("promotionalOffers", []))
        offer_windows.extend(promotions.get("upcomingPromotionalOffers", []))

        discount_price = (
            game.get("price", {}).get("totalPrice", {}).get("discountPrice")
        )

        if discount_price == 0 and offer_windows:
            title = game.get("title", "Untitled")

            image_url = next(
                (img.get("url") for img in game.get("keyImages", []) if img.get("type") == "OfferImageWide"),
                next((img.get("url") for img in game.get("keyImages", []) if img.get("type") == "Thumbnail"), "N/A"),
            )

            chosen_offer = None
            for window in offer_windows:
                offers = window.get("promotionalOffers", [])
                if offers:
                    chosen_offer = offers[0]
                    break

            end_date_str = chosen_offer.get("endDate")

            try:
                end_dt = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))

                bucharest = ZoneInfo("Europe/Bucharest")
                end_dt_buch = end_dt.astimezone(bucharest)
                end_date = end_dt_buch.strftime("%Y-%m-%d %H:%M:%S %Z")

                now_utc = datetime.now(timezone.utc)
                delta = end_dt - now_utc
                if delta.total_seconds() <= 0:
                    countdown = "Expired"
                else:
                    days = delta.days
                    hours = delta.seconds // 3600
                    minutes = (delta.seconds % 3600) // 60
                    countdown = f"{days}d {hours}h {minutes}m"
            except Exception:
                end_date = end_date_str or "N/A"
                countdown = end_date_str or "N/A"

            page_slug = (
                game.get("pageSlug")
                or next((m.get("pageSlug") for m in game.get("offerMappings", []) if m.get("pageSlug")), None)
                or (chosen_offer.get("pageSlug") if chosen_offer and chosen_offer.get("pageSlug") else None)
                or game.get("productSlug")
                or game.get("urlSlug")
                or ""
            )
            game_url = f"https://store.epicgames.com/en-US/p/{page_slug}" if page_slug else "N/A"

            free_games.append(
                {
                    "title": title,
                    "image_url": image_url,
                    "end_date": end_date,
                    "countdown": countdown,
                    "url": game_url,
                    "source": "Epic Games"
                }
            )

    return free_games

