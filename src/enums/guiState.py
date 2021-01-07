from enum import Enum


class GuiState(Enum):
    GenerateData = 0
    TrainModel = 1
    Predict = 2
    Output = 3
