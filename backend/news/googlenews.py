from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
import chromedriver_autoinstaller
import undetected_chromedriver as uc

def scrape_google_news(query):
    url = f"https://www.google.com/search?q={query}++real+estate+news&sca_esv=f72a643d70be9e1f&biw=1366&bih=641&tbm=nws&sxsrf=AHTn8zq7UgztTVobTWltAtMDDWQ_A-xapg%3A1741267064106&ei=eKDJZ8iaBpP_1e8PxZXmoQs&ved=0ahUKEwjItsKmxfWLAxWTf_UHHcWKObQQ4dUDCA4&uact=5&oq=saudi++real+estate+news&gs_lp=Egxnd3Mtd2l6LW5ld3MiF3NhdWRpICByZWFsIGVzdGF0ZSBuZXdzSABQAFgAcAB4AJABAJgBAKABAKoBALgBA8gBAJgCAKACAJgDAJIHAKAHAA&sclient=gws-wiz-news"
    print(f"Scraping URL: {url}")

    chromedriver_autoinstaller.install()
    # Optimize Chrome options for speed
    options = Options()
    
    options.binary_location = "/usr/bin/chromium-browser" 
    
    options.add_argument("--headless=new")  # New headless mode for better performance
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # Reduce logging to improve performance
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Start WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        articles = set()  # Use a set to avoid duplicates

        for i in range(0,1):
            # Wait for articles to load
            news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.SoaBEf")))

            # Extract all visible articles
            for item in news_items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "div.n0jPhd").text
                    link = item.find_element(By.CSS_SELECTOR, "a.WlydOe").get_attribute("href")
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
    articles = scrape_google_news("saudi")
    print(len(articles))
    if articles:
        for title, link in articles:
            print(f"{title}: {link}")
    else:
        print("No articles found.")
