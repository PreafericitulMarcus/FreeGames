import requests
from datetime import datetime, timezone

def request_handle():
    URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        content =  response.json()
    except request.exceptions.HTTPError as errh:
        raise SystemExit("HTTP Error:", errh)
    except request.exeptions.Timeout as errt:
        raise SystemExit("Timeout Error:", errt)
    except requests.exceptions.JSONDecodeError as errj:
        raise SystemExit("Jsor Decode Error:", errj)
    return content

def validate_free(game):
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

def get_countdown_end_of_promotion(game):
    end_date_string = game.get("promotions", {}).get("promotionalOffers", [])[0].get("promotionalOffers", [])[0].get("endDate")
    end_date = datetime.fromisoformat(end_date_string.replace("Z", "+00:00"))

    now_date = datetime.now(timezone.utc)

    until_expiration = end_date - now_date
    days = until_expiration.days
    hours = until_expiration.seconds // 3600
    minutes = (until_expiration.seconds % 3600) // 60 

    countdown =f"{days}d {hours}h {minutes}m" 

    return countdown

def get_game_url(game):
    page_slug = game.get("offerMappings", [])[0].get("pageSlug")
    game_url = f"https://store.epicgames.com/en-US/p/{page_slug}"
    return game_url

def fetch_free_epic_games():
    response_data = request_handle()

    games_data = response_data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])

    free_games = []
    for game in games_data:
        if validate_free(game) == False:
            continue

        free_games.append(
            {
                "title": get_title(game),
                "image_url": get_image_url(game),
                "countdown": get_countdown_end_of_promotion(game),
                "url": get_game_url(game),
                "source": "Epic Games"
            }
        )

    return free_games
