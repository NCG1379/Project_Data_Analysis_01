import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.preprocessing import MaxAbsScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def clean_data(df_benign_brute):
    # Las variables categóricas de interés
    v_categoricas = ["L4_DST_PORT", "PROTOCOL","Attack"]

    df_categoricas = df_benign_brute.copy(deep=True)

    df_categoricas = df_categoricas[v_categoricas]

    # Implementación del One-Hot

    unique_v_cat_port = [22, 53, 21, 3389, 443, 80, 445, 500, 67, 23, 6881, 5190, 5355, 25, 0, 8443, 8080, 8002, 139, 135, -1]

    df_categoricas.reset_index(inplace=True, drop=True)

    df_categoricas_one_hot = df_categoricas.copy(deep=True)

    for col in unique_v_cat_port:
        df_categoricas_one_hot[col] = 0
        df_categoricas_one_hot.loc[df_categoricas['L4_DST_PORT'] == col, col] = 1

    df_categoricas_one_hot

    # Obtener la tabla de frecuencia
    df_categoricas_one_hotfrq = df_categoricas_one_hot.groupby("Attack")[unique_v_cat_port].sum()

    df_categoricas_one_hotfrq

    v_continuas = ["IN_BYTES", "IN_PKTS", "OUT_BYTES", "OUT_PKTS", "FLOW_DURATION_MILLISECONDS", "DURATION_IN", "DURATION_OUT", "TCP_WIN_MAX_IN", "TCP_WIN_MAX_OUT"]

    df_continuas = df_benign_brute.copy(deep=True)
    df_continuas = df_continuas[v_continuas]
    df_continuas

    transformer = MaxAbsScaler().fit(df_continuas)

    df_continuas_transformed = pd.DataFrame(transformer.transform(df_continuas), columns=[col for col in df_continuas.columns])
    df_continuas_transformed

    # ---INGRESE SU CÓDIGO---
    df_benign_brute_one_hot = df_continuas_transformed.join(df_categoricas_one_hot, how='left')
    df_benign_brute_one_hot.reset_index(inplace=True, drop=True)
    df_benign_brute_one_hot.loc[df_benign_brute_one_hot["Attack"] == "Benign", "Attack"] = 0
    df_benign_brute_one_hot.loc[df_benign_brute_one_hot["Attack"] == "Brute Force", "Attack"] = 1
    df_benign_brute_one_hot.columns.to_list()
    df_benign_brute_one_hot.value_counts()

    del df_benign_brute_one_hot[-1]

    del df_benign_brute_one_hot[139]

    df_benign_brute_one_hot.drop(["L4_DST_PORT", "PROTOCOL"], axis=1)

    rename_cols = {22: "PORT_22", 3389: "PORT_3389", 21: "PORT_21", 53: "PORT_53", 80: "PORT_80", 443: "PORT_443"}    

    df_benign_brute_one_hot = df_continuas_transformed.join(df_categoricas_one_hot, how='left')
    df_benign_brute_one_hot.reset_index(inplace=True, drop=True)
    df_benign_brute_one_hot.loc[df_benign_brute_one_hot["Attack"] == "Benign", "Attack"] = 0
    df_benign_brute_one_hot.loc[df_benign_brute_one_hot["Attack"] == "Brute Force", "Attack"] = 1
    df_benign_brute_one_hot.columns.to_list()
    df_benign_brute_one_hot.value_counts()

    df_benign_brute_one_hot.rename(columns=rename_cols, inplace=True)

    return df_benign_brute_one_hot

