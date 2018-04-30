'''
a = [
(5-8-5+9)**2 +
(9-8-11+9)**2 +
(10-8-11+9)**2 +
(5-10-5+9)**2 +
(13-10-11+9)**2 +
(12-10-11+9)**2]
'''
import pandas as pd
import seaborn as sns
import numpy as np
import math
import matplotlib.pyplot as plt
from random import randint
import scipy.stats as ss
#from scipy.stats import norm, kurtosis, skew
import itertools as itt
sns.set(rc={'figure.figsize':(11.7,8.27)})
import plots
import importlib
from pandas_datareader import data, wb
import datetime
import apstats
#importlib.reload(plots)
#importlib.reload(apstats)

laundry_df = pd.DataFrame({'Type': ['Super']*4 + ['Best']*4,
                           'Cold': [4,5,6,5,6,6,4,4],
                           'Warm': [7,9,8,12,13,15,12,12],
                           'Hot': [10,12,11,9,12,13,10,13]})
# one  way anova
u_df = pd.DataFrame({'Year 1 Scores': [82,93,61,74,69,70,53],
                     'Year 2 Scores': [71,62,85,94,78,66,71],
                     'Year 3 Scores': [64,73,87,91,56,78,87]})

# two way anova
origSB_df = pd.DataFrame({'Sydney': [75,70,50,65,80,65],
                      'Brisbane': [75,70,55,60,65,65],
                      'Melbourne': [90,70,75,85,80,65]},
                     index = ['Shopper 1', 'Shopper 2', 'Shopper 3', 'Shopper 4', 'Shopper 5', 'Shopper 6'])

sty = ['1 feeding per day']
sty2 = ['2 feedings per day']

# two way anova
plant_df_one = pd.DataFrame({'AA': [65,70,60,60,60,55,60,50],
                         'BB': [70,65,60,70,65,60,60,50],
                         'CC': [55,65,70,55,55,60,50,50]}, index=sty*8)

# two way anova with Replication
plant_df_two = pd.DataFrame({'AA': [65,70,60,60,60,55,60,50] + [50,55,80,65,70,75,75,65],
                         'BB': [70,65,60,70,65,60,60,50] + [45,60,85,65,70,70,80,60],
                         'CC': [55,65,70,55,55,60,50,50] + [35,40,35,55,35,40,45,40]}, index= sty*8 + sty2*8)
