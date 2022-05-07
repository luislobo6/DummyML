from random import Random
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("prediction.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class RandomGenerator():

    def __init__(self, seed: int) -> None:
        logger.debug(f"RandomGenerator created, seed = {seed}")
        self.seed = seed
        self.random = Random(seed)

    def get_random_number(self):
        logger.debug("get_random_number")
        return self.random.random()
    
    def get_random_int(self, start: int, end: int):
        logger.debug(f"get_random_int(start = {start}, end = {end}")
        return self.random.randint(start, end)
    
    def get_random_float(self, start: float, end: float):
        logger.debug(f"get_random_float(start = {start}, end = {end}")
        return self.random.uniform(start, end)

    def set_seed(self, seed: int):
        logger.debug(f"set_seed = {seed}")
        self.seed = seed
        return self