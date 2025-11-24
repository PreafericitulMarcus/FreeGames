import json
import os
from providers.epic_games import fetch_free_epic_games

DATA_FILE = os.path.join(os.path.dirname(__file__), "gamedata", "games.json")

def update_free_games_data():
    """Runs all scrapers, compiles results, and saves to JSON."""
    all_games = []

    # 1. Fetch Epic Games
    try:
        epic_games = fetch_free_epic_games()
        all_games.extend(epic_games)
        print(f"Found {len(epic_games)} free games from Epic.")
    except Exception as e:
        print(f"Error fetching Epic Games: {e}")
        # Decide if you want to proceed if one scraper fails

    # 2. Add SteamDB and GOG fetch calls here later

    # Save the compiled data
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(all_games, f, indent=4)
        print(f"Successfully saved {len(all_games)} total free games to games.json.")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def load_free_games_data():
    """Loads the last saved game data from JSON."""
    update_free_games_data()
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return []
