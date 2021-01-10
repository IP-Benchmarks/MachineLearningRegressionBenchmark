from numpy import array, matrix
from typing import Union

from src.enums.modelType import ModelType
from src.helpers.modelHelper import ModelHelper


class Model:
    _model = None

    def __init__(self, modelType: ModelType = None, X: array = None, y: array = None, testSize: float = 0.2):
        X_train, X_test, y_train, y_test = ModelHelper.getTrainTestSplit(
            X, y, testSize)
        model = ModelHelper.getTrainingModel(modelType)
        self._model = ModelHelper.trainModel(model, X_train, y_train)

    def predict(self, data: Union[array, matrix]) -> array:
        return ModelHelper.predict(self._model, data)

    def evaluate(self, X: list, y: list) -> float:
        return ModelHelper.score(self._model, X, y)

    def getAlgorithmUsed(self):
        return type(self._model).__name__
