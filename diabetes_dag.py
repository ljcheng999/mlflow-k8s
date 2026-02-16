from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
# from airflow.providers.cncf.kubernetes.operators.pod
from datetime import datetime, timedelta

default_args = {
  "owner": "airflow",
  "depends_on_past": False,
  "start_date": datetime(2024, 1, 1),
  "email_on_failure": False,
  "email_on_retry": False,
  "retries": 1,
  "retry_delay": timedelta(minutes=5)
}

dag = DAG(
  "diabetes_training_k8s",
  default_args=default_args,
  description="Train diabetes model in k8s",
  schedule=None, # Manual triger
  catchup=False,
)

train_model = KubernetesPodOperator(
  namespace="airflow",
  image="diabetes-mlops:latest",
  cmds=["python", "train_mlflow.py"],
  labels={"app": "diabetes_train"},
  name="training_pod",
  task_id="train_model_in_k8s",
  get_logs=True,
  dag=dag,
  is_delete_operator_pod=True,
  image_pull_policy="Never", # Use image from Kind cache
  env_vars={
    "MLFLOW_TRACKING_URI": "http://mlflow.mlflow.svc.cluster.local"
  },

  # arguments=["echo", "10"],
  # do_xcom_push=True,
)

