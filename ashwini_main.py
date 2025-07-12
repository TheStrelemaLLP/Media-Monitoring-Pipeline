from parameter import Parameter
from link_extraction import Link_extraction

def main():
    parameterder = Parameter()
    link_extraction = Link_extraction()

    try:
        print("Leader Name:", parameterder.leader_name)
        print("Start Date:", parameterder.start_date)
        print("End Date:", parameterder.end_date) 


    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()