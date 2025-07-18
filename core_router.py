from modules.news_scraper import NewsScraper
from modules.chunking import split_docx_by_article_chunks
from modules.facebook_docs import create_facebook_doc
import os
from modules.link_extraction import Link_extraction
from utils import setup_logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.shared import RGBColor
from tqdm import tqdm
import os
import traceback
from urllib.parse import urlparse
from requests.exceptions import RequestException

logger = setup_logger("CoreRouter")

# Custom exceptions
class NewsScraperError(Exception):
    """Base exception for NewsScraper errors."""
    pass

class InvalidLeaderError(NewsScraperError):
    """Raised when an invalid leader is specified."""
    pass

class FileAccessError(NewsScraperError):
    """Raised when file operations fail."""
    pass

class WebScrapingError(NewsScraperError):
    """Raised when web scraping fails."""
    pass

# Placeholder for utility functions
def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and special characters."""
    return ' '.join(text.strip().split()) if text else ''

def ensure_heading_style(doc: Document, style_name: str, level: int):
    """Ensure heading style exists in the document."""
    try:
        return doc.styles[style_name]
    except KeyError:
        logger.error(f"Style '{style_name}' not found in document.")
        raise NewsScraperError(f"Document style '{style_name}' is missing.")

def is_valid_url(url: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class CoreRouter:
    def __init__(self, leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename, output_folder_path):
        self.link_extraction = Link_extraction(leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename)
        self.scraper = NewsScraper(file_path=output_filename, output_folder=output_folder_path, leader=leader_name)

    def process_news(self):
        print("1. Link Extraction.....")
        self.link_extraction.fetch_links()

        print("2. News Extraction.....")
        self.scraper.scrape()

        # Get the paths to the news output files
        docx_path, excel_path = self.scraper.get_output_paths()
        print(f"News Word document saved at: {docx_path}")
        if excel_path:
            print(f"Failed news links saved at: {excel_path}")

        # Get the file size in bytes
        size_bytes = os.path.getsize(docx_path)

        # Convert to kilobytes (1 KB = 1024 bytes)
        size_kb = size_bytes / 1024

        print(f"File size: {size_kb:.2f} KB")

        if size_kb >= 350:
            # Split the news Word document into chunks
            print(f"\nSplitting news Word document into chunks of {self.chunk_size_kb} KB...")
            chunk_paths = split_docx_by_article_chunks(
                input_path=docx_path,
                chunk_size_kb=self.chunk_size_kb,
                output_dir=self.output_folder_path,
                leader=self.leader_name
            )
            print(f"Chunked news files saved at: {', '.join(chunk_paths)}")
        else:
            print(f"\nNo chunking required.")

        # Process Facebook posts if an Excel file is provided
        if self.facebook_excel_file_path and os.path.exists(self.facebook_excel_file_path):
            print(f"\nProcessing Facebook posts from {self.facebook_excel_file_path}...")
            facebook_doc_path = create_facebook_doc(
                excel_file_path=self.facebook_excel_file_path,
                output_dir=self.output_folder_path,
                leader=self.leader_name
            )
            print(f"Facebook Word document saved at: {facebook_doc_path}")
        else:
            print("\nNo Facebook Excel file provided or file does not exist. Skipping Facebook processing.")


# def main():
#     try:
#         leader_name = "Devendra Fadnavis"
#         start_date = "07/15/2025"
#         end_date ="07/17/2025"

#         n_pages = 30

#         keywords_file_path = "C:/Users/HP/Desktop/Media-Monitoring/Input/search_query.xlsx"
#         output_filename = "C:/Users/HP/Desktop/Media-Monitoring/Output/extracted_links.xlsx"

#         # excel_file_path = output_filename  # Replace with your news Excel file path
#         facebook_excel_file_path = "C:/Users/HP/Downloads/CB_FB.xlsx"  # Replace with your Facebook Excel file path, or set to None if not used
#         output_folder_path = "C:/Users/HP/Downloads"  # Replace with your desired output folder
#         # leader = "Devendra Fadnavis"  # Define leader name for chunking and Facebook doc
#         chunk_size_kb = 250  # Size limit for each chunk in KB

#         print("1. Link Extraction.....")
#         link_extraction = Link_extraction(leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename)
#         link_extraction.fetch_links()

#         print("2. News Extraction.....")
#         # Initialize and run the news scraper
#         scraper = NewsScraper(file_path=output_filename, output_folder=output_folder_path, leader=leader_name)
#         scraper.scrape()

#         # Get the paths to the news output files
#         docx_path, excel_path = scraper.get_output_paths()
#         print(f"News Word document saved at: {docx_path}")
#         if excel_path:
#             print(f"Failed news links saved at: {excel_path}")

#         # Get the file size in bytes
#         size_bytes = os.path.getsize(docx_path)

#         # Convert to kilobytes (1 KB = 1024 bytes)
#         size_kb = size_bytes / 1024

#         print(f"File size: {size_kb:.2f} KB")

#         if size_kb >= 350:
#             # Split the news Word document into chunks
#             print(f"\nSplitting news Word document into chunks of {chunk_size_kb} KB...")
#             chunk_paths = split_docx_by_article_chunks(
#                 input_path=docx_path,
#                 chunk_size_kb=chunk_size_kb,
#                 output_dir=output_folder_path,
#                 leader=leader_name
#             )
#             print(f"Chunked news files saved at: {', '.join(chunk_paths)}")
#         else:
#             print(f"\nNo chunking required.")

#         # Process Facebook posts if an Excel file is provided
#         if facebook_excel_file_path and os.path.exists(facebook_excel_file_path):
#             print(f"\nProcessing Facebook posts from {facebook_excel_file_path}...")
#             facebook_doc_path = create_facebook_doc(
#                 excel_file_path=facebook_excel_file_path,
#                 output_dir=output_folder_path,
#                 leader=leader_name
#             )
#             print(f"Facebook Word document saved at: {facebook_doc_path}")
#         else:
#             print("\nNo Facebook Excel file provided or file does not exist. Skipping Facebook processing.")

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     main()