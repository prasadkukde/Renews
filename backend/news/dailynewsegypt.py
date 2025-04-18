from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time



def scrape_dailyegypt_news():
    url = "https://www.dailynewsegypt.com/category/business/real-estate-a-construction/"
    print(f"Scraping URL: {url}")

    # Set up Chrome options
    options = Options()
    options.add_argument("--headless=new")  # Run in headless mode (remove if debugging)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.142 Safari/537.36")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        articles = set()  # Avoid duplicates

        # while True:
        for i in (0,3):
            try:
                news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.p-wrap")))
                for item in news_items:
                    try:
                        title_element = item.find_element(By.CSS_SELECTOR, "a.p-url")
                        title = title_element.get_attribute("textContent")
                        link = title_element.get_attribute("href")
                        articles.add((title, link))
                    except Exception as e:
                        print(f"Error extracting news item: {e}")
            except Exception:
                print("Timeout while waiting for news items.")
                break

            # Try to click "Load More" (next)
            try:
                load_more_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(2)  # Let new content load
            except Exception:
                print("No more articles to load.")
                break

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
    articles = scrape_dailyegypt_news()
    print(len(articles))
    if articles:
        for title, link in articles:
            print(f"{title}: {link}")
    else:
        print("No articles found.")
