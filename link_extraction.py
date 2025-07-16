# modules/link_extraction.py
from utils import setup_logger
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

logger = setup_logger("Link_extraction")

class Link_extraction:
    def __init__(self, leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename):
        self.leader_name = leader_name
        self.start_date = start_date
        self.end_date = end_date
        self.n_pages = n_pages
        self.keywords_file_path = keywords_file_path
        self.output_filename = output_filename

    def setup_driver(self):
        # Set up Chrome options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

        try:
            # Initialize WebDriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            logging.info("WebDriver initialized successfully")
            return driver
        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {e}")
            raise

    # ====================================

    def keywords_extraction(self, file_path, sheet_name, pages):
        # Read the specific sheet for leader
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # prepare keyword dictionary for leader
        keyword_dict = {keyword: pages for keyword in df['Keyword']}   
        return keyword_dict
    
    # ====================================

    # ==================================================

    def link_filtering(self, data):
        df = pd.DataFrame(data, columns=["Title", "Links"])
        df_without_duplicates = df.drop_duplicates()
        return df_without_duplicates
    # ================================================

    def save_links(self, df, output_filename):
        df.to_excel(output_filename, index=False)

        print(f"Total links extracted: {len(df)}")
        print(f"Data saved to '{output_filename}'")
    # =================================================

    def fetch_links(self):
        # keywords_with_pages = Link_extraction.keywords_extraction(self.keywords_file_path, self.leader_name)

        keywords_with_pages = self.keywords_extraction(self.keywords_file_path, self.leader_name, self.n_pages)

        # set up driver
        driver = self.setup_driver()
        
        # Data storage
        data = []

        # Iterate through keywords and page limits
        for search_query, num_pages in keywords_with_pages.items():
            print(f"Searching for: {search_query} ({num_pages} pages)")

            news_url = f"https://www.google.co.in/search?q={search_query.replace(' ', '+')}&tbm=nws&tbs=cdr:1,cd_min:{self.start_date},cd_max:{self.end_date}"
            driver.get(news_url)
            time.sleep(5)

            for page in range(1, num_pages + 1):
                time.sleep(3)

                # Extract titles and links
                titles = driver.find_elements(By.XPATH, "//div[@class='n0jPhd ynAwRc MBeuO nDgy9d']")
                link_elements = driver.find_elements(By.XPATH, "//a[@jsname='YKoRaf']")

                for title_elem, link_elem in zip(titles, link_elements):
                    link = link_elem.get_attribute("href")
                    title = title_elem.text.strip()
                    if link and "google.com" not in link:
                        data.append({
                            "Title": title,
                            "Links": link
                        })

                # Try to go to next page
                try:
                    next_button = driver.find_element(By.ID, "pnnext")
                    next_url = next_button.get_attribute("href")
                    if next_url:
                        driver.get(next_url)
                    else:
                        print(f"No more pages found for '{search_query}' after {page} pages.")
                        break
                except:
                    print(f"No 'Next' button found for '{search_query}' after {page} pages.")
                    break

        driver.quit()

        df_without_duplicates = self.link_filtering(data)

        self.save_links(df_without_duplicates, self.output_filename)

        # return data

    # # ==================================================

    # def link_filtering(self, data):
    #     df = pd.DataFrame(data, columns=["Title", "Links"])
    #     df_without_duplicates = df.drop_duplicates()
    #     return df_without_duplicates
    # # ================================================

    # def save_links(self, df, output_filename):
    #     df.to_excel(output_filename, index=False)

    #     print(f"Total links extracted: {len(df)}")
    #     print(f"Data saved to '{output_filename}'")
