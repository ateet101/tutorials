import  pandas as pd
import  scipy.stats as ss
import numpy as np
class Anova:

    def __init__(self, df, type = 1, sets = 1):
        if sets > 1:
            self.df = self.replicant_means(df)
        else:
            self.df = df
        self.col = df.shape[1]
        self.row = df.shape[0]
        self.type = type
        self.sets = sets
        self.replicant_no = self.split_sets()[0].shape[0]

    def split_sets(self, df):
        sets_array = []
        set_names = df.index.unique()
        for set_name in set_names:
            sets_array.append(df[df.index == set_name])
        return sets_array

    def replicant_means(self, df):
        sets_array = self.split_sets(df)
        ind_col_mean = []
        for sets_array in sets_array:
            for col_num in range(0, self.col):
                ind_col = sets_array.iloc[:, col_num]
                ind_col_mean.append(ind_col.mean())
        return pd.DataFrame(np.array(ind_col_mean).reshape(self.sets, self.col))

    def SSE_within(self):
        sets_array = self.split_sets()
        SS_within = []
        for sets_array in sets_array:
            for col_num in range(0, self.col):
                ind_col = sets_array.iloc[:, col_num]
                ind_col_mean = ind_col.mean()
                SS_within.append(((ind_col - ind_col_mean) ** 2).sum())
        return np.sum(SS_within)

    def SS_interaction(self):
        means_df = self.replicant_means()
        column_means = means_df.mean()
        row_means = means_df.mean(axis = 1)
        overall_mean = row_means.mean()
        ss_array = []
        for m in range(0, len(row_means)):
            ss_inter = ((means_df.iloc[m] - column_means + overall_mean - row_means[m])**2).sum()
            ss_array.append(ss_inter.sum() * self.replicant_no)
        return np.sum(ss_array)

    def SSC(self): #SS Column
        if self.sets > 1:
            df = self.replicant_means()
        else:
            self.replicant_no = 1
            df = self.df
        column_means = df.mean()
        overall_mean = column_means.mean()
        SSC = ((column_means - overall_mean)**2).sum() * df.shape[0] * self.replicant_no
        return SSC

    def SSB(self): #SS Row
        if self.sets > 1:
            df = self.replicant_means()
        else:
            self.replicant_no = 1
            df = self.df
        row_means = df.mean(axis = 1)
        overall_mean = row_means.mean()
        SSB = ((row_means - overall_mean)**2).sum() * df.shape[1] * self.replicant_no
        return SSB

    def SSE(self): #SS Error
        if self.type == 1:
            SSE = (self.SST() - self.SSC())
        else:
            SSE = (self.SST() - self.SSC() - self.SSB())
        return SSE

    def SST(self): #SS Total
        overall_means = self.df.mean().mean()
        SST_array = pd.Series()
        for i in range(0, self.df.shape[1]):
            SST_array = SST_array.append(self.df.iloc[:, i])
        SST = ((SST_array - overall_means) ** 2).sum()
        return SST

    def MSB(self):
        MSB = self.SSB() / self.df_SSB
        return MSB


    def MSE(self):
        if self.type == 1:
            MSE = (self.SSE() / self.df_SSE)
        else:
            MSE = (self.SSE() / self.df_SSE)
        return MSE

    def F(self):
        if self.type == 1:
            F_stat = (self.MSC() / self.MSE())
        else:
            F_stat = []
            F_stat.append(self.MSC() / self.MSE())
            F_stat.append(self.MSB() / self.MSE())
        return F_stat







