#!/bin/bash

docker build -t diabetes-mlops:latest -f Dockerfile.mlops .
kind load docker-image diabetes-mlops:latest --name mlops-cluster1

kubectl create ns airflow || true

cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: airflow
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "watch", "list", "create", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: airflow
subjects:
- kind: ServiceAccount
  name: airflow-worker # Default SA for worker (or webserver in LocalExecutor)
  namespace: airflow
- kind: ServiceAccount
  name: airflow-scheduler
  namespace: airflow
- kind: ServiceAccount
  name: airflow-webserver
  namespace: airflow
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
EOF

kubectl create cm airflow-dags --from-file=diabetes_dag.py -n airflow --dry-run=client -o yaml | kubectl apply -f -
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm upgrade -i airflow apache-airflow/airflow \
  -n airflow \
  --version 1.16.0 \
  --timeout 15m \
  -f k8s/airflow-values.yaml

kubectl wait --for=condition=ready pod -l component=webserver -n airflow --timeout=180s
pkill -f "kubectl port-forward svc/airflow-webserver" || true
kubectl port-forward svc/airflow-webserver -n airflow 8080:8080 &

echo "Airflow UI at ==> http://localhost:8080 (admin/admin)"
