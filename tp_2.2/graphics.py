import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from distributions.distribution import Distribution
from collections import Counter

def generate_graph(distribution: Distribution):
    rejection_method_numbers = distribution.getRejectionMethodGeneratedNumbers()
    inverse_transform_number = distribution.getInverseTransformGeneratedNumbers()
    
    if (distribution.get_dist_type() == "continuous"):
        if (len(rejection_method_numbers) > 0):
            plt.hist(rejection_method_numbers, bins=50, density=True, alpha=0.8, color='skyblue', label='Método Rechazo')
        
        if (len(inverse_transform_number) > 0):
            plt.hist(inverse_transform_number, bins=50, density=True, alpha=0.2, color='red', label='Transformada Inversa')

        x, pdf = distribution.get_expected_pdf()
        plt.plot(x, pdf, label="Distribución Esperada", color='blue')           
    
    elif (distribution.get_dist_type() == "discrete"):
        conteo = Counter(rejection_method_numbers)
        x_vals = sorted(conteo.keys())
        frec_rel = [conteo[x] / len(rejection_method_numbers) for x in x_vals]

        plt.bar(x_vals, frec_rel, width=0.6, alpha=0.8, color='skyblue', label="Método Rechazo")
        
        x, pmf = distribution.get_expected_pmf()
        plt.bar(x, pmf, width=0.6, alpha=1.0, facecolor='none', edgecolor='blue', label="Distribución Esperada")


    plt.title(distribution.get_dist_name().upper())
    plt.xlabel('x')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()
    plt.grid(True)
    plt.show()
