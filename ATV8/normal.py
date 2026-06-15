import numpy as np
from matplotlib import pyplot as plt

class normal_dist:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def fdp(self, x):
        z = (x - self.mu)/self.sigma
        y = np.exp(-z**2/2)/(np.sqrt(2*np.pi)*self.sigma)
        return y

    def prob(self, a, b):
        x = np.linspace(a, b, int((b - a)*100))
        y = self.fdp(x)
        integral = np.trapezoid(y, x)
        return integral

    def FDA(self, x):
        return self.prob(0, x)

    def plot_graph(self, a, b):
        x = np.linspace(a, b, int(np.floor(b) - np.floor(a))*100)
        plt.plot(x, self.fdp(x), color='green', label=f"sigma:{self.sigma}\nmu:{self.mu}")
        
def phi(x):
    Z = normal_dist(0, 1)
    return Z.FDA(x)










