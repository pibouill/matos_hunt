# Listing Tracker

# **WIP**

Second hand websites listing tracker

## Prerequisites

1. Python 3.x installed.
2. A Telegram account.

## Installation

1. Clone or download the script.
2. Install the required Python dependencies:
```bash
pip install requests beautifulsoup4 python-dotenv
```

## Configuration

Before running the script, you need to gather your specific variables and add them to your environment file.

### Step 1: Obtaining Environment Variables

**1. `TELEGRAM_TOKEN` (Creating your Bot)**
* Open Telegram and search for **@BotFather**.
* Send the message `/newbot` to start the creation process.
* Follow the prompts: give your bot a display name and a unique username (must end in `bot`, e.g., `MyBazosTrackerBot`).
* @BotFather will reply with a confirmation message containing your **HTTP API Token** (it will look something like `1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ`). Copy this exact string.

**2. `CHAT_ID` (Connecting to your Bot)**
* First, you must activate your new bot. Search for your newly created bot's username in Telegram and send it a message (like `/start` or "hello"). If you skip this, the bot will not have permission to message you.
* Next, search Telegram for **@userinfobot** (or **@getmyid_bot**).
* Send it the message `/start`.
* It will reply with your personal `Id` (a string of numbers, e.g., `123456789`). Copy this number. This tells the bot exactly who to send the alerts to.

**3. `SEARCH_URL` (Setting your Target)**
* Open your web browser and go to `www.bazos.cz`.
* Search for your desired item.
* Apply any necessary filters directly on the site (e.g., selecting the "Hudba" category, entering your postal code).
* Once the search results show exactly what you want to monitor, copy the entire URL from your browser's address bar (e.g., `https://hudba.bazos.cz/?hledat=xone+96...`).

### Step 2: Setting up the `.env` file

1. Create a `.env.sample` file in the project directory (commit this to your repository):
```env
TELEGRAM_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
MAX_PRICE_CZK=5000
SEARCH_URL=https://www.bazos.cz/search.php?hledat=your_search_term
```

2. Copy the sample file to create your active environment file:
```bash
cp .env.sample .env
```

3. Open `.env` and configure your settings:
   * Paste your `TELEGRAM_TOKEN`.
   * Paste your `CHAT_ID`.
   * Set your `MAX_PRICE_CZK` limit (use numbers only, no currency symbols).
   * Paste your specific `SEARCH_URL`.

*(Note: Ensure your Python script includes `from dotenv import load_dotenv` and calls `load_dotenv()` at the top to read these variables using `os.getenv('TELEGRAM_TOKEN')`, etc.)*

## Usage

Run the script manually to test it:
```bash
python script.py
```
*Note: The first run creates a `seen_listings.json` file in the same directory to store the URLs of listings it has already alerted you about, preventing duplicate notifications.*

## Automation

To act as a continuous monitor, schedule the script to run automatically in the background. 

**Linux/macOS (Cron):**
Open your terminal, run `crontab -e`, and add this line to run the script every 15 minutes:
```bash
*/15 * * * * cd /absolute/path/to/your/script && /usr/bin/python3 script.py
```
*(Changing into the directory first ensures the script finds the `.env` and `.json` files correctly).*

**Windows:**
1. Open **Task Scheduler** and click **Create Task**.
2. Under **Triggers**, set it to run daily, and repeat the task every 15 minutes indefinitely.
3. Under **Actions**, set the program/script to your `python.exe` path.
4. Put `script.py` in the "Add arguments" box.
5. Put the absolute path to your script's folder in the "Start in (optional)" box to ensure it loads the `.env` file correctly.

---

## FB Marketplace (!)

This script does **not** support Facebook Marketplace.

Unlike Bazoš, which uses static HTML and is easy to parse, Facebook actively and aggressively fights automated scraping. Building a custom Python script for Facebook Marketplace is highly discouraged because:

* **Dynamic Obfuscation:** CSS classes are randomly generated (e.g., `<div class="x193iq5w">`) and change constantly, making it impossible to reliably target elements like the title or price.
* **No Static HTML:** Content is rendered dynamically via complex JavaScript.
* **Aggressive Blocking:** Automated requests without proper session cookies and human-like behavior will quickly result in IP bans or account suspensions.

### Recommended Alternatives for Facebook
If you need to monitor Facebook Marketplace, use one of these external tools and solutions instead of a custom script:

**1. Browser Extensions (Easiest & Safest)**
These run directly in your active browser using your existing Facebook login and cookies. 
* **[Distill Web Monitor](https://distill.io/):** The gold standard for this. Select the results grid on FB Marketplace and set it to alert you on changes.
* **[Visualping](https://visualping.io/):** Another popular alternative that visually compares page changes. 
* *Warning:* Set the check interval to 30–60 minutes. Checking too frequently (e.g., every 5 minutes) will get your account temporarily flagged by Facebook.

**2. Cloud Scrapers & No-Code Bots (Intermediate)**
Managed services that maintain the infrastructure, proxies, and code required to bypass anti-bot measures.
* **[Apify](https://apify.com/):** Has pre-built "Actors" specifically designed to scrape Facebook Marketplace into clean JSON data. You will likely need to provide session cookies from a "burner" account.
* **[Browse AI](https://www.browse.ai/):** A no-code platform where you can record yourself navigating Facebook Marketplace, and it will build a monitoring robot based on your actions.

**3. Headless Browsers (For Developers)**
If you insist on writing the code yourself, you must mimic human behavior in an invisible browser. It is incredibly fragile and requires constant maintenance.
* **[Playwright](https://playwright.dev/):** Microsoft's modern browser automation framework.
* **[Selenium](https://www.selenium.dev/):** The legacy standard for browser automation.
* **[Puppeteer](https://pptr.dev/):** Google's Node.js API for Chrome/Chromium.
