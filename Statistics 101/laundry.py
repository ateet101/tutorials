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
print(laundry_df)

row = laundry_df.shape[0]
col = laundry_df.shape[1]
print(row)

col_means = laundry_df.mean()
row_means = laundry_df.mean(axis = 1)#importlib.reload(apstats)

laundry_df = pd.DataFrame({'Type': ['Super']*4 + ['Best']*4,
                           'Cold': [4,5,6,5,6,6,4,4],
                           'Warm': [7,9,8,12,13,15,12,12],
                           'Hot': [10,12,11,9,12,13,10,13]})
print(laundry_df)

laundry_df = laundry_df.set_index('Type')
row = laundry_df.shape[0]
col = laundry_df.shape[1]
print(row)

col_means = laundry_df.mean()
row_means = laundry_df.mean(axis = 1)

def SSC_within(df, sets):
    row = df.shape[0]
    col = df.shape[1]
    set_names = df.index.unique()
    SS_within = []
    for set_name in set_names:
        new_df = df[df.index == set_name]
        for col_num in range(0, col):
            ind_col = new_df.iloc[:,col_num]
            ind_col_mean = ind_col.mean()
            SS_within.append(((ind_col - ind_col_mean) **2).sum())
    return SS_within, new_df.shape[0]

def MS_within(df, sets):
    ss, replicants = SSC_within(df, 2)
    df_within = (replicants - 1) * sets * col
    ms = np.sum(ss) / df_within
    print(np.sum(ss), df_within)
    return ms

def ss_row(df, sets):
    row = df.shape[0]
    col = df.shape[1]
    set_names = df.index.unique()
    SS_within = []
    for set_name in set_names:
        new_df = df[df.index == set_name]