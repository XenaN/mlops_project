import time

import joblib
import numpy as np
import pandas

with open("dataset.csv") as f:
    df = pandas.read_csv(f)
with open("model.clf", "rb") as f:
    model = joblib.load(f)

df = df.drop(columns=["AQI"])

ticks = 20
buff = []

for i in range(ticks):
    start = time.time()
    pred = model.predict(df)
    buff.append(time.time() - start)

print(f"Average time: {np.mean(buff) / df.shape[0]}")
print(f"Std time: {np.std(buff) / df.shape[0]}")
