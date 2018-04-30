import  pandas as pd
import  scipy.stats as ss

class Anova:

    def __init__(self, df):
        self.df = df
        self.col = df.shape[1]
        self.row = df.shape[0]
        self.N = df.shape[0] * df.shape[1]
        # SSC
        self.df_SSC = self.col - 1
        # SSE
        self.df_SSE = self.N - self.col
        # SST
        self.df_SST = self.N - 1
        # SSB Two-way
        self.df_SSB = self.row - 1
        # SSE Two-Way
        self.df_SSE2 = (self.col - 1)*(self.row - 1)
        # Column/Group Mean
        self.col_means = self.df.mean()
        # Row/Block Mean
        self.row_means = self.df.mean(axis=1)
        # Overall Mean
        self.overall_means = self.col_means.mean()

    def SSC(self):
        SSC = self.col_means.var() * (self.df_SSC) * self.row
        return SSC

    def SSE(self):
        SSE = 0
        for i in range(0, self.df.shape[1]):
            ss = (self.df.iloc[:,i].var()*6)
            SSE = ss + SSE
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

    def MSE(self):
        MSE = self.SSE() / self.df_SSE
        return  MSE

    def F(self):
        F_stat = self.MSC() / self.MSE()
        return F_stat

    def one_way(self, alpha):
        df_denom = self.df_SSE
        df_numer = self.df_SSC
        f_crit_val = ss.f.isf(alpha, df_numer, df_denom)
        p_val = ss.f.sf(self.F(), self.df_SSC, self.df_SSE)
        return p_val, f_crit_val


    def anova(self, alpha):
        anova_df = pd.DataFrame(
            {'Source Var': ['Between (SSC)', 'Within (SSE)', 'Total (SST)'],
             'df': [self.df_SSC, self.df_SSE, self.df_SST],
             'SS': [self.SSC(), self.SSE(), self.SST()],
             'MS': [self.MSC(), self.MSE(), '-'],
             'F': [self.F(), '-', '-'],
             'P-value': [self.one_way(alpha)[0], '-', '-'],
             'F-crit': [self.one_way(alpha)[1], '-', '-']})
        return anova_df[['Source Var', 'df', 'SS','MS','F','P-value','F-crit']]
