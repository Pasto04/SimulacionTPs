import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


class GenerateGraphics:
    @staticmethod
    def generate_line_chart(title, subplot_number, x_axys_label, y_axys_label, data, expected_value, multiple_lists = False):
        plt.subplot(2, 2, subplot_number)
        plt.title(title)
        plt.xlabel(x_axys_label)
        plt.ylabel(y_axys_label)

        if multiple_lists:
            for aux in data:
                plt.plot(aux)
        else:
            plt.plot(data, label="Capital")
        
        if (expected_value != 0):
            plt.axhline(y=expected_value, color='darkorange', linestyle='--', label='Capital inicial')
            plt.legend()
        else:
            plt.axhline(y=expected_value, color='darkorange', linestyle='-')

        plt.legend()
        plt.plot()


    @staticmethod
    def generate_bar_chart(title, subplot_number, x_axys_label, y_axys_label, data, expected_value):
        plt.subplot(2, 2, subplot_number)
        plt.title(title)
        plt.xlabel(x_axys_label)
        plt.ylabel(y_axys_label)

        plt.bar(x = np.arange(len(data))+1, height = data)
        plt.xlim(0, len(data) + 1)

        if (expected_value):
            plt.axhline(y=expected_value, color='darkorange', linestyle='--', label='Valor esperado')
        plt.legend()
        plt.plot()


    @staticmethod
    def generate_bar_chart_from_counter(title, subplot_number, x_axys_label, y_axys_label, data, min_bet: int):
        plt.subplot(2, 2, subplot_number)
        plt.title(title)
        plt.xlabel(x_axys_label)
        plt.ylabel(y_axys_label)

        counts = Counter(data)
        numbers = list(counts.keys())
        frequencies = list(counts.values())

        plt.bar(numbers, frequencies, color='skyblue', edgecolor='black', width=min_bet*0.75)

        plt.xticks(ticks=numbers, rotation=45)
        plt.plot()


    @staticmethod
    def generate_pie_chart(title, subplot_number, data):
        plt.subplot(2, 2, subplot_number)
        plt.title(title)

        labels = list(data.keys())
        sizes = list(data.values())

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.plot()
                
        # Plot
        '''plt.pie(sizes, labels=labels, colors=colors, explode=explode, 
                autopct='%1.1f%%', shadow=True, startangle=140)


        plt.pie(data, *, explode=None, labels=["Ganadores", "Perdedores"], colors=None, 
                              autopct=None, pctdistance=0.6, shadow=False, 
                              labeldistance=1.1, startangle=0, radius=1, counterclock=True, 
                              wedgeprops=None, textprops=None, center=(0, 0), frame=False, 
                              rotatelabels=False, normalize=True, hatch=None, data=None)
        '''



    @staticmethod
    def show_graphics(title: str):
        plt.suptitle(title)
        fig_manager = plt.get_current_fig_manager()
        fig_manager.resize(1366, 768)
        plt.tight_layout()
        plt.show()

