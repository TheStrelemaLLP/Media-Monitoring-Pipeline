
from core_router import CoreRouter
from utils import setup_logger

# Initialize logger
logger = setup_logger("Main", log_file="logs/media_monitoring.log")

if __name__ == "__main__":
    logger.info("Media monitoring script started.")

    leader_list = [
        {"leader_name": "Devendra Fadnavis", "start_date": "07/21/2025", "end_date": "07/28/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
        {"leader_name": "Prakash Abitkar", "start_date": "07/21/2025", "end_date": "07/28/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
        {"leader_name": "Ashish Shelar", "start_date": "07/21/2025", "end_date": "07/28/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
        {"leader_name": "Ravindra Chavan", "start_date": "07/21/2025", "end_date": "07/28/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
        {"leader_name": "Eknath Shinde", "start_date": "07/21/2025", "end_date": "07/28/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
        # {"leader_name": "Shinraj Singh Chauhan", "start_date": "07/21/2025", "end_date": "07/28/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
        {"leader_name": "Chandrakant Patil", "start_date": "07/21/2025", "end_date": "07/28/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
        # {"leader_name": "Chandrashekhar Bawankule", "start_date": "07/21/2025", "end_date": "07/28/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},

        # {"leader_name": "Dhankar Resignation", "start_date": "07/21/2025", "end_date": "07/23/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
        # {"leader_name": "DF Birthday", "start_date": "07/22/2025", "end_date": "07/23/2025","facebook_excel_file_path":"C:/Users/HP/Downloads/CB_FB.xlsx"},
    
    ]

    n_pages = 30
    keywords_file_path = "C:/Users/HP/Desktop/Media-Monitoring/Input/search_query.xlsx"
    # "https://github.com/danish-strelema/Media-Monitoring/blob/main/Input/search_query.xlsx"
    output_filename = "C:/Users/HP/Desktop/Media-Monitoring/Output/extracted_links.xlsx"
    # "https://github.com/danish-strelema/Media-Monitoring/blob/main/Output/extracted_links.xlsx"
    #
    i_file_path = "C:/Users/HP/Desktop/Media-Monitoring/Input/Names_variations.xlsx"
    # "https://github.com/danish-strelema/Media-Monitoring/blob/main/Input/Names_variations.xlsx"
    # 
    output_folder_path = "C:/Users/HP/Downloads"
    # "https://github.com/danish-strelema/Media-Monitoring/tree/main/Output"
    # "C:/Users/HP/Downloads"
    chunk_size_kb = 250

    for leader_info in leader_list:
        leader_name = leader_info["leader_name"]
        start_date = leader_info["start_date"]
        end_date = leader_info["end_date"]
        facebook_excel_file_path =leader_info["facebook_excel_file_path"]

        logger.info(f"Processing started for leader: {leader_name} | From: {start_date} To: {end_date}")

        try:
            router = CoreRouter(
                leader_name, start_date, end_date, n_pages,
                keywords_file_path, output_filename,
                output_folder_path, facebook_excel_file_path,
                chunk_size_kb, i_file_path
            )
            router.process_news()
            logger.info(f"Successfully processed news for {leader_name}.")
        except Exception as e:
            logger.error(f"Error while processing {leader_name}: {e}", exc_info=True)

    logger.info("Media monitoring script finished.")
