from modules.adder import Adder
from modules.divider import Divider
from modules.news_scraper import NewsScraper
from modules.chunking import split_docx_by_article_chunks
from modules.facebook_docs import create_facebook_doc
import os
from link_extraction import Link_extraction

def main():
    try:
        leader_name = "Prakash Abitkar"
        start_date = "07/12/2025"
        end_date ="07/17/2025"

        n_pages = 30

        keywords_file_path = "C:/Users/HP/Desktop/Media-Monitoring/search_query.xlsx"
        output_filename = "C:/Users/HP/Desktop/Media-Monitoring/extracted_links.xlsx"

        # excel_file_path = output_filename  # Replace with your news Excel file path
        facebook_excel_file_path = "C:/Users/HP/Downloads/CB_FB.xlsx"  # Replace with your Facebook Excel file path, or set to None if not used
        output_folder_path = "C:/Users/HP/Downloads"  # Replace with your desired output folder
        # leader = "Devendra Fadnavis"  # Define leader name for chunking and Facebook doc
        chunk_size_kb = 250  # Size limit for each chunk in KB

        print("1. Link Extraction.....")
        link_extraction = Link_extraction(leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename)
        link_extraction.fetch_links()

        print("2. News Extraction.....")
        # Initialize and run the news scraper
        scraper = NewsScraper(file_path=output_filename, output_folder=output_folder_path, leader=leader_name)
        scraper.scrape()

        # Get the paths to the news output files
        docx_path, excel_path = scraper.get_output_paths()
        print(f"News Word document saved at: {docx_path}")
        if excel_path:
            print(f"Failed news links saved at: {excel_path}")

        # Split the news Word document into chunks
        print(f"\nSplitting news Word document into chunks of {chunk_size_kb} KB...")
        chunk_paths = split_docx_by_article_chunks(
            input_path=docx_path,
            chunk_size_kb=chunk_size_kb,
            output_dir=output_folder_path,
            leader=leader_name
        )
        print(f"Chunked news files saved at: {', '.join(chunk_paths)}")

        # Process Facebook posts if an Excel file is provided
        if facebook_excel_file_path and os.path.exists(facebook_excel_file_path):
            print(f"\nProcessing Facebook posts from {facebook_excel_file_path}...")
            facebook_doc_path = create_facebook_doc(
                excel_file_path=facebook_excel_file_path,
                output_dir=output_folder_path,
                leader=leader_name
            )
            print(f"Facebook Word document saved at: {facebook_doc_path}")
        else:
            print("\nNo Facebook Excel file provided or file does not exist. Skipping Facebook processing.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()