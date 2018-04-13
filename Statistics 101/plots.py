import matplotlib.pyplot as plt
import numpy as np

class Plots:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def test(self):
        print(str(self.x))

    def compute(self, lower, middle, high):
        between = []
        color = []
        between.append(np.where(np.round(self.x) == middle[0])[0][313])
        between.append(np.where(np.round(self.x) == middle[1])[0][313])
        color.append(np.where(np.round(self.x) == lower[0])[0][0])
        color.append(np.where(np.round(self.x) == lower[1])[0][313])
        color.append(np.where(np.round(self.x) == high[0])[0][313])
        color.append(np.where(np.round(self.x) == high[1])[0][-1])
        return between, color

    def add_plots(self,  ax, low, middle, high, plot_title):
        color_in, color_out = self.compute(low, middle, high)
        ax.plot(self.x, self.y)
        ax.fill_between(self.x[color_in[0]:color_in[1]], 0, self.y[color_in[0]:color_in[1]])
        ax.fill_between(self.x[color_out[0]:color_out[1]], 0, self.y[color_out[0]:color_out[1]], facecolor ='green')
        ax.fill_between(self.x[color_out[2]:color_out[3]], 0, self.y[color_out[2]:color_out[3]], facecolor ='green')
        ax.set_title(plot_title)
        return ax

    def compute_two(self, lower, high):
        color = []
        color.append(np.where(np.round(self.x, 1) == lower[0])[0][0])
        color.append(np.where(np.round(self.x, 1) == lower[1])[0][30])
        color.append(np.where(np.round(self.x, 1) == high[0])[0][30])
        color.append(np.where(np.round(self.x, 1) == high[1])[0][-1])
        return color

    def add_plots_two(self,  ax, low, high, plot_title):
        color_out = self.compute_two(low, high)
        ax.plot(self.x, self.y)
        ax.fill_between(self.x, 0, self.y, facecolors="blue")
        ax.fill_between(self.x[color_out[0]:color_out[1]], 0, self.y[color_out[0]:color_out[1]], facecolor ='green')
        ax.fill_between(self.x[color_out[2]:color_out[3]], 0, self.y[color_out[2]:color_out[3]], facecolor ='green')
        ax.set_title(plot_title)
        return ax