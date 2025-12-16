from datetime import datetime

import curl_cffi


def request_handle():
    URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    try:
        response = curl_cffi.get(URL, timeout=10)
        response.raise_for_status()
        content = response.json()
    except curl_cffi.exceptions.HTTPError as errh:
        raise SystemExit("HTTP Error:", errh)
    except curl_cffi.exceptions.Timeout as errt:
        raise SystemExit("Timeout Error:", errt)
    except curl_cffi.exceptions.JSONDecodeError as errj:
        raise SystemExit("Jsor Decode Error:", errj)
    return content


def is_free(game):
    promotions = game.get("promotions")
    discount_price = game.get("price", {}).get("totalPrice", {}).get("discountPrice")

    if discount_price == 0 and promotions != None:
        return True
    else:
        return False


def get_title(game):
    title = game.get("title", "Untitled")
    return title


def get_image_url(game):
    image_options = game.get("keyImages", [])
    image_url = "N/A"
    for image in image_options:
        if image.get("type") == "OfferImageWide":
            image_url = image.get("url")
        elif image.get("type") == "Thumbnail":
            image_url = image.get("url")
    return image_url


def get_end_of_promotion(game):
    promotions = game.get("promotions") or {}
    promotions_group = promotions.get("promotionalOffers") or []
    end_date_string = None
    if promotions_group and len(promotions_group) > 0:
        offers = promotions_group[0].get("promotionalOffers") or []
        if offers and len(offers) > 0:
            end_date_string = offers[0].get("endDate")
            if end_date_string:
                end_date_string = end_date_string.replace("Z", "+00:00")
    return end_date_string


def get_game_url(game):
    mappings = game.get("offerMappings")
    page_slug = None

    if mappings and len(mappings) > 0:
        page_slug = mappings[0].get("pageSlug")

    if not page_slug:
        page_slug = game.get("productSlug")

    if page_slug:
        return f"https://store.epicgames.com/en-US/p/{page_slug}"

    print(f"[Warning]: No slug found for game {game.get('title', 'Unknown')}")
    return None


def fetch_free_epic_games():
    response_data = request_handle()

    games_data = (
        response_data.get("data", {})
        .get("Catalog", {})
        .get("searchStore", {})
        .get("elements", [])
    )

    free_games = []
    for game in games_data:
        if not is_free(game):
            continue

        free_games.append(
            {
                "title": get_title(game),
                "image_url": get_image_url(game),
                "end_date": get_end_of_promotion(game),
                "url": get_game_url(game),
                "source": "Epic Games",
            }
        )

    return free_games
