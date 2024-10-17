import pandas as pd
import zipfile
import random

# Requieres to add a shortcut of the shared file to df.valero1 to load in drive
file_path = 'NF-UQ-NIDS-v2.csv.zip'

brute_force = []
classes = ["Brute", "XSS", "Injection", "Backdoor"]
benign_traffic = []
classes_data = []
headers = True
b_sample_limit = 300000
b_counter = 0

with zipfile.ZipFile(file_path, 'r') as nids:
  with nids.open('NF-UQ-NIDS-v2.csv', 'r') as nids_data:
    for line in nids_data:
      if headers:
        benign_traffic.append(str(line).replace("b'","").strip("'").split(","))
        headers = False
      elif any(attack.lower() in str(line).lower() for attack in classes):
        classes_data.append(str(line).replace("b'","").strip("'").split(","))
      elif 'benign' in str(line).lower():
        if (bool(random.getrandbits(1))) & (b_counter <= b_sample_limit):
          b_counter += 1
          benign_traffic.append(str(line).replace("b'","").strip("'").split(","))

df_benign_traffic = pd.DataFrame(benign_traffic[1:], columns=benign_traffic[0])
df_classes_data = pd.DataFrame(classes_data[1:], columns=benign_traffic[0])

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

df_benign_traffic = df_benign_traffic.map(check_column_value)
df_classes_data = df_classes_data.map(check_column_value)

df_classes_data.to_csv('df_attacks.csv', index=False)
df_benign_traffic.to_csv('df_benign_traffic.csv', index=False)

