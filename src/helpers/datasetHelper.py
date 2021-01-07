from pandas import DataFrame, read_csv, set_option, reset_option


class DatasetHelper:

    @staticmethod
    def readCsv(path: str) -> DataFrame:
        """Read the csv to a pandas Dataframe"""
        return read_csv(
            path, header=0, index_col='Date', parse_dates=True)

    @staticmethod
    def saveCsv(dataset: DataFrame, path: str) -> None:
        """Save the dataset to csv"""
        dataset.to_csv(path)

    @staticmethod
    def prepareDataset(dataset: DataFrame) -> DataFrame:
        """User defined logic to prepare the dataset"""
        dataset.fillna(value=-99999, inplace=True)
        return dataset

    @staticmethod
    def printFullOutput(rows: int = 10):
        """Dataset printing options to display the full format"""
        set_option('display.max_rows', rows)
        set_option('display.max_columns', None)
        set_option('display.width', 2000)
        set_option('display.float_format', '{:20,.2f}'.format)
        set_option('display.max_colwidth', -1)

    @staticmethod
    def resetPrintingOptions():
        """Reset dataset printing options to default"""
        reset_option('display.max_rows')
        reset_option('display.max_columns')
        reset_option('display.width')
        reset_option('display.float_format')
        reset_option('display.max_colwidth')
