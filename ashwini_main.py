from link_extraction import Link_extraction

def main():
    leader_name = "Siddharth Shirole"
    start_date = "07/09/2025"
    end_date ="07/10/2025"

    n_pages = 30

    keywords_file_path = "C:/Users/HP/Desktop/Media-Monitoring/search_query.xlsx"
    output_filename = "C:/Users/HP/Desktop/Media-Monitoring/extracted_links.xlsx"

    link_extraction = Link_extraction(leader_name, start_date, end_date, n_pages, keywords_file_path, output_filename)

    try:
        link_extraction.fetch_links()

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()