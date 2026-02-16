import mlflow, os, logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import ElasticNet
from dotenv import load_dotenv

# def eval_metrics(actual, predict) -> list[float]:
# def eval_matrice(actual, predict) -> tuple[float, float, float]:
#   rmse = mean_squared_error(actual, predict) ** 0.5
#   mae = mean_absolute_error(actual, predict)
#   r2 = r2_score(actual, predict)
#   return [rmse, mae, r2]
#   # return rmse, mae, r2

def eval_matrice(actual, predict):
  rmse = mean_squared_error(actual, predict) ** 0.5
  mae = mean_absolute_error(actual, predict)
  r2 = r2_score(actual, predict)
  return rmse, mae, r2


def get_experiment(experiment_name):
  client = mlflow.MlflowClient()
  experiment = client.get_experiment_by_name(experiment_name)
  print(f"experiment name - {experiment.name}")
  print(f"experiment id - {experiment.experiment_id}")
  print(f"experiment lifecycle_stage - {experiment.lifecycle_stage}")
  
  # client.delete_experiment(experiment_id=experiment.experiment_id)

if __name__ == "__main__":
  DATA_DIRECTORY = "data"
  FILE_NAME = "diabetes.csv"
  DATA_PATH = DATA_DIRECTORY + "/" + FILE_NAME

  load_dotenv()

  logging.basicConfig(level=logging.WARN)
  logger = logging.getLogger(__name__)

  logger.error(f"MLflow version: {mlflow.__version__}")

  mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:8081"))
  mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "Diabetes_ElasticNet_v3"))

  # get_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "Diabetes_ElasticNet_v3"))
  

  if not os.path.exists(DATA_PATH):
    from export_data import download_export_data
    download_export_data(DATA_DIRECTORY, FILE_NAME)

  try:
    # data = pd.read_csv(csv_url, sep=";")
    df = pd.read_csv(DATA_PATH)
  except Exception as e:
    logger.exception(
      "Unable to read the csv file. Error: %s", e
    )
  
  # print(df.head())

  X = df.drop("target", axis=1)
  # print("\nx is here: \n", X)
  # print(df.head())

  Y = df["target"]
  # print("\ny is here: \n", Y)

  ############################################################

  # # Split the data into training and test sets. (0.75, 0.25) split.
  # train, test = train_test_split(data)
  # # The predicted column is "quality" which is a scalar from [3, 9]
  # train_x = train.2

  train_x, test_x, train_y, test_y = train_test_split(X, Y)

  alpha = 0.5
  l1_ratio = 0.5


  with mlflow.start_run() as run:

    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=2323)
    lr.fit(train_x, train_y)

    predict = lr.predict(test_x)
    (rmse, mae, r2) = eval_matrice(test_y, predict)


    mlflow.log_param("alpha: ", alpha)
    mlflow.log_param("l1_ratio: ", l1_ratio)
    mlflow.log_param("rmse: ", rmse)
    mlflow.log_param("mae: ", mae)
    mlflow.log_param("r2: ", r2)

    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)


    mlflow.sklearn.log_model(
      sk_model = lr,
      name = "model",
      registered_model_name = "DEM3",
    )

    print(run.info.to_proto())
    print(run.data.to_dictionary())
    print(f"Done")
  

    # logger.error(f"Tracking URI: {mlflow.get_tracking_uri()}")
    # logger.error(f"Artifact URI: {mlflow.get_artifact_uri()}")












