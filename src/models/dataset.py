import copy
from pandas import DataFrame, concat
from numpy import array, ndarray

from src.helpers.datasetHelper import DatasetHelper


class Dataset:
    _dataFrame: DataFrame
    _label: str

    def __init__(self, label: str, path: str = '', dataFrame: DataFrame = None):
        if path:
            self._dataFrame = DatasetHelper.readCsv(path)
        else:
            self._dataFrame = dataFrame

        self._label = label

        self.prepareDataset()

    def getDataset(self):
        """Gets a reference of the dataset object"""
        return self._dataFrame

    def getDatasetCopy(self):
        """Gets a copy of the dataset object"""
        return copy.copy(self._dataFrame)

    def copy(self):
        return copy.copy(self)

    def prepareDataset(self):
        """Modifies the dataset object with a user defined logic"""
        self._dataFrame = DatasetHelper.prepareDataset(self.getDatasetCopy())

    def getFeatureData(self):
        """Gets the data held in the feature columns"""
        return array(self._dataFrame.drop([self._label], 1))

    def getLabelData(self):
        return array(self._dataFrame[self._label])

    def updateLabelData(self, values: ndarray):
        self._dataFrame[self._label] = values

    def addRow(self, row: DataFrame):
        self._dataFrame = concat([row, self._dataFrame.iloc[:]])
