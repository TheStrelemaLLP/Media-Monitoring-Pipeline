# modules/adder.py
from utils import setup_logger

logger = setup_logger("Adder")

class Adder:
    def add(self, a, b):
        try:
            result = a + b
            logger.info(f"Added {a} and {b}, result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error adding {a} and {b}: {e}")
            raise
