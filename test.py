from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: Runs Chrome in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Install and use the correct ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Test by opening Google
driver.get("https://www.google.com")
print("Title:", driver.title)

# Close driver
driver.quit()
