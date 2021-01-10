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
    resultingFunction = ''
    dataFrame: DataFrame = None
    dataSet: Dataset = None
    scaler: Scaler = None
    model: Model = None

    label = 'Y'

    @property
    def features(self):
        return [f'X{x}' for x in range(self.numberOfVariables)]

    def resetDatasetAndModel(self):
        self.dataFrame: DataFrame = None
        self.dataSet: Dataset = None
        self.scaler: Scaler = None
        self.model: Model = None
