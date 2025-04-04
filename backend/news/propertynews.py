# https://www.propertynews.ae/?s=real+estate
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = r"C:\Users\PRASAD KUKDE\Downloads\chromedriver-win64\chromedriver.exe"

def scrape_property_news():
    url = "https://www.propertynews.ae/?s=real+estate"
    print(f"Scraping URL: {url}")

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Run in headless mode (remove if debugging)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.142 Safari/537.36")

    # Set up Chrome WebDriver with Service
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        articles = set()  # Use a set to avoid duplicates

        for i in (0,2):
            # Wait for articles to load
            news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.jeg_post")))

            # Extract all visible articles
            for item in news_items:
                try:
                    title_element = item.find_element(By.CSS_SELECTOR, "h3 > a")
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
        try:
            driver.quit()
        except Exception as e:
            print(f"Safe quit error: {e}")
        del driver
        
    return list(articles)

# Run scraper and print results
if __name__ == "__main__":
    articles = scrape_property_news()
    print(len(articles))
    if articles:
        for title, link in articles:
            print(f"{title}: {link}")
    else:
        print("No articles found.")
