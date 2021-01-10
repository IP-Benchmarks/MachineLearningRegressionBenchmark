from pandas import DataFrame
from numpy import ndarray
from typing import Union

from src.enums.scalerType import ScalerType
from src.helpers.scalerHelper import ScalerHelper


class Scaler:
    _scaler = None

    def __init__(self, scalerType: ScalerType, data: Union[ndarray, DataFrame]):
        self._scaler = ScalerHelper.getScaler(scalerType)
        self.fitScaler(data)

    def fitScaler(self, data: Union[ndarray, DataFrame]):
        ScalerHelper.fit(self._scaler, data)

    def transform(self, data: Union[ndarray, DataFrame]):
        if isinstance(data, ndarray):
            return ScalerHelper.scaleArray(self._scaler, data)
        else:
            return ScalerHelper.scaleDataset(self._scaler, data)
