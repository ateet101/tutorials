import matplotlib.pyplot
import numpy as np

class Plots:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def test(self):
    	print('hhjkk')

    def add_plots(self, lower, middle, high):
    	between = np.where(np.round(x) == middle[0])[0][313]
		between1 = np.where(np.round(x) == middle[1])[0][313]
		color1 = np.where(np.round(x) == lower[0])[0][0]
		color2 = np.where(np.round(x) == lower[1])[0][313]
		color3 = np.where(np.round(x) == high[0])[0][313]
		color4 = np.where(np.round(x) == high[1])[0][-1]
		fig, ax1 = plt.subplots(1, 1, sharex=True)
		ax1.plot(x,y)
		ax1.fill_between(x[between:between1], 0, y[between:between1])
		ax1.fill_between(x[color1:color2], 0, y[color1:color2], facecolor ='green')
		ax1.fill_between(x[color3:color4], 0, y[color3:color4], facecolor ='green')