from core_router import CoreRouter
from utils import setup_logger
import os
import pandas as pd
import shutil

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)   # remove file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # remove folder and its contents
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Base directory of project (where main.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure required directories exist
LOGS_DIR = os.path.join(BASE_DIR, "logs")
INPUT_DIR = os.path.join(BASE_DIR, "Input")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize logger
logger = setup_logger("Main", log_file=os.path.join(LOGS_DIR, "media_monitoring.log"))

if __name__ == "__main__":
    logger.info("Media monitoring script started.")

    n_pages = 30

    # Example file paths
    input_leaders_file = os.path.join(INPUT_DIR, "input_leaders.xlsx")
    keywords_file_path = os.path.join(INPUT_DIR, "search_query.xlsx")
    
    i_file_path = os.path.join(INPUT_DIR, "Names_variations.xlsx")
    output_folder_path = OUTPUT_DIR
    clear_folder(output_folder_path)

    chunk_size_kb = 500

    leader_list = pd.read_excel(input_leaders_file)
    
    
    for leader_name, start_date, end_date, fb_file in zip(leader_list["leader_name"],leader_list["start_date"],leader_list["end_date"],leader_list["facebook_profile_url"]):

        leader_folder_path = os.path.join(OUTPUT_DIR, leader_name)
        os.makedirs(leader_folder_path, exist_ok=True)
        output_folder_path = leader_folder_path

        output_filename = os.path.join(leader_folder_path, "extracted_links.xlsx")

        facebook_excel_file_path = str(fb_file)
        # os.path.join(INPUT_DIR, str(fb_file))

        logger.info(
            f"Processing started for leader: {leader_name} | From: {start_date} To: {end_date} with "
        )

        try:
            router = CoreRouter(
                leader_name,
                start_date,
                end_date,
                n_pages,
                keywords_file_path,
                output_filename,
                output_folder_path,
                facebook_excel_file_path,
                chunk_size_kb,
                i_file_path,
            )
            router.process_news()
            logger.info(f"Successfully processed news for {leader_name}.")
        except Exception as e:
            logger.error(f"Error while processing {leader_name}: {e}", exc_info=True)

    logger.info("Media monitoring script finished.")
