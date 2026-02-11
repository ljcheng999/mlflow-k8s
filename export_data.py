from sklearn.datasets import load_diabetes
import os
import pandas as pd

def download_export_data(dir: str, filename: str) -> str:

  data_path = dir + "/" + filename

  diabetes_data = load_diabetes() # Scikit-Learn built-in dataset

  # Convert the dataset to a DataFrame
  diabetes_df = pd.DataFrame(data=diabetes_data.data,
                            columns=diabetes_data.feature_names)

  # Add target variable to the DataFrame
  diabetes_df['target'] = diabetes_data.target

  os.makedirs("data", exist_ok=False) # no row number after writing

  diabetes_df.to_csv(data_path, index=False)

  print(f"[INFO]: file name - {filename} is saved into {data_path}")

