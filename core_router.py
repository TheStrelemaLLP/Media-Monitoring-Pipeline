import os
import traceback
from urllib.parse import urlparse

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
from requests.exceptions import RequestException

from utils import setup_logger
from modules.news_scraper import NewsScraper
from modules.chunking import Chunking
from modules.facebook_docs import Facebook_doc
from modules.link_extraction import Link_extraction


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
    def __init__(self, leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename, output_folder_path, facebook_excel_file_path, chunk_size_kb, i_file_path):
        self.link_extraction = Link_extraction(leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename, facebook_excel_file_path)
        self.scraper = NewsScraper(file_path=output_filename, output_folder=output_folder_path, leader=leader_name, chunk_size_kb = chunk_size_kb, i_file_path = i_file_path, link_extraction = self.link_extraction)
        self.facebook_doc = Facebook_doc()
        self.chunking = Chunking()
    
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
            print(f"\nSplitting news Word document into chunks of {self.scraper.chunk_size_kb} KB...")
            chunk_paths = self.chunking.split_docx_by_article_chunks(
                input_path=docx_path,
                chunk_size_kb=self.scraper.chunk_size_kb,
                output_dir=self.scraper.output_folder,
                leader=self.link_extraction.leader_name
            )
            print(f"Chunked news files saved at: {', '.join(chunk_paths)}")
        else:
            print(f"\nNo chunking required.")

        # Process Facebook posts if an Excel file is provided
        if self.link_extraction.facebook_excel_file_path and os.path.exists(self.link_extraction.facebook_excel_file_path):
            print(f"\nProcessing Facebook posts from {self.link_extraction.facebook_excel_file_path}...")
            facebook_doc_path = self.facebook_doc.create_facebook_doc(
                excel_file_path=self.link_extraction.facebook_excel_file_path,
                output_dir=self.scraper.output_folder,
                leader=self.link_extraction.leader_name
            )
            print(f"Facebook Word document saved at: {facebook_doc_path}")
        else:
            print("\nNo Facebook Excel file provided or file does not exist. Skipping Facebook processing.")
