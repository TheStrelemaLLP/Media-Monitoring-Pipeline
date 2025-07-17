from modules.adder import Adder
from modules.divider import Divider
from modules.news_scraper import NewsScraper
from modules.chunking import split_docx_by_article_chunks
from modules.facebook_docs import create_facebook_doc
import os


def main():
    adder = Adder()
    divider = Divider()

    try:
        excel_file_path = "C:/Users/HP/Documents/Media Monitoring/Devendra Fadnavis/7 July to 14 July 2025/DF_14th_July.xlsx"  # Replace with your news Excel file path
        facebook_excel_file_path = "C:/Users/HP/Documents/Media Monitoring/Chandrashekhar Bawankule/19th May to 26th May 2025/CB_FB.xlsx"  # Replace with your Facebook Excel file path, or set to None if not used
        output_folder_path = "C:/Users/HP/Downloads"  # Replace with your desired output folder
        leader = "Devendra Fadnavis"  # Define leader name for chunking and Facebook doc
        chunk_size_kb = 250  # Size limit for each chunk in KB

        # Initialize and run the news scraper
        scraper = NewsScraper(file_path=excel_file_path, output_folder=output_folder_path, leader=leader)
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
            leader=leader
        )
        print(f"Chunked news files saved at: {', '.join(chunk_paths)}")

        # Process Facebook posts if an Excel file is provided
        if facebook_excel_file_path and os.path.exists(facebook_excel_file_path):
            print(f"\nProcessing Facebook posts from {facebook_excel_file_path}...")
            facebook_doc_path = create_facebook_doc(
                excel_file_path=facebook_excel_file_path,
                output_dir=output_folder_path,
                leader=leader
            )
            print(f"Facebook Word document saved at: {facebook_doc_path}")
        else:
            print("\nNo Facebook Excel file provided or file does not exist. Skipping Facebook processing.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()