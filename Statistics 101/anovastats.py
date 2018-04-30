import  pandas as pd
import  scipy.stats as ss
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Anova:

    def __init__(self, df, type = 1, sets = 1):
        self.df = df
        self.col = df.shape[1]
        self.row = df.shape[0]
        self.type = type
        self.sets = sets
        #self.set_names = self.df.index.unique()
        self.replicant_no = self.split_sets()[0].shape[0]
        if sets > 1:
            self.replicant_df = self.replicant_means()
            self.N = self.replicant_df.shape[0] * self.replicant_df.shape[1]
            self.df_SSC = self.replicant_df.shape[1] - 1
            self.df_SSB = self.replicant_df.shape[0] - 1
            self.df_within = (self.replicant_no - 1) * self.replicant_df.shape[0] * self.replicant_df.shape[1]
            self.df_SST = self.df_SSB + self.df_SSC + self.df_SSB*self.df_SSC + self.df_within
        else:
            self.N = self.col * self.row
            self.df_SSC = self.col - 1
            self.df_SSB = self.row - 1
            self.df_SST = self.N - 1
        # SSE SSE Two-Way
        if self.type == 1:
            self.df_SSE = self.N - self.col
        elif (self.type == 2) & (self.sets == 1):
            self.df_SSE = (self.col - 1) * (self.row - 1)
        else:
            self.df_SSE = (self.replicant_df.shape[0] - 1) * (self.replicant_df.shape[1] - 1)


    def split_sets(self):
        sets_array = []
        set_names = self.df.index.unique()
        for set_name in set_names:
            sets_array.append(self.df[self.df.index == set_name])
        return sets_array

    def replicant_means(self):
        sets_array = self.split_sets()
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

    def MSC(self):
        MSC = self.SSC() / self.df_SSC
        return MSC

    def MSB(self):
        MSB = self.SSB() / self.df_SSB
        return MSB


    def MSE(self):
        MSE = (self.SSE() / self.df_SSE)
        return MSE

    def MS_interaction(self):
        MS_interaction = self.SS_interaction() / self.df_SSE
        return  MS_interaction

    def MS_within(self):
        MS_within = self.SSE_within() / self.df_within
        return MS_within

    def F(self):
        if self.type == 1:
            F_stat = (self.MSC() / self.MSE())
        elif (self.type == 2) & (self.sets > 1):
            F_stat = []
            F_stat.append(self.MSC() / self.MS_within())
            F_stat.append(self.MSB() / self.MS_within())
            F_stat.append(self.MS_interaction() / self.MS_within())
        else:
            F_stat = []
            F_stat.append(self.MSC() / self.MSE())
            F_stat.append(self.MSB() / self.MSE())
        return F_stat

    def p_val(self, alpha):
        if self.type == 1:
            p_val = ss.f.sf(self.F(), self.df_SSC, self.df_SSE)
        elif (self.type == 2) & (self.sets > 1):
            p_val = []
            p_val.append(ss.f.sf(self.F()[0], self.df_SSC, self.df_within))
            p_val.append(ss.f.sf(self.F()[1], self.df_SSB, self.df_within))
            p_val.append(ss.f.sf(self.F()[2], self.df_SSE, self.df_within))
        else:
            p_val = []
            p_val.append(ss.f.sf(self.F()[0], self.df_SSC, self.df_SSE))
            p_val.append(ss.f.sf(self.F()[1], self.df_SSB, self.df_SSE))
        return p_val

    def f_crit(self, alpha):
        if self.type == 1:
            f_crit = ss.f.isf(alpha, self.df_SSC, self.df_SSE)
        elif (self.type == 2) & (self.sets > 1):
            f_crit = []
            f_crit.append(ss.f.isf(alpha, self.df_SSC, self.df_within))
            f_crit.append(ss.f.isf(alpha, self.df_SSB, self.df_within))
            f_crit.append(ss.f.isf(alpha, self.df_SSE, self.df_within))
        else:
            f_crit = []
            f_crit.append(ss.f.isf(alpha, self.df_SSC, self.df_SSE))
            f_crit.append(ss.f.isf(alpha, self.df_SSB, self.df_SSE))
        return f_crit

    def anova_oneway(self, alpha):
        anova_df = pd.DataFrame(
            {'Source Var': ['Between (SSC)', 'Within (SSE)', 'Total (SST)'],
             'df': [self.df_SSC, self.df_SSE, self.df_SST],
             'SS': [self.SSC(), self.SSE(), self.SST()],
             'MS': [self.MSC(), self.MSE(), '-'],
             'F': [self.F(), '-', '-'],
             'P-value': [self.p_val(alpha), '-', '-'],
             'F-crit': [self.f_crit(alpha), '-', '-']})
        return anova_df[['Source Var', 'df', 'SS', 'MS', 'F', 'P-value', 'F-crit']]

    def anova_twoway(self, alpha):
        if self.sets == 1:
            anova_df = pd.DataFrame(
                    {'Source of Variation': ['Rows', 'Columns', 'Error', 'Total'],
                    'df': [self.df_SSB, self.df_SSC, self.df_SSE, self.df_SST],
                    'SS': [self.SSB(), self.SSC(), self.SSE(), '-'],
                    'MS': [self.MSB(), self.MSC(), self.MSE(), '-'],
                    'F': [self.F()[1], self.F()[0], '-', '-'],
                    'P-value': [self.p_val(alpha)[1], self.p_val(alpha)[0], '-', '-'],
                    'F-crit': [self.f_crit(alpha)[1], self.f_crit(alpha)[0], '-', '-']})
            return anova_df[['Source of Variation', 'SS', 'df', 'MS','F','P-value', 'F-crit']]
        else:
            anova_df = pd.DataFrame(
                {'Source of Variation': ['Rows', 'Columns', 'Row * Column', 'Error', '-', 'Total'],
                 'df': [self.df_SSB, self.df_SSC, self.df_SSB*self.df_SSC, self.df_within, '-', self.df_SST],
                 'SS': [self.SSB(), self.SSC(), self.SS_interaction(), self.SSE_within(), '-', self.SST()],
                 'MS': [self.MSB(), self.MSC(), self.MS_interaction(), self.MS_within(), '-', '-'],
                 'F': [self.F()[1], self.F()[0], self.F()[2], '-', '-', '-'],
                 'P-value': [self.p_val(alpha)[1], self.p_val(alpha)[0], self.p_val(alpha)[2], '-', '-', '-'],
                 'F-crit': [self.f_crit(alpha)[1], self.f_crit(alpha)[0], self.f_crit(alpha)[2], '-', '-', '-']})
            return anova_df[['Source of Variation', 'SS', 'df', 'MS', 'F', 'P-value', 'F-crit']]

    def marginal_means(self):
        indexes = self.df.index.unique()
        if self.sets > 1:
            r_df = self.replicant_df.copy()
            r_df = r_df.set_index(indexes)
            r_df.columns = self.df.columns
            r_df = r_df.reset_index().melt(id_vars='index',value_vars=r_df.columns)
            sns.factorplot(data = r_df, x ='variable', y = 'value', hue='index')
            plt.title("Estimated Marginal Means")
            plt.ylabel("Estimated Marginal Means")
            plt.show()
        else:
            r_df = self.df.reset_index().copy()
            r_df = r_df.groupby('index').mean()
            r_df = r_df.reset_index().melt(id_vars='index', value_vars=r_df.columns)
            sns.factorplot(data=r_df, x='variable', y='value', hue='index')
            plt.title("Estimated Marginal Means")
            plt.ylabel("Estimated Marginal Means")
            plt.show()
        return r_df