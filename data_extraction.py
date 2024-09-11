# ---INGRESE SU CÓDIGO---
from ydata_profiling import ProfileReport

import pandas as pd
import zipfile
import random

# Requieres to add a shortcut of the shared file to "MyDrive"
file_path = '/content/drive/MyDrive/NF-UQ-NIDS-v2.zip'

brute_force = []
benign_traffic = []
headers = True
b_sample_limit = 300000
b_counter = 0


with zipfile.ZipFile(file_path, 'r') as nids:
  with nids.open('NF-UQ-NIDS-v2.csv', 'r') as nids_data:
    for line in nids_data:
      if headers:
        benign_traffic.append(str(line).replace("b'","").strip("'").split(","))
        brute_force.append(str(line).replace("b'","").strip("'").split(","))
        headers = False
      elif 'brute' in str(line).lower():
        brute_force.append(str(line).replace("b'","").strip("'").split(","))
      elif 'benign' in str(line).lower():
        if (bool(random.getrandbits(1))) & (b_counter <= b_sample_limit):
          b_counter += 1
          benign_traffic.append(str(line).replace("b'","").strip("'").split(","))


print(len(brute_force), len(benign_traffic)

# ---INGRESE SU CÓDIGO---
import pandas as pd

df_benign_traffic = pd.DataFrame(benign_traffic[1:], columns=benign_traffic[0])
df_brute_force = pd.DataFrame(brute_force[1:], columns=brute_force[0])

# Unfortunately, all data was processed as str type, to validate the best type
# and map the col to the best fit we define the following function:

def check_column_value(x):
  try:
    x_new = int(x)
    return x_new
  except ValueError:
    pass
  try:
    x_new = float(x)
    return x_new
  except ValueError:
    pass
  return x


df_brute_force = df_brute_force.map(check_column_value)
df_benign_traffic = df_benign_traffic.map(check_column_value)

# After removing attacks different from brute force, or simple "benign" traffic:
df_brute_force.to_csv('df_brute_force.csv', index=False)
df_brute_force

# Control sample or "benign" traffic:
df_benign_traffic.to_csv('df_benign_traffic.csv', index=False)
df_benign_traffic)
