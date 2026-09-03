import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import statsmodels.formula.api as smf
from scipy.stats import mannwhitneyu
from statsmodels.stats.outliers_influence import variance_inflation_factor
mpl.rcParams['font.size'] = 10 #have a set front size
mpl.rcParams['figure.dpi'] = 200 #display resolution

cross_verified_loc = os.path.join(os.getcwd(), 'datasets', 'wiki-database-subsample.csv')
cross_verified = pd.read_csv(cross_verified_loc)

western_countries = ['Western Europe','Northern America', 'Southern Europe', 'Northern Europe', 'Oceania Western World '] #sorting of western regions

cross_verified['isWestern'] = cross_verified['un_subregion'].isin(western_countries).astype(int) #assigning isWestern value


database = cross_verified[['isWestern', 'gender', 'bigperiod_birth', 'level2_main_occ', 'ranking_visib_5criteria']]

database2 = database.dropna() #removing missing data
 
print(f"Full database : {len(database):,} rows")
print(f"After dropna  : {len(database2):,} rows")
