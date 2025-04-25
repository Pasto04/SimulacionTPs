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
            #if len(lista[x].capital) > aux: aux = len(lista[x].capital)
        else:
            plt.plot(data, label="Capital")
        
        plt.axhline(y=expected_value, color='darkorange', linestyle='--', label='Capital inicial')
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
    def show_graphics(title: str):
        plt.suptitle(title)
        fig_manager = plt.get_current_fig_manager()
        fig_manager.resize(1366, 768)
        plt.tight_layout()
        plt.show()

