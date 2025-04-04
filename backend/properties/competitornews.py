from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



chrome_driver_path = r"C:\Users\PRASAD KUKDE\Downloads\chromedriver-win64\chromedriver.exe"

def scrape_competitor_news(query):
    url = f"https://www.arabianbusiness.com/tags/{query}"
    print(f"Scraping URL: {url}")

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

        articles = set()

        news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))
        for item in news_items:
            try:
                title_element = item.find_element(By.CSS_SELECTOR, "h2 > a")
                title = title_element.get_attribute("textContent").strip()
                link = title_element.get_attribute("href")
                articles.add((title, link))
            except Exception as e:
                print(f"Error extracting news item: {e}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        try:
            driver.quit()
        except:
            pass
        del driver

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
