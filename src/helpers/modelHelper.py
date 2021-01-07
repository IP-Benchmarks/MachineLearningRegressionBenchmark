from ..enums.modelType import ModelType
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from numpy import array, matrix
from typing import Union
from sklearn.linear_model import BayesianRidge, LassoLars, ARDRegression, PassiveAggressiveRegressor, \
    TheilSenRegressor, LinearRegression
from sklearn.tree import DecisionTreeRegressor
import joblib


class ModelHelper:
    @staticmethod
    def getTrainingModel(modelType: ModelType):
        """Returns the training model based on the selected type"""
        _models = {
            ModelType.LinearRegression: LinearRegression(n_jobs=-1),
            ModelType.ARDRegression: ARDRegression(),
            ModelType.PassiveAggressiveRegressor: PassiveAggressiveRegressor(),
            ModelType.TheilSenRegressor: TheilSenRegressor(n_jobs=-1),
            ModelType.DecisionTreeRegressor: DecisionTreeRegressor()
        }

        return _models[modelType]

    @staticmethod
    def loadModel(path: str):
        return joblib.load(path)

    @staticmethod
    def saveModel(model, path: str):
        joblib.dump(model, path)

    @staticmethod
    def getTrainTestSplit(X: array = None, y: array = None, testSize: float = 0.2):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=testSize)
        return X_train, X_test, y_train, y_test

    @staticmethod
    def trainModel(model, X_train, y_train):
        return model.fit(X_train, y_train)

    @staticmethod
    def predict(model, data: Union[array, matrix]):
        return model.predict(data)

    @staticmethod
    def score(model, X, y, testSize: float = 0.2) -> list:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=testSize)
        return model.score(X_test, y_test)
