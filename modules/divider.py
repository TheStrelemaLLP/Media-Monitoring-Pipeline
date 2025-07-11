# modules/divider.py
from logger import setup_logger
logger = setup_logger("Divider")

class Divider:
    def divide(self, a, b):
        try:
            result = a / b
            logger.info(f"Divided {a} by {b}, result: {result}")
            return result
        except ZeroDivisionError as e:
            logger.warning(f"Tried dividing {a} by zero")
            raise ValueError("Cannot divide by zero") from e
        except Exception as e:
            logger.error(f"Error dividing {a} by {b}: {e}")
            raise
