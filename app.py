from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import sys

if __name__ == "__main__":
    logging.info("Starting the application")

    try:
        a=1/0
    except Exception as e:
        logging.info("Custom exception")
        raise CustomException(e,sys)