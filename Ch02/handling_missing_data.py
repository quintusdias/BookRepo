import pandas as pd
import numpy as np

unemp = pd.read_csv('data/UNRATE.csv', parse_dates=['DATE'])
unemp = unemp.sort_values(by='DATE').set_index('DATE')

# Generate a data set where data is randomly missing
rand_unemp = unemp.sample(frac=0.9).sort_index()
rand_unemp = rand_unemp.reindex(unemp.index)

# generate a data set where data is more likely to be missing if unemployment
# is high
bias_unemp = unemp.copy()
idx = unemp.query('UNRATE > 8').sample(frac=0.5).sort_index().index
bias_unemp.UNRATE[idx] = np.NaN


