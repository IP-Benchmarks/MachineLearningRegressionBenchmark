from enums.guiState import GuiState
import PySimpleGUI as sg
import base64
import os


class Gui:
    maxNumberOfVariables = 20
    numberOfVariables = 5
    parametersArr = [{'exp': 1, 'coeff': 1}
                     for _ in range(maxNumberOfVariables)]
    window = None
    state = GuiState.TrainModel

    def __init__(self):
        pass

    def start(self):
        sg.theme('DarkBlue')
        self.window = sg.Window('Regression Benchmark', self.createLayout(),
                                icon="./assets/ico.ico", finalize=True)
        self.window.read(timeout=10)
        self.window['numberOfVariables'].update(self.numberOfVariables)
        self.window['action'].update("Train Model")

        while True:  # Event Loop
            event, values = self.window.read(timeout=10)
            if event in (None, 'Exit'):  # exits event loop
                break

            self.updateValues(values)

            if event == 'action':
                if(self.state == GuiState.TrainModel):
                    # model.train()
                    self.window['action'].update("Predict")
                    self.state = GuiState.Predict
                elif(self.state == GuiState.Predict):
                    # model.predict()
                    self.window['action'].update("Show output")
                    self.state = GuiState.Output
                else:
                    # model.showOutput()
                    pass

        self.window.close()

    def createLayout(self):
        return [
            [sg.Text('Number of variables:', size=(20, 1)),
             sg.Input(size=(100, 1), key='numberOfVariables'),
             ],
            self.createParameterLayout('coeff', 'Coefficients:'),
            self.createParameterLayout('exp', 'Exponents:'),
            [sg.Text(size=(50, 1)),
             sg.Text(size=(50, 1)),
             sg.Button(size=(20, 1), button_color=("white", "black"),
                       button_text="Start",  key='action')
             ]
        ]

    def createParameterLayout(self, parameterName, title):
        arr = [sg.Input(size=(5, 1), key=f'{parameterName}{x}', visible=True)
               for x in range(self.maxNumberOfVariables)]
        arr.insert(0, sg.Text(
            title, size=(20, 1), visible=True))

        return arr

    def updateValues(self, values):
        try:
            temp = int(values['numberOfVariables'])
            if(temp != self.numberOfVariables):
                self.numberOfVariables = temp
                if(self.numberOfVariables > self.maxNumberOfVariables):
                    self.numberOfVariables = self.maxNumberOfVariables
                    self.window['numberOfVariables'].update(
                        self.numberOfVariables)
                self.updateParameterVisibility('coeff')
                self.updateParameterVisibility('exp')
        except:
            self.numberOfVariables = 1
            self.window['numberOfVariables'].update(self.numberOfVariables)

            self.updateParameterVisibility('coeff')
            self.updateParameterVisibility('exp')

        self.updateParameterValues('exp', values)
        self.updateParameterValues('coeff', values)

    def updateParameterVisibility(self, parameterName):
        for x in range(self.numberOfVariables):
            self.window[f'{parameterName}{x}'].update(visible=True)

        for x in range(self.numberOfVariables, self.maxNumberOfVariables):
            self.window[f'{parameterName}{x}'].update(visible=False)

    def updateParameterValues(self, parameterName, values):
        for x in range(self.maxNumberOfVariables):
            try:
                self.parametersArr[x][parameterName] = float(
                    values[f'{parameterName}{x}'])
            except:
                self.window[f'{parameterName}{x}'].update(1)
