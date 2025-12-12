# modules/link_extraction.py
import os
import sys
import time

# Add parent directory to path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from utils import setup_logger


logger = setup_logger("Link_extraction")


class Link_extraction:
    def __init__(
        self,
        leader_name,
        start_date,
        end_date,
        n_pages,
        keywords_file_path,
        output_filename,
        facebook_excel_file_path,
    ):
        """
        Initializes an instance of the class with provided parameters.

        Parameters:
        - leader_name (str): Name of the political leader to monitor or analyze.
        - start_date (str): Start date for the analysis period (format: 'MM/DD/YYYY' or similar).
        - end_date (str): End date for the analysis period.
        - n_pages (int): Number of pages to scrape per keyword.
        - keywords_file_path (str): Path to the file containing keywords for filtering or analysis.
        - output_filename (str): Name of the output file where the results will be saved.
        - facebook_excel_file_path (str): (Currently unused) path to FB file if needed later.
        """
        self.leader_name = leader_name
        self.start_date = start_date
        self.end_date = end_date
        self.n_pages = n_pages
        self.keywords_file_path = keywords_file_path
        self.output_filename = output_filename
        self.facebook_excel_file_path = facebook_excel_file_path
        logger.info(
            f"Initialized Link_extraction for leader: {leader_name}, "
            f"from {start_date} to {end_date}"
        )


    def setup_driver(self):
        """
        Sets up and initializes a (optionally headless) Chrome WebDriver instance.

        Returns:
        - driver (webdriver.Chrome): A configured Selenium Chrome WebDriver instance.
        """
        # Uncomment next line if you want fully headless:
        options = Options()
        options.add_argument("--headless=new")   # use new headless mode
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("start-maximized")
        # user-agent...
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            logger.info("WebDriver initialized successfully")
            return driver
        except Exception:
            logger.exception("Failed to initialize WebDriver")
            raise


    def keywords_extraction(self, file_path, sheet_name, pages):
        """
        Extracts keywords from a specified Excel sheet and prepares a dictionary mapping
        each keyword to the given number of pages.
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            keyword_dict = {keyword: pages for keyword in df["Keyword"]}
            logger.info(
                f"Extracted {len(keyword_dict)} keywords from sheet '{sheet_name}'"
            )
            logger.debug(f"Keywords extracted: {keyword_dict}")
            return keyword_dict
        except Exception:
            logger.exception(
                f"Failed to extract keywords from file '{file_path}', "
                f"sheet '{sheet_name}'"
            )
            raise



    def link_filtering(self, data):
        """
        Filters out duplicate entries from a list of dictionaries containing:
        'Keyword', 'Page', 'Title', 'Links'.

        Parameters:
        - data (list of dict)

        Returns:
        - df_without_duplicates (DataFrame): Unique (Title, Link) pairs
          while keeping other columns.
        """
        try:
            # Convert the input list of dictionaries into a DataFrame
            df = pd.DataFrame(data)

            # In case some rows are missing columns, ensure they exist
            for col in ["Keyword", "Page", "Title", "Links"]:
                if col not in df.columns:
                    df[col] = None

            # Remove duplicates based on Title + Links
            df_without_duplicates = df.drop_duplicates(subset=["Title", "Links"])

            logger.info(
                f"Filtered {len(data)} rows down to "
                f"{len(df_without_duplicates)} unique entries"
            )
            return df_without_duplicates
        except Exception:
            logger.exception("Error during link filtering")
            raise



    def save_links(self, df, output_filename):
        """
        Saves the given DataFrame of links to an Excel file and logs summary information.
        Ensures parent directory exists before writing.
        """
        try:
            parent_dir = os.path.dirname(os.path.abspath(output_filename))
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
                logger.info(f"Created parent directory: {parent_dir}")

            df.to_excel(output_filename, index=False)
            logger.info(f"Total links extracted: {len(df)}")
            logger.info(f"Data saved to '{output_filename}'")
        except Exception:
            logger.exception(f"Failed to save DataFrame to file '{output_filename}'")
            raise




    def fetch_links(self):
        """
        Automates the process of fetching news article links and titles from Google News
        search results for a list of keywords over a given date range.

        Uses newer Google layout logic from the standalone script:
        - Result locator: //a[.//div[@role='heading']]
        - Title from nested div[@role='heading']
        - Pagination using //a[@id='pnnext' or @aria-label='Next']
        """
        logger.info("Starting fetch_links() process")

        # 1) Get keywords + page counts
        try:
            keywords_with_pages = self.keywords_extraction(
                self.keywords_file_path, self.leader_name, self.n_pages
            )
        except Exception:
            logger.error("Keyword extraction failed. Exiting fetch_links().")
            return

        # 2) Start driver
        try:
            driver = self.setup_driver()
        except Exception:
            logger.error("WebDriver setup failed. Exiting fetch_links().")
            return

        data = []

        # 3) Loop over keywords
        for search_query, num_pages in keywords_with_pages.items():
            try:
                logger.info(f"Searching for: {search_query} ({num_pages} pages)")

                url = (
                    f"https://www.google.com/search?"
                    f"q={search_query.replace(' ', '+')}"
                    f"&tbm=nws&tbs=cdr:1,cd_min:{self.start_date},cd_max:{self.end_date}"
                )

                driver.get(url)
                time.sleep(5)  # Allow page to load

                # 4) Loop over pages for this keyword
                for page in range(1, num_pages + 1):
                    logger.debug(f"Processing page {page} for '{search_query}'")
                    time.sleep(2)

                    try:
                        # ---------------------------------------------
                        # FETCH RESULTS (no clicking / no new tabs)
                        # ---------------------------------------------
                        results = driver.find_elements(
                            By.XPATH, "//a[.//div[@role='heading']]"
                        )
                        logger.debug(
                            f"Found {len(results)} results on page {page} "
                            f"for '{search_query}'"
                        )

                        for r in results:
                            try:
                                title_element = r.find_element(
                                    By.XPATH, ".//div[@role='heading']"
                                )
                                title = title_element.text.strip()
                                link = r.get_attribute("href")

                                if link and "google.com" not in link:
                                    data.append(
                                        {
                                            "Keyword": search_query,
                                            "Page": page,
                                            "Title": title,
                                            "Links": link,
                                        }
                                    )
                                    logger.debug(
                                        f"Collected ({search_query}, page {page}): "
                                        f"{title} | {link}"
                                    )
                            except Exception:
                                logger.exception(
                                    "Error extracting title/link from a result element"
                                )
                                continue

                        # ---------------------------------------------
                        # PAGINATION (new Google layout logic)
                        # ---------------------------------------------
                        try:
                            next_btn = driver.find_element(
                                By.XPATH, "//a[@id='pnnext' or @aria-label='Next']"
                            )
                            driver.execute_script("arguments[0].click();", next_btn)
                            time.sleep(4)
                        except Exception:
                            logger.warning(
                                f"No more pages available for '{search_query}' "
                                f"after page {page}."
                            )
                            break

                    except Exception:
                        logger.exception(
                            f"Error on page {page} for keyword '{search_query}'"
                        )
                        continue

            except Exception:
                logger.exception(
                    f"Error occurred while processing keyword: {search_query}"
                )
                continue

        # 5) Clean up driver
        try:
            driver.quit()
            logger.info("Browser session closed")
        except Exception:
            logger.exception("Error while closing the browser")

        # 6) Filter + save
        try:
            df_without_duplicates = self.link_filtering(data)
            self.save_links(df_without_duplicates, self.output_filename)
            logger.info("Link extraction completed and saved successfully")
        except Exception:
            logger.error("Final filtering or saving failed")