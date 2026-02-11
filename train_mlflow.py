import mlflow, os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import ElasticNet

# def eval_metrics(actual, predict) -> list[float]:
def eval_matrice(actual, predict) -> tuple[float, float, float]:
  rmse = mean_squared_error(actual, predict) ** 0.5
  mae = mean_absolute_error(actual, predict)
  r2 = r2_score(actual, predict)
  return [rmse, mae, r2]
  # return rmse, mae, r2

if __name__ == "__main__":
  DATA_DIRECTORY = "data"
  FILE_NAME = "diabetes.csv"
  DATA_PATH = DATA_DIRECTORY + "/" + FILE_NAME

  tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:8081")
  mlflow.set_tracking_uri(tracking_uri)
  mlflow.set_experiment("Diabetes_ElasticNet_v1")

  if not os.path.exists(DATA_PATH):
    from export_data import download_export_data
    download_export_data(DATA_DIRECTORY, FILE_NAME)

  df = pd.read_csv(DATA_PATH)
  print(df.head())

  X = df.drop("target", axis=1)
  print("\nx is here: \n", x)
  print(df.head())

  Y = df["target"]
  print("\ny is here: \n", y)

  train_x, test_x, train_y, test_y = train_test_split(X, Y)

  alpha = 0.5
  l1_ratio = 0.5

  with mlflow.start_run():
    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=2323)
    lr.fit(train_x, train_y)

    predict = lr.predict(test_x)

    (rmse, mae, r2) = eval_matrice(test_y, predict)

    mlflow.log_param("alpha: ", alpha)
    mlflow.log_param("l1_ratio: ", l1_ratio)
    mlflow.log_param("rmse: ", rmse)
    mlflow.log_param("mae: ", mae)
    mlflow.log_param("r2: ", r2)

    mlflow.sklearn.load_model(
      sk_model = lr,
      artifact_path = "model",
      registered_mode_name = "DEM",
    )

    print(f"Done")