from ..enums.scalerType import ScalerType
from sklearn import preprocessing
from pandas import DataFrame
from numpy import array
import joblib


class ScalerHelper:

    @staticmethod
    def getScaler(scalerType: ScalerType):
        """Returns the scaler based on the selected type"""
        _scalers = {
            ScalerType.StandardScaler: preprocessing.StandardScaler(),
            scalerType.MinMaxScaler: preprocessing.MinMaxScaler()
        }

        return _scalers[scalerType]

    @staticmethod
    def loadScaler(path: str):
        return joblib.load(path)

    @staticmethod
    def saveScaler(scaler, path: str):
        joblib.dump(scaler, path)

    @staticmethod
    def fit(scaler, data):
        scaler.fit(data)

    @staticmethod
    def scaleDataset(scaler, dataset: DataFrame) -> DataFrame:
        names = dataset.columns
        scaled_dataset = scaler.transform(dataset)
        scaled_dataset = DataFrame(scaled_dataset, columns=names)
        return scaled_dataset

    @staticmethod
    def scaleArray(scaler, npArray: array) -> array:
        return scaler.transform(npArray)
