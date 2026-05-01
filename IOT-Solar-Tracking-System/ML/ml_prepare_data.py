import pandas as pd

# Read the already generated ML dataset
df = pd.read_csv("ml_dataset.csv")

print("ML dataset verified successfully")
print(df.columns)
print(df.shape)
