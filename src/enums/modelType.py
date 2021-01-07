from enum import Enum


class ModelType(Enum):
    LinearRegression = 0
    ARDRegression = 1
    PassiveAggressiveRegressor = 2
    TheilSenRegressor = 3
    DecisionTreeRegressor = 4
