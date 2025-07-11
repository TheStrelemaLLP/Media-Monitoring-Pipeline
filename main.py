# main.py
from modules.adder import Adder
from modules.divider import Divider

def main():
    adder = Adder()
    divider = Divider()

    try:
        print("Addition:", adder.add(10, 5))
        print("Division:", divider.divide(10, 2))
        print("Faulty Division:", divider.divide(10, 0))  # This will cause exception
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
