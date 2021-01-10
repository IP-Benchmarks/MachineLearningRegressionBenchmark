import PySimpleGUI as sg
from operator import itemgetter

from src.enums.guiState import GuiState
from src.enums.modelType import ModelType
from src.enums.scalerType import ScalerType
from src.helpers.datasetHelper import DatasetHelper
from src.helpers.plotterHelper import PlotterHelper
from src.models.dataset import Dataset
from src.models.model import Model
from src.models.scaler import Scaler
from src.store import Store
from src.helpers.randomHelper import RandomHelper


class Gui:
    _store = Store()
    _window = None
    _state = GuiState.GenerateData

    _models = [{"key": "model" + str(x.value), "value": x}
               for x in ModelType]
    _selectedModel = ModelType.LinearRegression
    _subscriptMap = {
        "0": "₀",
        "1": "₁",
        "2": "₂",
        "3": "₃",
        "4": "₄",
        "5": "₅",
        "6": "₆",
        "7": "₇",
        "8": "₈",
        "9": "₉",
        "10": "₁₀",
        "11": "₁₁",
        "12": "₁₂",
        "13": "₁₃",
        "14": "₁₄",
        "15": "₁₅",
        "16": "₁₆",
        "17": "₁₇",
        "18": "₁₈",
        "19": "₁₉",
        "20": "₂₀",
    }

    def start(self):
        sg.theme('DarkBlue')
        self._window = sg.Window('Regression Benchmark', self.createLayout(),
                                 icon="./assets/ico.ico", finalize=True)
        self._window.read(timeout=10)
        self._window['numberOfVariables'].update(self._store.numberOfVariables)
        self._window['maxCoeff'].update(self._store.maxCoeff)
        self._window['maxExp'].update(self._store.maxExp)
        self._window['minValue'].update(self._store.minValue)
        self._window['maxValue'].update(self._store.maxValue)
        self._window['numberOfSamples'].update(self._store.numberOfSamples)
        self.updateDisplayedModel(self._selectedModel)
        while True:  # Event Loop
            event, values = self._window.read(timeout=10)
            if event in (None, 'Exit'):  # exits event loop
                break

            if event == 'updateValues':
                self.updateValues(values)

            if event == 'randomizeValues':
                self.randomizeValues()
                self.updateDisplayedValues()

            if event == 'updateValues' or event == 'randomizeValues':
                self._window['action'].update("Generate data")
                self._window['action'].update(visible=True)
                self._window['runall'].update(visible=True)
                self._state = GuiState.GenerateData

            if event == 'runall':
                self.runAllModels()

            if event == 'action':
                if self._state == GuiState.GenerateData:
                    self._window['action'].update("Generating...")
                    self.generateData()
                    self._window['action'].update("Train Model")
                    self._state = GuiState.TrainModel
                elif self._state == GuiState.TrainModel:
                    self._window['action'].update("Training...")
                    self.trainModel()
                    self._window['action'].update("Test")
                    self._state = GuiState.Test
                elif self._state == GuiState.Test:
                    self._window['action'].update("Testing...")
                    self._window['score'].update(self.testModel())
                    self._window['action'].update("Show output")
                    self._state = GuiState.Output
                else:
                    self.showOutput()

        self._window.close()

    def createLayout(self):
        return [
            [
                sg.Text('Maximum coefficient:', size=(20, 1)),
                sg.Input(size=(20, 1), key='maxCoeff'),
                sg.Text(size=(20, 1)),
                sg.Text('Maximum exponent:', size=(20, 1)),
                sg.Input(size=(20, 1), key='maxExp'),
                sg.Text(size=(30, 1)),
                sg.Button(size=(20, 1), button_color=("white", "black"),
                          button_text="Update", key='updateValues'),
                sg.Button(size=(20, 1), button_color=("white", "black"),
                          button_text="Randomize", key='randomizeValues')
            ],
            [
                sg.Text('Domain minimum value:', size=(20, 1)),
                sg.Input(size=(20, 1), key='minValue'),
                sg.Text(size=(20, 1)),
                sg.Text('Domain maximum value:', size=(20, 1)),
                sg.Input(size=(20, 1), key='maxValue'),
                sg.Text(size=(20, 1)),
                sg.Text('Number of samples:', size=(20, 1)),
                sg.Input(size=(20, 1), key='numberOfSamples')
            ],
            [
                sg.Text('Regression model:', size=(20, 1))
            ] + [
                sg.Radio(model.name, "radio_group1", key="model" + str(model.value)) for model in ModelType
            ],
            [
                sg.Text('Number of variables:', size=(20, 1)),
                sg.Input(size=(20, 1), key='numberOfVariables'),
            ],
            self.createParameterLayout('coeff', 'Coefficients:'),
            self.createParameterLayout('exp', 'Exponents:'),
            [
                sg.Text('Resulting function:', size=(20, 2)),
                sg.Text('', key='resultingFunction', size=(120, 2))
            ],
            [
                sg.Text('Regression score:', size=(20, 2)),
                sg.Text('', key='score', size=(120, 2))
            ],
            [
                sg.Text(size=(77, 1)),
                sg.Text(size=(77, 1)),
                sg.Col([
                    [
                        sg.Button(size=(20, 1), button_color=(
                            "white", "black"), button_text="Auto run all models", key='runall', visible=False),
                        sg.Button(size=(20, 1), button_color=(
                            "white", "black"), button_text="Start", key='action', visible=False)
                    ]
                ])
            ]
        ]

    # Workaround for tkinker bug that missaligns invisible items
    @staticmethod
    def inputColumn(*args, **kwargs):
        return sg.Col([[sg.Input(*args, **kwargs)]], pad=(0, 0))

    def createParameterLayout(self, parameterName, title):
        arr = [self.inputColumn(size=(7, 1), key=f'{parameterName}{x}', visible=False)
               for x in range(self._store.maxNumberOfVariables)]
        arr.insert(0, sg.Text(title, size=(20, 1),
                              key=parameterName, visible=True))

        return arr

    def updateValues(self, values):
        try:
            temp = int(values['numberOfVariables'])
            if (temp != self._store.numberOfVariables):
                self._store.numberOfVariables = temp

                if (self._store.numberOfVariables > self._store.maxNumberOfVariables):
                    self._store.numberOfVariables = self._store.maxNumberOfVariables

                elif self._store.numberOfVariables < self._store.minNumberOfVariables:
                    self._store.numberOfVariables = self._store.minNumberOfVariables

        except:
            self._store.numberOfVariables = self._store.minNumberOfVariables
        finally:
            self.updateParameterValues('coeff', values)
            self.updateParameterValues('exp', values)
            self.updateDisplayedValues()

        try:
            self._store.maxCoeff = float(values['maxCoeff'])
        except:
            self._window['maxCoeff'].update(self._store.maxCoeff)

        try:
            self._store.maxExp = float(values['maxExp'])
        except:
            self._window['maxExp'].update(self._store.maxExp)

        try:
            self._store.minValue = int(values['minValue'])
        except:
            self._window['minValue'].update(self._store.minValue)

        try:
            self._store.maxValue = int(values['maxValue'])
        except:
            self._window['maxValue'].update(self._store.maxValue)

        try:
            self._store.numberOfSamples = int(values['numberOfSamples'])
        except:
            self._window['numberOfSamples'].update(self._store.numberOfSamples)

        for model in self._models:
            if values[model["key"]]:
                self._selectedModel = model["value"]

    def updateDisplayedModel(self, value):
        for model in self._models:
            if model["value"] == value:
                self._window[model["key"]].update(True)
            else:
                self._window[model["key"]].update(False)

    def updateDisplayedValues(self):
        self._window['numberOfVariables'].update(self._store.numberOfVariables)
        self.updateParameterVisibility('coeff')
        self.updateParameterVisibility('exp')

        self.updateDisplayedParameterValues('exp')
        self.updateDisplayedParameterValues('coeff')
        self.updateResultingFunction()

    def updateDisplayedParameterValues(self, parameterName):
        for x in range(self._store.maxNumberOfVariables):
            self._window[f'{parameterName}{x}'].update(
                self._store.parametersArr[x][parameterName])

    def updateParameterVisibility(self, parameterName):
        for x in range(self._store.numberOfVariables):
            self._window[f'{parameterName}{x}'].update(visible=True)

        for x in range(self._store.numberOfVariables, self._store.maxNumberOfVariables):
            self._window[f'{parameterName}{x}'].update(visible=False)

    def updateParameterValues(self, parameterName, values):
        for x in range(self._store.maxNumberOfVariables):
            try:
                self._store.parametersArr[x][parameterName] = int(
                    values[f'{parameterName}{x}'])
            except ValueError:
                try:
                    self._store.parametersArr[x][parameterName] = float(
                        values[f'{parameterName}{x}'])
                except:
                    self._window[f'{parameterName}{x}'].update(1)

    def resultingFunction(self):
        resultingFunction = ''
        for x in range(self._store.numberOfVariables):
            coeff = self._store.parametersArr[x]['coeff']
            if coeff > 0 and x > 0:
                resultingFunction += ' + '
            resultingFunction += f'{coeff}X{self._subscriptMap[f"{x}"]}^'

            exp = self._store.parametersArr[x]['exp']
            if exp < 0:
                resultingFunction += '-'

            resultingFunction += f'{exp}'
        self._store.resultingFunction = resultingFunction

    def updateResultingFunction(self):
        self.resultingFunction()
        self._window['resultingFunction'].update(self._store.resultingFunction)

    def randomizeValues(self):
        self._store.numberOfVariables = RandomHelper.randomInt(
            self._store.minNumberOfVariables, self._store.maxNumberOfVariables)
        for x in range(self._store.numberOfVariables):
            self._store.parametersArr[x]['coeff'] = RandomHelper.randomFloat(
                self._store.maxCoeff)
            self._store.parametersArr[x]['exp'] = RandomHelper.randomFloat(
                self._store.maxExp)

    def generateData(self):
        DatasetHelper.generateDataset(self._store)
        self._store.dataSet = Dataset(
            self._store.label, self._store.dataFrame)
        self._store.scaler = Scaler(
            ScalerType.StandardScaler, self._store.dataSet.getFeaturesData())

    def trainModel(self, model: ModelType = None):
        X = self._store.scaler.transform(self._store.dataSet.getFeaturesData())
        y = self._store.dataSet.getLabelData()
        if model == None:
            self._store.model = Model(self._selectedModel, X, y)
        else:
            self._store.model = Model(model, X, y)

    def testModel(self):
        X = self._store.scaler.transform(self._store.dataSet.getFeaturesData())
        y = self._store.dataSet.getLabelData()

        return round(self._store.model.evaluate(X, y), 2)

    def showOutput(self, show=True):
        PlotterHelper.plotFormula(
            self._store, self._store.model.getAlgorithmUsed(), show)

    def runAllModels(self):
        self.generateData()
        scores = {}
        figures = []
        for model in self._models:
            self.trainModel(model['value'])
            scores[self._store.model.getAlgorithmUsed()] = self.testModel()
            figures.append(self.showOutput(False))

        figures.append(PlotterHelper.plotEvaluations(list(map(itemgetter(0), scores.items())),
                                                     list(
                                                         map(itemgetter(1), scores.items())),
                                                     'All scores'))
        self._window['score'].update(' '.join(str(e) for e in scores.values()))
        print(figures)
        # for figure in figures:
        # figure.show()
        PlotterHelper.show()
