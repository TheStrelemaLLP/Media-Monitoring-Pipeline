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
    def __init__(self, leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename, facebook_excel_file_path):
        """
        Initializes an instance of the class with provided parameters.

        Parameters:
        - leader_name (str): Name of the political leader to monitor or analyze.
        - start_date (str): Start date for the analysis period (format: 'MM/DD/YYYY' or similar).
        - end_date (str): End date for the analysis period.
        - n_pages (int): Number of pages to scrape or process (e.g., for web scraping or document parsing).
        - keywords_file_path (str): Path to the file containing keywords for filtering or analysis.
        - output_filename (str): Name of the output file where the results will be saved.
        """
        self.leader_name = leader_name
        self.start_date = start_date
        self.end_date = end_date
        self.n_pages = n_pages
        self.keywords_file_path = keywords_file_path
        self.output_filename = output_filename
        self.facebook_excel_file_path = facebook_excel_file_path
        logger.info(f"Initialized Link_extraction for leader: {leader_name}, from {start_date} to {end_date}")

    # =======================================

    def setup_driver(self):
        """
        Sets up and initializes a headless Chrome WebDriver instance using Selenium and ChromeDriverManager.

        Configures browser options to:
        - Run in headless mode (no GUI).
        - Disable automation detection features.
        - Start the browser maximized.
        - Use a custom user-agent to mimic a real browser session.

        Returns:
        - driver (webdriver.Chrome): A configured Selenium Chrome WebDriver instance.

        Raises:
        - Exception: If the WebDriver fails to initialize, logs the error and re-raises the exception.
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            logger.info("WebDriver initialized successfully")
            return driver
        except Exception as e:
            logger.exception("Failed to initialize WebDriver")
            raise

    # ====================================

    def keywords_extraction(self, file_path, sheet_name, pages):
        """
        Extracts keywords from a specified Excel sheet and prepares a dictionary mapping 
        each keyword to the given number of pages.

        Parameters:
        - file_path (str): Path to the Excel file containing keyword data.
        - sheet_name (str): Name of the sheet from which to read keywords.
        - pages (int): Number of pages to associate with each keyword (used for further processing like scraping).

        Returns:
        - keyword_dict (dict): Dictionary where keys are keywords and values are the specified page count.
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            keyword_dict = {keyword: pages for keyword in df['Keyword']}
            logger.info(f"Extracted {len(keyword_dict)} keywords from sheet '{sheet_name}'")
            logger.debug(f"Keywords extracted: {keyword_dict}")
            return keyword_dict
        except Exception as e:
            logger.exception(f"Failed to extract keywords from file '{file_path}', sheet '{sheet_name}'")
            raise

    # ==================================================

    def link_filtering(self, data):
        """
        Filters out duplicate entries from a list of dictionaries containing 'Title' and 'Links'.

        Parameters:
        - data (list of dict): A list where each item is a dictionary with keys 'Title' and 'Links',
        representing article titles and corresponding URLs.

        Returns:
        - df_without_duplicates (DataFrame): A pandas DataFrame containing unique (Title, Link) pairs only.
        """
        try:
            # Convert the input list of dictionaries into a DataFrame
            df = pd.DataFrame(data, columns=["Title", "Links"])

            # Remove exact duplicate rows (based on both Title and Links)
            df_without_duplicates = df.drop_duplicates()

            logger.info(f"Filtered {len(data)} links down to {len(df_without_duplicates)} unique entries")
            return df_without_duplicates
        except Exception as e:
            logger.exception("Error during link filtering")
            raise

    # ================================================

    def save_links(self, df, output_filename):
        """
        Saves the given DataFrame of links to an Excel file and prints summary information.

        Parameters:
        - df (DataFrame): A pandas DataFrame containing the extracted links (and possibly titles).
        - output_filename (str): Name of the Excel file to save the data into.

        Outputs:
        - Prints the total number of links extracted.
        - Confirms the output file location.
        """
        try:
            # Save the DataFrame to an Excel file without the index column
            df.to_excel(output_filename, index=False)

            # Print summary information
            logger.info(f"Total links extracted: {len(df)}")
            logger.info(f"Data saved to '{output_filename}'")
        except Exception as e:
            logger.exception(f"Failed to save DataFrame to file '{output_filename}'")
            raise

    # =================================================

    def fetch_links(self):
        """
        Automates the process of fetching news article links and titles from Google News search results 
        for a list of keywords over a given date range.

        Steps:
        - Extracts keywords and their respective page limits.
        - Sets up a headless Chrome browser using Selenium.
        - Performs Google News searches for each keyword.
        - Iterates through multiple pages of results per keyword.
        - Extracts article titles and URLs.
        - Filters out duplicate entries.
        - Saves the cleaned data to an Excel file.

        Returns:
        - None (results are saved to an Excel file defined by `self.output_filename`).
        """
        logger.info("Starting fetch_links() process")

        try:
            keywords_with_pages = self.keywords_extraction(
                self.keywords_file_path,
                self.leader_name,
                self.n_pages
            )
        except Exception:
            logger.error("Keyword extraction failed. Exiting fetch_links().")
            return

        try:
            driver = self.setup_driver()
        except Exception:
            logger.error("WebDriver setup failed. Exiting fetch_links().")
            return

        data = []

        for search_query, num_pages in keywords_with_pages.items():
            try:
                logger.info(f"Searching for: {search_query} ({num_pages} pages)")
                news_url = f"https://www.google.co.in/search?q={search_query.replace(' ', '+')}&tbm=nws&tbs=cdr:1,cd_min:{self.start_date},cd_max:{self.end_date}"
                driver.get(news_url)
                time.sleep(5)  # Allow time for page to load

                for page in range(1, num_pages + 1):
                    time.sleep(3)  # Short delay to mimic human behavior
                    logger.debug(f"Processing page {page} for query: '{search_query}'")

                    try:
                        titles = driver.find_elements(By.XPATH, "//div[@class='n0jPhd ynAwRc MBeuO nDgy9d']")
                        link_elements = driver.find_elements(By.XPATH, "//a[@jsname='YKoRaf']")

                        for title_elem, link_elem in zip(titles, link_elements):
                            link = link_elem.get_attribute("href")
                            title = title_elem.text.strip()
                            # Filter out links pointing back to Google
                            if link and "google.com" not in link:
                                data.append({
                                    "Title": title,
                                    "Links": link
                                })
                                logger.debug(f"Collected: {title} | {link}")

                        # Try to navigate to the next page of results
                        try:
                            next_button = driver.find_element(By.ID, "pnnext")
                            next_url = next_button.get_attribute("href")
                            if next_url:
                                driver.get(next_url)
                            else:
                                logger.warning(f"No more pages found for '{search_query}' after {page} pages.")
                                break
                        except Exception:
                            logger.warning(f"No 'Next' button found for '{search_query}' after {page} pages.")
                            break

                    except Exception as e:
                        logger.exception(f"Error on page {page} for keyword '{search_query}'")
                        continue

            except Exception as e:
                logger.exception(f"Error occurred while processing keyword: {search_query}")
                continue

        driver.quit()
        logger.info("Browser session closed")

        try:
            df_without_duplicates = self.link_filtering(data)
            self.save_links(df_without_duplicates, self.output_filename)
            logger.info("Link extraction completed and saved successfully")
        except Exception:
            logger.error("Final filtering or saving failed")