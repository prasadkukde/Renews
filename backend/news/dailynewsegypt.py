from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
import chromedriver_autoinstaller

def scrape_dailyegypt_news():
    url = "https://www.dailynewsegypt.com/category/business/real-estate-a-construction/"
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

        for i in range(0,3):
            # Wait for articles to load
            news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.p-wrap")))
            # Extract all visible articles
            for item in news_items:
                try:
                    title_element = item.find_element(By.CSS_SELECTOR, "a.p-url")
                    title = title_element.get_attribute("textContent")
                    link = title_element.get_attribute("href")
                    articles.add((title, link))  # Avoid duplicates
                except Exception as e:
                    print(f"Error extracting news item: {e}")

            # Try to find and click the "Load More" button
            try:
                load_more_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                driver.execute_script("arguments[0].click();", load_more_button)  # Click using JS
                time.sleep(2)  # Allow new articles to load
            except Exception:
                print("No more articles to load.")
                break  # Exit loop when "Load More" button is not found

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()  # Ensure driver quits to free up resources

    return list(articles)

# Run scraper and print results
if __name__ == "__main__":
    articles = scrape_dailyegypt_news()
    print(len(articles))
    if articles:
        for title, link in articles:
            print(f"{title}: {link}")
    else:
        print("No articles found.")
