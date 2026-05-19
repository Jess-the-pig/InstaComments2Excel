import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
POST_URL = "https://www.instagram.com/p/DYSE2juo4jA/"
COOKIES_FILE = "cookie.json"
OUTPUT_FILE = "comments.xlsx"

# --- CHROME ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/chromium-browser"

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)


# ---------------------------
# COOKIES
# ---------------------------
def load_cookies(filepath):
    try:
        with open(filepath, "r") as f:
            cookies = json.load(f)

        print(f"🍪 {len(cookies)} cookies chargés")
        return cookies
    except Exception as e:
        print("❌ Erreur cookies:", e)
        return []


try:
    print("🚀 Démarrage...")

    # 1. OUVRIR INSTAGRAM
    driver.get("https://www.instagram.com/")
    time.sleep(5)

    # 2. AJOUT COOKIES
    cookies = load_cookies(COOKIES_FILE)

    for cookie in cookies:
        try:
            cookie.pop("sameSite", None)
            cookie.pop("expiry", None)
            driver.add_cookie(cookie)
        except:
            pass

    # 3. ACTIVER SESSION
    driver.refresh()
    time.sleep(5)

    print("✅ Session chargée")

    # 4. OUVRIR POST
    driver.get(POST_URL)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    print("📍 Post chargé")

    # ---------------------------
    # SCROLL COMMENTAIRES
    # ---------------------------
    body = driver.find_element(By.TAG_NAME, "body")

    for i in range(10):
        body.send_keys(Keys.END)
        time.sleep(2)
        print(f"Scroll {i+1}/10")

    print("📜 Scroll terminé")

    # ---------------------------
    # 🔥 EXTRACTION CORRIGÉE
    # ---------------------------
    print("🔍 Recherche container commentaires...")

    time.sleep(5)

    # ouverture zone commentaires (si bouton présent)
    try:
        btns = driver.find_elements(By.XPATH, "//span")
        for b in btns:
            if "comment" in b.text.lower():
                b.click()
                break
        time.sleep(3)
    except:
        pass

    # extraction brute fiable
    elements = driver.find_elements(By.XPATH, "//div//span")

    print("Spans trouvés:", len(elements))

    comments = []

    for el in elements:
        try:
            text = el.text.strip()

            if len(text) < 2:
                continue

            if text in ["Like", "Reply", "View replies", "Hide replies"]:
                continue

            comments.append(text)

        except:
            pass

    print("\n✅ EXEMPLE COMMENTAIRES:")
    for c in comments[:30]:
        print("-", c)


    # ---------------------------
    # DEBUG EXPORT HTML (CORRECTEMENT PLACÉ)
    # ---------------------------
    with open("debug_instagram.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("💾 HTML sauvegardé")

finally:
    driver.quit()
    print("🛑 Fin")