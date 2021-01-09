class Store:
    maxNumberOfVariables = 20
    minNumberOfVariables = 1
    numberOfVariables = None
    maxCoeff = 500
    maxExp = 10
    maxValue = 50
    minValue = 0
    parametersArr = [{'exp': 1, 'coeff': 1}
                     for _ in range(maxNumberOfVariables)]
