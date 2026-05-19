from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Options Chrome
options = Options()
options.add_argument("--headless")  # mode headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

# Si tu veux spécifier le binaire Chromium explicitement
options.binary_location = "/usr/bin/chromium-browser"

# Service pointant vers ChromeDriver
service = Service("/usr/bin/chromedriver")

print("Script démarré")

# Lancement du navigateur
driver = webdriver.Chrome(service=service, options=options)

# Aller sur la page
driver.get("https://www.python.org")

# Afficher le titre
print("Titre de la page:", driver.title)

driver.quit()