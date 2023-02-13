import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

class InventoryChart:
    
    def __init__(self) -> None:
        self.__chart_type = ""
        self.__chart_title = ""
        self.__x = []
        self.__y = []
        self.__x_label = ""
        self.__y_label = ""
        self.__colours = ""
        self.__data = []
        self.__labels = []
        self.__direction = ""
    
    def create_bar_chart(self, chart_title, x, y, xlabel, ylabel, direction, colours):
        self.__chart_type = "bar"
        self.__chart_title = chart_title
        self.__x = x
        self.__y = y
        self.__x_label = xlabel,
        self.__y_label = ylabel
        self.__direction = direction
        self.__colours = colours
        return self.generateChart()

    def create_pie_chart(self, chart_title, data, labels, legend_title, colours):
        self.__chart_type = "pie"
        self.__chart_title = chart_title
        self.__data = data
        self.__labels = labels
        self.__colours = colours
        return self.generateChart(legend_title)
    

    def generateChart(self, legend_title=None):
        fig = Figure(constrained_layout=True, figsize=(8,5))
        axis = fig.add_subplot(1, 1, 1)

        # Line chart added for future implementation
        variationCharts = ["bar", "line"]
            
        try:
            if self.__chart_type == "bar":
                if self.__direction == "horizontal":
                    barh = axis.barh(self.__x, self.__y, color=self.__colours)
                    axis.bar_label(barh, padding=5)
                else:
                    bar = axis.bar(self.__x, self.__y, color=self.__colours)
                    axis.bar_label(bar, padding=5)
            elif self.__chart_type == "pie":
                axis.pie(self.__data, labels=self.__labels, colors=self.__colours, textprops={'fontsize': 14})
        except Exception as exec:
            print(exec)
        
        if self.__chart_type in variationCharts:
            for label in (axis.get_xticklabels() + axis.get_yticklabels()):
                label.set_fontsize(12)
                
            axis.set_xlabel(self.__x_label)
            axis.set_ylabel(self.__y_label)
            axis.set_facecolor("#FAEBD9")
        else:
            axis.legend(title=legend_title)

        fig.patch.set_facecolor("#FAEBD9")
        axis.set_title(self.__chart_title)
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return output.getvalue()

