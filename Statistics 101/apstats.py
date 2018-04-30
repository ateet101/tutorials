import  pandas as pd
import  scipy.stats as ss

class Anova:

    def __init__(self, df, type):
        self.type = type
        self.df = df
        self.col = df.shape[1]
        self.row = df.shape[0]
        self.N = df.shape[0] * df.shape[1]
        # SSC
        self.df_SSC = self.col - 1
        # SSE SSE Two-Way
        if self.type == 1:
            self.df_SSE = self.N - self.col
        else:
            self.df_SSE = (self.col - 1)*(self.row - 1)
        # SST
        self.df_SST = self.N - 1
        # SSB Two-way
        self.df_SSB = self.row - 1
        # Column/Group Mean
        self.col_means = self.df.mean()
        # Row/Block Mean
        self.row_means = self.df.mean(axis=1)
        # Overall Mean
        self.overall_means = self.col_means.mean()

    def SSC(self):
        SSC = ((self.col_means - self.overall_means)**2).sum() * self.row
        return SSC

    def SSB(self):
        SSB = ((self.row_means - self.overall_means)**2).sum() * self.col
        return SSB

    def SSE(self):
        if self.type == 1:
            SSE = (self.SST() - self.SSC())
        else:
            SSE = (self.SST() - self.SSC() - self.SSB())
        return SSE

    '''
    def SST(self):
        SST_array = pd.Series()
        for i in range(0, self.df.shape[1]):
            SST_array = SST_array.append(self.df.iloc[:, i])
            SST = SST_array.var()
        return SST * 20
    '''

    def SST(self):
        SST_array = pd.Series()
        for i in range(0, self.df.shape[1]):
            SST_array = SST_array.append(self.df.iloc[:, i])
        SST = ((SST_array - self.overall_means) ** 2).sum()
        return SST

    def MSC(self):
        MSC = self.SSC() / self.df_SSC
        return MSC

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

    def one_way(self, alpha):
        if self.type == 1:
            df_denom = self.df_SSE
            df_numer = self.df_SSC
            f_crit_val = ss.f.isf(alpha, df_numer, df_denom)
            p_val = ss.f.sf(self.F(), self.df_SSC, self.df_SSE)
            return p_val, f_crit_val
        else:
            p_val = []
            f_crit_val = []
            f_crit_val.append(ss.f.isf(alpha, self.df_SSC, self.df_SSE))
            f_crit_val.append(ss.f.isf(alpha, self.df_SSB, self.df_SSE))
            p_val.append(ss.f.sf(self.F()[0], self.df_SSC, self.df_SSE))
            p_val.append(ss.f.sf(self.F()[1], self.df_SSB, self.df_SSE))
            return p_val, f_crit_val


    def anova_oneway(self, alpha):
        anova_df = pd.DataFrame(
            {'Source Var': ['Between (SSC)', 'Within (SSE)', 'Total (SST)'],
             'df': [self.df_SSC, self.df_SSE, self.df_SST],
             'SS': [self.SSC(), self.SSE(), self.SST()],
             'MS': [self.MSC(), self.MSE(), '-'],
             'F': [self.F(), '-', '-'],
             'P-value': [self.one_way(alpha)[0], '-', '-'],
             'F-crit': [self.one_way(alpha)[1], '-', '-']})
        return anova_df[['Source Var', 'df', 'SS', 'MS', 'F', 'P-value', 'F-crit']]

    def anova_twoway(self, alpha):
        p_val, f_crit_val = self.one_way(alpha)
        anova_df = pd.DataFrame(
            {'Source of Variation': ['Rows', 'Columns', 'Error', 'Total'],
             'df': [self.df_SSB, self.df_SSC, self.df_SSE, self.df_SST],
             'SS': [self.SSB(), self.SSC(), self.SSE(), '-'],
             'MS': [self.MSB(), self.MSC(), self.MSE(), '-'],
             'F': [self.F()[1], self.F()[0], '-', '-'],
             'P-value': [p_val[1], p_val[0], '-', '-'],
             'F-crit': [f_crit_val[1], f_crit_val[0], '-', '-']})
        return anova_df[['Source of Variation', 'SS', 'df', 'MS','F','P-value', 'F-crit']]

    def row_graph(self, ax):
        self.df.plot()










