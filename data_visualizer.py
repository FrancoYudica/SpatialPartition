
import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.stats import norm



def distribution_visualizer(samples, title, color='blue'):

    # 1) Box and Whiskers plot ----------------------------------
    plt.boxplot(samples, patch_artist=True, vert=0)

    # 2) Outputs statistics -------------------------------------
    mu = np.mean(samples)
    sigma = np.std(samples)
    print(title)
    print("     Mean:", round(mu, 4))
    print("     Sigma:", round(sigma, 4))
    print("     Median:", round(np.median(samples), 4))
    print("     Variance:", round(sigma * sigma, 4))
    print("     Range:", round(np.max(samples) - np.min(samples), 4))
    print("     Max:", round(np.max(samples), 4))
    print("     Min:", round(np.min(samples), 4))
    print("     CV", round(sigma / mu, 4))
    print("     Percentile 25:", round(np.percentile(samples, 25), 4))
    print("     Percentile 75:", round(np.percentile(samples, 75), 4))

    # 3) Normal distribution plot -------------------------------
    plt.figure(figsize=(8,6))
    plt.title(title)
    plt.xlabel("Time taken", fontsize=10)
    # Calculates mean and standard derivation

    x_values = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plt.plot(x_values, norm.pdf(x_values, mu, sigma), color=color)
    plt.text(int(mu), 0, f"Mean: {round(mu, 2)}, Sigma: {round(sigma, 2)}")
    # Mean vertical line
    plt.axline((mu, 0), (mu, 0.000001), color=color)
    plt.show()


if __name__ == "__main__":

    # Displays plots of fixed samples count
    serialized_data = open("samples.json", 'r')
    data = json.load(serialized_data)
    simple_samples = sorted(data["SamplesSimple"])
    grid_samples = sorted(data["SamplesGrid"])
    quad_tree_samples = sorted(data["SamplesQuadTree"])

    distribution_visualizer(simple_samples, title="Simple normal distribution", color='red')
    distribution_visualizer(grid_samples, title="Grid normal distribution", color='blue')
    distribution_visualizer(quad_tree_samples, title="Quad tree normal distribution", color='green')
