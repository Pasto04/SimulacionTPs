import matplotlib.pyplot as plt


class Graphics:
    @staticmethod
    def generate_probabilities_chart(probabilities: dict[int:int], title: str, xlabel: str, ylabel: str):
        levels = sorted(probabilities.keys())
        probabilities = [probabilities[level] for level in levels]

        plt.figure(figsize=(8, 5))
        plt.bar(levels, probabilities, color='skyblue', edgecolor='black')

        plt.xlabel('Número de clientes en cola')
        plt.ylabel('Probabilidad')
        plt.title('Distribución de Probabilidad de Clientes en Cola')
        plt.xticks(levels)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.show()
