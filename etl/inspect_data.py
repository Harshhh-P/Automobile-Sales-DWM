import pandas as pd

# Path to raw dataset
file_path = "data/raw/car_data.csv"

# Read dataset
df = pd.read_csv(file_path)

print("\n========== DATASET INFORMATION ==========\n")

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumns:")
for column in df.columns:
    print("-", column)

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nData types:")
print(df.dtypes)

print("\nUnique values:")
for column in df.columns:
    print(f"\n{column}: {df[column].nunique()} unique values")