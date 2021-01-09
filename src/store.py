from models.dataset import Dataset
from models.model import Model
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
    model: Model = None
