# MLflow connecting to Kubernetes cluster

## Important note: 
All the following is only for local environment

### Cluster config
This local cluster is using Kind to create (kind-config)

###### Prerequisite: 
- docker daemon need to be running
```
kind create cluster -n mlops-cluster1 --config kind-config.yaml
```

### Helm

#### Prerequisite
Add helm repo in local machine and update most update verison
```
helm repo add community-charts https://community-charts.github.io/helm-charts
helm repo update
```

#### Deployment
##### (Option 1) configure the deployment in CLI
```

helm upgrade -i mlflow community-charts/mlflow -n mlflow --create-namespace \
--set backendStore.databaseMigration=true \
--set postgresql.enable=true \
--set postgresql.auth.password='' \
--set postgresql.auth.username=mlflow \
--set postgresql.auth.database=mlflow \
--set artifactRoot.proxiedArtifactStorage=true \
--set artifactRoot.defaultArtifactRoot=mlflow-artifacts:/mlartifact \
--set extraEnvVars.MLFLOW_SERVER_ALLOWED_HOST="*" \
--set extraArgs.artifacts-destination="/tmp/mlartifacts" \
--set "extraFlags[0]=serveArtifacts"
```

##### (Option 2) configure the deployment in helm values.yaml
Modify the value in helm/mlflow.values.yaml, then
```
helm upgrade -i mlflow community-charts/mlflow -n mlflow --create-namespace -f helm/mlflow.values.yaml
```

# Initialize the project
```
uv init
uv sync                               # create a virtual environment
source .venv/bin/activate
uv add mlflow scikit-learn pandas
```


### Visit mlflow UI from local machine

```
kubectl port-forward svc/mlflow -n mlflow 8081:80
```

```
Note:
* Setting backendStore.databaseMigration=true will create a postgres for mlflow
* Please do not hard code password
* Please do not set MLFLOW_SERVER_ALLOWED_HOST in production




####################
##### FAQ
####################

### if error show the port is being used
pkill -f "kubectl port-forward svc/mlflow" || true
```