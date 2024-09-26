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
import dataframe_clean as dfc

df_brute = pd.read_csv('df_brute_force_v1.csv')
df_benign = pd.read_csv('df_benign_traffic_v1.csv')

df_benign_brute = pd.concat([df_benign, df_brute])

df_info = pd.DataFrame(df_benign_brute.info())
df_info.to_csv("df info.csv")

df_benign_brute_one_hot = dfc.clean_data(df_benign_brute)

X = df_benign_brute_one_hot.iloc[:, :16].astype('int')
del X['Attack']
print(X)
y = df_benign_brute_one_hot.Attack.astype('int')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=16)

# instantiate the model (using the default parameters)
logreg = LogisticRegression(solver='lbfgs', max_iter=3000, random_state=16)

# fit the model with data
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)

print(logreg.get_params())

print(logreg.score(X_test, y_test))


df_benign_test = pd.read_csv(r'results\NF-UQ-NIDS-v2_clean_bn.csv')

df_benign_test_one_hot = dfc.clean_data(df_benign_test)

X_benign_test = df_benign_test_one_hot.iloc[:, :16].astype('int')
del X_benign_test['Attack']

y_benign_test = df_benign_test_one_hot.Attack.astype('int')

print(logreg.score(X_benign_test, y_benign_test))

y_pred_test = logreg.predict(X_benign_test)

from sklearn import metrics

cnf_matrix = metrics.confusion_matrix(y_benign_test, y_pred_test)
cnf_matrix

class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.show()

