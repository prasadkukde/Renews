from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import os


# Configure Chrome options



def scrape_competitor_news(query):
    url = f"https://www.arabianbusiness.com/tags/{query}"
    print(f"Scraping URL: {url}")

    # Optimize Chrome options for speed
    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") 
    options.add_argument("--headless=new")  # New headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.142 Safari/537.36")


    # Start WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        articles = set()  # Use a set to avoid duplicates
        news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))
        # Extract all visible articles
        for item in news_items:
            try:
                title_element = item.find_element(By.CSS_SELECTOR, "h2 > a")
                title = title_element.get_attribute("textContent")
                link = title_element.get_attribute("href")
                articles.add((title, link))  # Avoid duplicates
            except Exception as e:
                print(f"Error extracting news item: {e}")


    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()  # Ensure driver quits to free up resources

    return list(articles)

# Run scraper and print results
if __name__ == "__main__":
    articles = scrape_competitor_news("aldar")
    print(len(articles))
    if articles:
        for title, link in articles:
            print(f"{title}: {link}")
    else:
        print("No articles found.")
