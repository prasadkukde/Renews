import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os


def scrape_properties(url):

    print(f"Scraping URL: {url}")

    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") 
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    properties = []
    try:

        cnt = 0
        for i in range(0,3):
        # while True:
            print("Page number: ", cnt + 1)
            cnt += 1
            news_items = driver.find_elements(By.CSS_SELECTOR, "li.a37d52f0")
            for item in news_items:
                try:
                    price = "AED: " + item.find_element(By.CSS_SELECTOR, "span[aria-label='Price']").text
                    title = item.find_element(By.CSS_SELECTOR, "h2.f0f13906").text
                    type_of_apt = item.find_element(By.CSS_SELECTOR, "span[aria-label='Type']").text
                    
                    no_of_beds = item.find_element(By.CSS_SELECTOR, "span._1822ec30 span._19e94678[aria-label='Beds']").text + " Beds"
                    no_of_baths = item.find_element(By.CSS_SELECTOR, "span[aria-label='Baths']").text + " Baths"

                    area = item.find_element(By.CSS_SELECTOR, "span[aria-label='Area'] h4").text
                    if area == "":
                        continue
                    location = item.find_element(By.CSS_SELECTOR, "h3._4402bd70").text
                    link = item.find_element(By.CSS_SELECTOR, "a.d40f2294").get_attribute("href")

                    properties.append(
                        {
                            "Type": type_of_apt,
                            "Beds": no_of_beds,
                            "Baths": no_of_baths,
                            "Area": area,
                            "Price": price,
                            "Title": title,
                            "Location": location,
                            "Link": link,
                        }
                    )
                except Exception as e:
                    print(f"Error extracting property details: {e}")

            try:
                load_more_button = driver.find_element(By.CSS_SELECTOR, "a[title='Next']")
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(2)
            except Exception:
                print("No more articles to load.")
                break

    except Exception as e:
        print(f"Error loading page: {e}")

    driver.quit()
    return properties


# Example usage
if __name__ == '__main__':
    property_data = []

    companies = [   
                    # 'mag'
                  'sobha'
                #   'aldar'
                #   'emaar'
                #   'damac'
                #   'nakheel'
                #   'meraas'
                #  'danube'
                 ]  
    for comp in companies:
        property_data += scrape_properties(comp)
        
    # for i in property_data:
    #     print(i['Beds'], i['Title'])

    file_path = "combined_data.xlsx"

    print("Data appended successfully!")

    df = pd.DataFrame(property_data)

    df['Price (Numeric)'] = df['Price'].str.extract(r'(\d[\d,]*)')[0].str.replace(',', '').astype(float)

    df = df.sort_values(by=['Type', 'Beds', 'Baths', 'Price (Numeric)'])

    df.drop('Price (Numeric)', axis=1, inplace=True)


    # df.to_excel("combined_data.xlsx", index=False)
    existing_data = pd.read_excel(file_path, engine='openpyxl')
    updated_data = pd.concat([existing_data, df], ignore_index=True)


    # Save to Excel
    updated_data.to_excel(file_path, index=False, engine='openpyxl')
    print("Excel file 'combined_data.xlsx' has been created successfully.")
