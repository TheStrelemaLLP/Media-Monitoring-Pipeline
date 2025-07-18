# from modules.adder import Adder
# from modules.divider import Divider
# from modules.news_scraper import NewsScraper
# from modules.chunking import split_docx_by_article_chunks
# from modules.facebook_docs import create_facebook_doc
# import os
# from modules.link_extraction import Link_extraction

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

from core_router import CoreRouter
from utils import setup_logging

if __name__ == "__main__":
    setup_logging()

    leader_name = "Devendra Fadnavis"
    start_date = "07/15/2025"
    end_date ="07/17/2025"

    n_pages = 30

    keywords_file_path = "C:/Users/HP/Desktop/Media-Monitoring/Input/search_query.xlsx"
    output_filename = "C:/Users/HP/Desktop/Media-Monitoring/Output/extracted_links.xlsx"

    facebook_excel_file_path = "C:/Users/HP/Downloads/CB_FB.xlsx"  # Replace with your Facebook Excel file path, or set to None if not used
    output_folder_path = "C:/Users/HP/Downloads"  # Replace with your desired output folder
    chunk_size_kb = 250  # Size limit for each chunk in KB

    router = CoreRouter(leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename, output_folder_path)

    router.process_news()

    # question = "who is Sidharth Shirole?"
    # answer = router.generate_answer(question)
