from matplotlib import pyplot
from pandas.plotting import register_matplotlib_converters
from matplotlib import style
from numpy import arange

style.use('ggplot')
register_matplotlib_converters()


class PlotterHelper:

    @staticmethod
    def plotEvaluations(names: list, results: list):
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
                            xytext=(0, -150),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', rotation=90)

        autolabel(rects1)
        fig.tight_layout()
        pyplot.show()

    @staticmethod
    def plot(knownValues: list, predictedValues: list, x_label: str, y_label: str, title: str = None):
        pyplot.title(title)
        pyplot.xlabel(x_label)
        pyplot.ylabel(y_label)
        pyplot.plot(knownValues, label="Varables")
        pyplot.plot(predictedValues, label="Function result")
        pyplot.legend(loc=3)
        pyplot.show()
