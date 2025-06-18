import matplotlib.pyplot as plt


class Graphics:
    @staticmethod
    def generate_probabilities_chart(probabilities: dict[int:int], image_id: str):
        levels = sorted(probabilities.keys())
        probabilities = [probabilities[level] for level in levels]

        plt.figure(figsize=(8, 5))
        plt.bar(levels, probabilities, color='skyblue', edgecolor='black')

        plt.xlabel('Número de clientes en cola')
        plt.ylabel('Probabilidad')
        plt.title('Distribución de Probabilidad de Clientes en Cola')

        if len(levels) > 20:
            step = max(1, len(levels) // 20)
            plt.xticks(levels[::step])
        else:
            plt.xticks(levels)

        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.savefig(f"./images/mm1-{image_id}.png")
        plt.close()

