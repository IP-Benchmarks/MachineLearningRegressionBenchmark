import random


class RandomHelper:

    @staticmethod
    def randomInt(min: int, max: int):
        return random.randint(min, max)

    @staticmethod
    def randomFloat(max: float, digits=2) -> float:
        return round(random.random() * max, digits)

    @staticmethod
    def randomFloat(min: float, max: float, digits=2) -> float:
        return round(random.uniform(min, max), digits)
