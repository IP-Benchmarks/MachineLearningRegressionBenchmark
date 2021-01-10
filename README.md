# MachineLearningRegressionBenchmark

This repository holds benchmark for regression algorithms using an agent with learning capabilities on a non linear function affected by noise.

# Introduction

This application is developed using python 3.7+. To be able to run it you need to install the packages from [requirements.txt](https://github.com/IulianOctavianPreda/MachineLearningRegressionBenchmark/blob/master/requirements.txt). You can install them using:

`$ pip install -r requirements.txt`

These packages are:

-   Pandas
-   Numpy
-   Matplotlib
-   Scikit-learn
-   Joblib
-   Pysimplegui
-   Pyinstaller

# Architecture

The code is split in multiple packages:

-   main - the main entry point in the application
-   src - package containing the main classes used by the application
-   enums - contains the enums used by the gui, scaler and models
-   helpers - is the package that contains static methods useful for the classes found in the src package

# Application flow

-   The number of variables, their exponent and their coefficient can be user defined, otherwise are picked randomly
-   The function is composed based on the selected values
-   The application then will pick random values for each variable. This will be the dataset. It can be loaded from a CSV too filling in the parameters automatically.
-   Using the dataset we create the test sets in a ratio of 20-80 and then the data will be scaled using the Scaler
-   Then a Model is selected and trained.
