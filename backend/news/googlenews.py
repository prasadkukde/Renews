import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Suppress __del__ error
uc.Chrome.__del__ = lambda self: None

def scrape_google_news(query):
    url = f"https://www.google.com/search?q={query}+real+estate+news&tbm=nws"
    print(f"Scraping URL: {url}")

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.142 Safari/537.36")

    driver = uc.Chrome(version_main=134, options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        articles = set()
        news_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.SoaBEf")))

        for item in news_items:
            try:
                title = item.find_element(By.CSS_SELECTOR, "div.n0jPhd").text.strip()
                link = item.find_element(By.CSS_SELECTOR, "a.WlydOe").get_attribute("href")
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
    articles = scrape_google_news("saudi")
    print(len(articles))
    if articles:
        for title, link in articles:
            print(f"{title}: {link}")
    else:
        print("No articles found.")
