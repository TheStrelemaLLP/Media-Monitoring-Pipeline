from parameter import Parameter
from link_extraction import Link_extraction

def main():
    parameterder = Parameter()
    link_extraction = Link_extraction()

    try:
        print("Leader Name:", parameterder.leader_name)
        print("Start Date:", parameterder.start_date)
        print("End Date:", parameterder.end_date)

        leader_name = parameterder.leader_name
        start_date = parameterder.start_date
        end_date = parameterder.end_date
        n_pages = parameterder.n_pages
        keywords_file_path = parameterder.keywords_file_path
        output_filename = parameterder.output_filename

        driver = link_extraction.setup_driver()
        keyword_dict = link_extraction.keywords_extraction(keywords_file_path, leader_name, n_pages)
        data = link_extraction.fetch_links(driver, keyword_dict, start_date, end_date)
        df_without_duplicates = link_extraction.link_filtering(data)
        link_extraction.save_links(df_without_duplicates, output_filename)

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()