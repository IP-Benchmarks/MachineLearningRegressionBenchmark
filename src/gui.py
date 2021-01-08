from enums.guiState import GuiState
from enums.modelType import ModelType
from helpers.randomHelper import RandomHelper
import PySimpleGUI as sg
import random


class Gui:
    _models = [{"key": "model" + str(x.value), "value": x}
               for x in ModelType]
    _maxNumberOfVariables = 20
    _minNumberOfVariables = 1
    _numberOfVariables = None
    _maxCoeff = 500
    _maxExp = 10
    _selectedModel = ModelType.LinearRegression
    _parametersArr = [{'exp': 1, 'coeff': 1}
                      for _ in range(_maxNumberOfVariables)]
    _window = None
    _state = GuiState.GenerateData
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
        self._window['numberOfVariables'].update(self._numberOfVariables)
        self._window['maxCoeff'].update(self._maxCoeff)
        self._window['maxExp'].update(self._maxExp)
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
                self._state = GuiState.GenerateData

            if event == 'action':
                if(self._state == GuiState.GenerateData):
                    self._window['action'].update("Generating...")
                    # model.generateData()
                    self._window['action'].update("Train Model")
                    self._state = GuiState.TrainModel
                elif(self._state == GuiState.TrainModel):
                    self._window['action'].update("Training...")
                    # model.train()
                    self._window['action'].update("Predict")
                    self._state = GuiState.Predict
                elif(self._state == GuiState.Predict):
                    self._window['action'].update("Predicting...")
                    # model.predict()
                    self._window['action'].update("Show output")
                    self._state = GuiState.Output
                else:
                    # model.showOutput()
                    pass

        self._window.close()

    def createLayout(self):
        return [
            [sg.Text('Maximum coefficient:', size=(20, 1)),
             sg.Input(size=(20, 1), key='maxCoeff'),
             sg.Text(size=(20, 1)),
             sg.Text('Maximum exponent:', size=(20, 1)),
             sg.Input(size=(20, 1), key='maxExp'),
             sg.Text(size=(30, 1)),
             sg.Button(size=(20, 1), button_color=("white", "black"),
                       button_text="Update",  key='updateValues'),
             sg.Button(size=(20, 1), button_color=("white", "black"),
                       button_text="Randomize",  key='randomizeValues')
             ],
            [sg.Text('Regression model:', size=(20, 1))]
            + [sg.Radio(model.name, "radio_group1",
                        key="model" + str(model.value)) for model in ModelType],

            [sg.Text('Number of variables:', size=(20, 1)),
             sg.Input(size=(20, 1), key='numberOfVariables'),
             ],
            self.createParameterLayout('coeff', 'Coefficients:'),
            self.createParameterLayout('exp', 'Exponents:'),
            [sg.Text('Resulting function:', size=(20, 2)),
             sg.Text('', key='resultingFunction', size=(120, 2))
             ],
            [sg.Text(size=(77, 1)),
             sg.Text(size=(77, 1)),
             sg.Col([[sg.Button(size=(20, 1), button_color=(
                 "white", "black"), button_text="Start",  key='action', visible=False)]])

             ]
        ]

    # Workaround for tkinker bug that missaligns invisible items
    def inputColumn(*args, **kwargs):
        return sg.Col([[sg.Input(*args, **kwargs)]], pad=(0, 0))

    def createParameterLayout(self, parameterName, title):
        arr = [self.inputColumn(size=(7, 1), key=f'{parameterName}{x}', visible=False)
               for x in range(self._maxNumberOfVariables)]
        arr.insert(0, sg.Text(
            title, size=(20, 1), key=parameterName, visible=True))

        return arr

    def updateValues(self, values):
        try:
            temp = int(values['numberOfVariables'])
            if(temp != self._numberOfVariables):
                self._numberOfVariables = temp

                if(self._numberOfVariables > self._maxNumberOfVariables):
                    self._numberOfVariables = self._maxNumberOfVariables

                elif self._numberOfVariables < self._minNumberOfVariables:
                    self._numberOfVariables = self._minNumberOfVariables

        except:
            self._numberOfVariables = self._minNumberOfVariables
        finally:
            self.updateDisplayedValues()

        try:
            self._maxCoeff = float(values['maxCoeff'])
        except:
            self._window['maxCoeff'].update(self._maxCoeff)
        try:
            self._maxExp = float(values['maxExp'])
        except:
            self._window['maxExp'].update(self._maxExp)

        for model in self._models:
            if values[model["key"]]:
                self._selectedModel = model["value"]

    def updateDisplayedModel(self, value):
        for model in self._models:
            if(model["value"] == value):
                self._window[model["key"]].update(True)
            else:
                self._window[model["key"]].update(False)

    def updateDisplayedValues(self):
        self._window['numberOfVariables'].update(self._numberOfVariables)
        self.updateParameterVisibility('coeff')
        self.updateParameterVisibility('exp')

        self.updateDisplayedParameterValues('exp')
        self.updateDisplayedParameterValues('coeff')
        self.updateResultingFunction()

    def updateDisplayedParameterValues(self, parameterName):
        for x in range(self._maxNumberOfVariables):
            self._window[f'{parameterName}{x}'].update(
                self._parametersArr[x][parameterName])

    def updateParameterVisibility(self, parameterName):
        for x in range(self._numberOfVariables):
            self._window[f'{parameterName}{x}'].update(visible=True)

        for x in range(self._numberOfVariables, self._maxNumberOfVariables):
            self._window[f'{parameterName}{x}'].update(visible=False)

    def updateParameterValues(self, parameterName, values):
        for x in range(self._maxNumberOfVariables):
            try:
                self._parametersArr[x][parameterName] = int(
                    values[f'{parameterName}{x}'])
            except ValueError:
                try:
                    self._parametersArr[x][parameterName] = float(
                        values[f'{parameterName}{x}'])
                except:
                    self._window[f'{parameterName}{x}'].update(1)

    def updateResultingFunction(self):
        resultingFunction = ''
        for x in range(self._numberOfVariables):
            coeff = self._parametersArr[x]['coeff']
            if(coeff > 0 and x > 0):
                resultingFunction += ' + '
            resultingFunction += f'{coeff}X{self._subscriptMap[f"{x}"]}^'

            exp = self._parametersArr[x]['exp']
            if(exp < 0):
                resultingFunction += '-'

            resultingFunction += f'{exp}'
        self._window['resultingFunction'].update(resultingFunction)

    def randomizeValues(self):
        self._numberOfVariables = RandomHelper.randomInt(
            self._minNumberOfVariables, self._maxNumberOfVariables)
        for x in range(self._numberOfVariables):
            self._parametersArr[x]['coeff'] = RandomHelper.randomFloat(
                self._maxCoeff)
            self._parametersArr[x]['exp'] = RandomHelper.randomFloat(
                self._maxExp)
