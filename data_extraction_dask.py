import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport
from IPython.display import IFrame
from scipy import stats
import scipy
import statsmodels.api as sm
import matplotlib  # Matplotlib se verá en los recursos de la Unidad 4.
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook
import dask.dataframe as dd


# prof = ProfileReport(data_nids_filter, minimal=True) # Complete report about data and characteristics
# prof.to_file(output_file='data_nids_filter.html') # Save report

data_nids_filter_v1 = dd.read_csv(r'NF-UQ-NIDS.csv')
data_nids_filter_v2 = dd.read_csv(r'NF-UQ-NIDS-v2.csv')

benigns= ["Benign"]
attacks = ["Brute Force"]

data_nids_filter_v1_bf = pd.DataFrame(data_nids_filter_v1[data_nids_filter_v1["Attack"].isin(attacks)])
data_nids_filter_v2_bf = pd.DataFrame(data_nids_filter_v2[data_nids_filter_v2["Attack"].isin(attacks)])

data_nids_filter_v1_bn = pd.DataFrame(data_nids_filter_v1[data_nids_filter_v1["Attack"].isin(benigns)].sample(frac=0.03, random_state=1))
data_nids_filter_v2_bn = pd.DataFrame(data_nids_filter_v2[data_nids_filter_v2["Attack"].isin(benigns)].sample(frac=0.015, random_state=1))

data_nids_filter_v2_bf.to_csv("NF-UQ-NIDS-v2_clean_bf.xlsx")
data_nids_filter_v2_bn.to_csv("NF-UQ-NIDS-v2_clean_bf.xlsx")
