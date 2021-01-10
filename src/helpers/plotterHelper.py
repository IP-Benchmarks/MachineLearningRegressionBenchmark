from matplotlib import pyplot
from pandas.plotting import register_matplotlib_converters
from matplotlib import style
from numpy import arange, linspace, ndarray, array, unique
from scipy.interpolate import make_interp_spline, BSpline

from src.store import Store

style.use('ggplot')
register_matplotlib_converters()


class PlotterHelper:

    @staticmethod
    def show():
        pyplot.show()

    @staticmethod
    def plotEvaluations(names: list, results: list, figure: str, show: bool = False):
        f = pyplot.figure(figure)
        x = arange(len(names))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = pyplot.subplots()
        rects1 = ax.bar(x - width / 2, results, width)

        # Add some text for names, title and custom x-axis tick names, etc.
        ax.set_ylabel('Scores')
        ax.set_title('Models Scores')
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        pyplot.setp(ax.get_xticklabels(), rotation=30,
                    horizontalalignment='right')

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, -75),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', rotation=90)

        autolabel(rects1)
        fig.tight_layout()
        if show:
            pyplot.show()
        else:
            return fig

    @staticmethod
    def plotFormula(store: Store, figure: str, show: bool = False):
        features = store.features

        fig = pyplot.figure(figure, figsize=[10, 10])
        pyplot.suptitle(store.model.getAlgorithmUsed(), y=1, fontsize=18)
        pyplot.title(store.resultingFunction, wrap=True, fontsize=10)
        pyplot.xlabel('Variables - X')
        pyplot.ylabel('Results - Y')

        for feature in features:
            x = store.dataSet.getFeatureData(feature)
            y = store.dataSet.getLabelData()
            uqIdx = PlotterHelper.uniqueIndexes(x, y)
            x, y = PlotterHelper.sortRelatedLists(x[uqIdx], y[uqIdx])

            xNew = linspace(x.min(), x.max(), store.numberOfSamples)
            bSpline = make_interp_spline(x, y)
            yNew = bSpline(xNew)

            pyplot.plot(xNew, yNew, label=feature)

        pyplot.legend(loc=3)
        if show:
            pyplot.show()
        else:
            return fig

    @staticmethod
    def sortRelatedLists(list1: ndarray, list2: ndarray) -> (array, array):
        x, y = (array(t) for t in zip(*sorted(zip(list1, list2))))
        return x, y

    @staticmethod
    def uniqueIndexes(x: array, y: array):
        arr = array([*zip(y, x)])
        return unique(arr[:, 1], return_index=True)[1]
