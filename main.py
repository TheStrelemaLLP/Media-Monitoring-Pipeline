from core_router import CoreRouter
from utils import setup_logger
import os

# Base directory of project (where main.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure required directories exist
LOGS_DIR = os.path.join(BASE_DIR, "logs")
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize logger
logger = setup_logger("Main", log_file=os.path.join(LOGS_DIR, "media_monitoring.log"))

if __name__ == "__main__":
    logger.info("Media monitoring script started.")

    leader_list = [
        {
            "leader_name": "Devendra Fadnavis",
            "start_date": "07/21/2025",
            "end_date": "07/28/2025",
            "facebook_excel_file_path": os.path.join(INPUT_DIR, "CB_FB.xlsx"),  # <- moved into input/
        },
        # Add more leaders here if needed
    ]

    n_pages = 30

    # Example file paths
    keywords_file_path = os.path.join(INPUT_DIR, "search_query.xlsx")
    output_filename = os.path.join(OUTPUT_DIR, "extracted_links.xlsx")
    i_file_path = os.path.join(INPUT_DIR, "Names_variations.xlsx")
    output_folder_path = OUTPUT_DIR

    chunk_size_kb = 250

    for leader_info in leader_list:
        leader_name = leader_info["leader_name"]
        start_date = leader_info["start_date"]
        end_date = leader_info["end_date"]
        facebook_excel_file_path = leader_info["facebook_excel_file_path"]

        logger.info(
            f"Processing started for leader: {leader_name} | From: {start_date} To: {end_date}"
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
