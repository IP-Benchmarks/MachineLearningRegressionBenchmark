from src.models.dataset import Dataset
from src.models.model import Model
from src.models.scaler import Scaler
from pandas import DataFrame


class Store:
    maxNumberOfVariables = 20
    minNumberOfVariables = 1
    numberOfVariables = None
    maxCoeff = 500
    maxExp = 10
    maxValue = 50
    minValue = 0
    numberOfSamples = 1000
    parametersArr = [{'exp': 1, 'coeff': 1}
                     for _ in range(maxNumberOfVariables)]

    features = [f'X{x}' for x in range(numberOfVariables)]
    label = 'Y'
    dataFrame: DataFrame = None

    dataSet: Dataset = None
    scaler: Scaler = None
    model: Model = None
