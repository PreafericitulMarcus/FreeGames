import requests
from bs4 import BeautifulSoup



URL = "https://steamdb.info/upcoming/free/"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"

def fetch_steamdb_free_games():
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SteamDB data: {e}")
        return []

    table = soup.find("table", class_="table-products")
    # Skip the header row
    rows = table.find_all("tr")[1:] if table else []

    free_games = []

    for row in rows:
        cols = row.find_all("td")
        
        # Ensure we have all expected columns
        if len(cols) >= 5:
            try:
                name_tag = cols[1].find("a")
                title = name_tag.get_text(strip=True)
                promo_type = cols[3].get_text(strip=True)
                
                # Check for the specific promotion type
                if "Free to keep" in promo_type:
                    
                    # 1. Get Steam App ID from the SteamDB link
                    # e.g., /app/440/Team_Fortress_2/ -> '440' is the App ID
                    steamdb_path = name_tag.get("href")
                    app_id_match = re.search(r'/app/(\d+)/', steamdb_path)
                    
                    if not app_id_match:
                        continue # Skip if App ID cannot be found

                    app_id = app_id_match.group(1)
                    
                    # 2. Construct the direct Steam store link (the "claim link")
                    game_url = f"https://store.steampowered.com/app/{app_id}/"

                    # 3. Construct a standard Steam capsule image URL
                    image_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
                    
                    # 4. Extract end date (optional: SteamDB often lists this in cols[5])
                    end_date_cell = cols[5].get_text(strip=True)
                    
                    # SteamDB dates are a bit complex, but we can capture the raw text
                    # We can assume the time-limited promotions (Free to Keep) have an end date
                    end_date = end_date_cell if end_date_cell else "N/A"
                    
                    # SteamDB often shows a countdown in a different column/format on the main sales page.
                    # For this specific 'Upcoming/Free' list, the end date is the most reliable time info.

                    free_games.append({
                        "title": title,
                        "image_url": image_url,
                        "end_date": end_date,
                        # For "Free to Keep," the end date is the most useful time info
                        "countdown": f"Ends: {end_date}", 
                        "url": game_url,
                        "source": "Steam",
                    })

            except Exception as e:
                # Log the error for debugging, but continue scraping
                print(f"Error processing row on SteamDB: {e}")
                continue

    return free_games

if __name__ == "__main__":
    # Test the scraper
    games = fetch_steamdb_free_games()
    if games:
        print(f"Found {len(games)} 'Free to Keep' Steam games.")
        for game in games[:3]:
            print(f"- {game['title']} | Ends: {game['end_date']} | Link: {game['url']}")
    else:
        print("No free Steam games found on the targeted list.")