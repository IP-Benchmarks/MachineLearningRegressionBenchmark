from enums.guiState import GuiState
import PySimpleGUI as sg
import random


class Gui:
    _maxNumberOfVariables = 20
    _minNumberOfVariables = 1
    _numberOfVariables = None
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
        self.window.read(timeout=10)
        self.window['numberOfVariables'].update(self.numberOfVariables)
        while True:  # Event Loop
            event, values = self.window.read(timeout=10)
            if event in (None, 'Exit'):  # exits event loop
                break

            if event == 'updateValues':
                self.updateValues(values)
                self.window['action'].update("Generate data")
                self.window['action'].update(visible=True)
                self._state = GuiState.GenerateData

            if event == 'randomizeValues':
                self.randomizeValues()
                self.updateDisplayedValues()
                self.window['action'].update("Generate data")
                self.window['action'].update(visible=True)
                self._state = GuiState.GenerateData

            if event == 'action':
                if(self.state == GuiState.GenerateData):
                    self.window['action'].update("Generating...")
                    # model.generateData()
                    self.window['action'].update("Train Model")
                    self._state = GuiState.TrainModel
                elif(self.state == GuiState.TrainModel):
                    self.window['action'].update("Training...")
                    # model.train()
                    self.window['action'].update("Predict")
                    self._state = GuiState.Predict
                elif(self.state == GuiState.Predict):
                    self.window['action'].update("Predicting...")
                    # model.predict()
                    self.window['action'].update("Show output")
                    self._state = GuiState.Output
                else:
                    # model.showOutput()
                    pass

        self.window.close()

    def createLayout(self):
        return [
            [sg.Text('Number of variables:', size=(20, 1)),
             sg.Input(size=(88, 1), key='numberOfVariables'),
             sg.Button(size=(20, 1), button_color=("white", "black"),
                       button_text="Update",  key='updateValues'),
             sg.Button(size=(20, 1), button_color=("white", "black"),
                       button_text="Randomize",  key='randomizeValues')
             ],
            self.createParameterLayout('coeff', 'Coefficients:'),
            self.createParameterLayout('exp', 'Exponents:'),
            [sg.Text('Resulting function:', size=(20, 2)),
             sg.Text('', key='resultingFunction', size=(120, 2))
             ],
            [sg.Text(size=(60, 1)),
             sg.Text(size=(59, 1)),
             sg.Col([[sg.Button(size=(20, 1), button_color=(
                 "white", "black"), button_text="Start",  key='action', visible=False)]])

             ]
        ]

    # Workaround for tkinker bug that missaligns invisible items
    def inputColumn(*args, **kwargs):
        return sg.Col([[sg.Input(*args, **kwargs)]], pad=(0, 0))

    def createParameterLayout(self, parameterName, title):
        arr = [self.inputColumn(size=(5, 1), key=f'{parameterName}{x}', visible=False)
               for x in range(self._maxNumberOfVariables)]
        arr.insert(0, sg.Text(
            title, size=(20, 1), key=parameterName, visible=True))

        return arr

    def updateValues(self, values):
        try:
            temp = int(values['numberOfVariables'])
            if(temp != self.numberOfVariables):
                self._numberOfVariables = temp

                if(self.numberOfVariables > self.maxNumberOfVariables):
                    self._numberOfVariables = self._maxNumberOfVariables

                elif self.numberOfVariables < self.minNumberOfVariables:
                    self._numberOfVariables = self._minNumberOfVariables

        except:
            self._numberOfVariables = self._minNumberOfVariables
        finally:
            self.updateDisplayedValues()

    def updateDisplayedValues(self):
        self.window['numberOfVariables'].update(self.numberOfVariables)
        self.updateParameterVisibility('coeff')
        self.updateParameterVisibility('exp')

        self.updateDisplayedParameterValues('exp')
        self.updateDisplayedParameterValues('coeff')
        self.updateResultingFunction()

    def updateDisplayedParameterValues(self, parameterName):
        for x in range(self._maxNumberOfVariables):
            self.window[f'{parameterName}{x}'].update(
                self._parametersArr[x][parameterName])

    def updateParameterVisibility(self, parameterName):
        for x in range(self.numberOfVariables):
            self.window[f'{parameterName}{x}'].update(visible=True)

        for x in range(self.numberOfVariables, self._maxNumberOfVariables):
            self.window[f'{parameterName}{x}'].update(visible=False)

    def updateParameterValues(self, parameterName, values):
        for x in range(self._maxNumberOfVariables):
            try:
                self.parametersArr[x][parameterName] = int(
                    values[f'{parameterName}{x}'])
            except ValueError:
                try:
                    self.parametersArr[x][parameterName] = float(
                        values[f'{parameterName}{x}'])
                except:
                    self.window[f'{parameterName}{x}'].update(1)

    def updateResultingFunction(self):
        resultingFunction = ''
        for x in range(self.numberOfVariables):
            coeff = self._parametersArr[x]['coeff']
            if(coeff > 0 and x > 0):
                resultingFunction += ' + '
            resultingFunction += f'{coeff}X{self.subscriptMap[f"{x}"]}^'

            exp = self._parametersArr[x]['exp']
            if(exp < 0):
                resultingFunction += '-'

            resultingFunction += f'{exp}'
        self.window['resultingFunction'].update(resultingFunction)

    def randomizeValues(self):
        self._numberOfVariables = random.randint(
            self._minNumberOfVariables, self._maxNumberOfVariables)
        for x in range(self.numberOfVariables):
            self.parametersArr[x]['coeff'] = round(random.random()*500)
            self.parametersArr[x]['exp'] = round(random.random()*10)
