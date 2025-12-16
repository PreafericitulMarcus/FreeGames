from core.providers.epic_games import fetch_free_epic_games

# from .steam import SteamScrapper

__all__ = ["fetch_free_epic_games", "PROVIDER_MAP"]

PROVIDER_MAP = {
    # "steam": SteamScrapper,
    "epic_games": fetch_free_epic_games
}
