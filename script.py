# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    script.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: pibouill <pibouill@student.42prague.com>   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/01 10:13:04 by pibouill          #+#    #+#              #
#    Updated: 2026/04/01 10:13:04 by pibouill         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- CONFIGURATION ---
# Retrieve variables from the environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MAX_PRICE_ENV = os.getenv("MAX_PRICE_CZK")
SEARCH_URL = os.getenv("SEARCH_URL")

SEEN_FILE = "seen_listings.json"
# ---------------------

# Basic validation to ensure the .env file is set up correctly
if not all([TELEGRAM_TOKEN, CHAT_ID, MAX_PRICE_ENV, SEARCH_URL]):
    print("Error: Missing environment variables. Please check your .env file.")
    sys.exit(1)

try:
    MAX_PRICE_CZK = int(MAX_PRICE_ENV) if MAX_PRICE_ENV else 0
except (ValueError, TypeError):
    print("Error: MAX_PRICE_CZK in your .env file must be a number.")
    sys.exit(1)


def send_telegram_alert(message):
    """Sends a message via Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")


def load_seen_listings() -> List[str]:
    """Loads previously seen listing URLs to avoid duplicate alerts."""
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_seen_listings(seen_list: List[str]) -> None:
    """Saves the current list of seen URLs."""
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen_list, f, indent=4)


def check_bazos() -> None:
    """Scrapes the Bazoš search URL and checks for new items under the price limit."""
    headers: Dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    if not SEARCH_URL:
        print("Error: SEARCH_URL is not set in the environment.")
        return

    try:
        response = requests.get(SEARCH_URL, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch Bazoš: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    seen_listings = load_seen_listings()
    new_seen = list(seen_listings)

    # Bazoš wraps listings in a div with the class 'inzeraty'
    listings = soup.find_all("div", class_="inzeraty")

    if not listings:
        print("No listings found on the page. Check your SEARCH_URL.")
        return

    for listing in listings:
        title_element = listing.find("h2", class_="nadpis")
        if not title_element:
            continue

        title = title_element.text.strip()
        link_element = title_element.find("a")
        if not link_element:
            continue

        # Construct the full URL (handling relative paths)
        href = link_element["href"]
        if href.startswith("http"):
            link = href
        else:
            if SEARCH_URL:
                base_url = "/".join(SEARCH_URL.split("/")[:3])
                link = base_url + href
            else:
                continue

        # Extract the price
        price_div = listing.find("div", class_="inzeratycena")
        if not price_div:
            continue

        price_text = price_div.text.strip()

        # Clean the price string
        try:
            # Keep only digits
            price_digits = "".join(filter(str.isdigit, price_text))
            if not price_digits:
                continue
            price = int(price_digits)
        except ValueError:
            continue

        # Check against constraints
        if price <= MAX_PRICE_CZK and link not in seen_listings:
            message = (
                f"🚨 *New Bazoš Alert!*\n\n*Item:* {title}\n*Price:* "
                f"{price} CZK\n*Link:* [Click here to view]({link})"
            )
            send_telegram_alert(message)
            new_seen.append(link)
            print(f"Alert sent for: {title}")

    # Save the updated list of URLs so we don't alert on them again
    save_seen_listings(new_seen)


if __name__ == "__main__":
    print("Checking Bazoš...")
    check_bazos()
    print("Done.")
