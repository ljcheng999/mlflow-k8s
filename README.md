# MLflow connecting to Kubernetes cluster

## Important note: 
Please **DO NOT** do the following in the production environment. All the following is **ONLY** for local environment because it has some password and everywhere-allowed access.

```
├── ./app.py                                # Flask App
├── ./assets
│   ├── ./assets/breakdown.md
│   ├── ./assets/k8s-healthcheck.png
│   └── ./assets/mlflow-experiments.png
├── ./data
│   └── ./data/diabetes.csv
├── ./diabetes_dag.py
├── ./Dockerfile
├── ./export_data.py
├── ./helm
│   └── ./helm/mlflow.values.yaml
├── ./k8s
│   └── ./k8s/manifest.yaml
├── ./kind-cluster
│   └── ./kind-cluster/kind-config.yaml
├── ./LICENSE
├── ./mlflow.db
├── ./pyproject.toml
├── ./README.md
├── ./requirements.txt
├── ./train_mlflow.py
├── ./utils.py
└── ./uv.lock
```

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

uv add aiflow                         # airflow
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

### To clean up the experiments in local machine
```
mlflow gc --tracking-uri "http://localhost:8081" --backend-store-uri sqlite:///./mlflow.db --experiment-ids 2
mlflow gc --tracking-uri sqlite:///./mlflow.db --backend-store-uri sqlite:///./mlflow.db --experiment-ids 2
```

#### Load newly build docker image in the cluster locally
There are 2 ways:
**Option 1**: Let k8s pod load your docker image from docker hub registry if the docker image can be public
```
### Build docker image

DOCKER_REPO=jcheng919
DOCKER_IMG=mlflow-k8s-diabetes-datasets
DOCKER_TAG=1.0.1

docker build -t $DOCKER_IMG:$DOCKER_TAG .
docker tag $DOCKER_IMG:$DOCKER_TAG $DOCKER_REPO/$DOCKER_IMG:$DOCKER_TAG
docker push $DOCKER_REPO/$DOCKER_IMG:$DOCKER_TAG
```

**Option 2**: Load your newly build docker image from local to your local cluster
```
### Build docker image

DOCKER_REPO=jcheng919
DOCKER_IMG=mlflow-k8s-diabetes-datasets
DOCKER_TAG=1.0.1

$ docker build -t $DOCKER_IMG:$DOCKER_TAG .

NAME                  CLUSTER                AUTHINFO                                                
kind-mlops-cluster1   kind-mlops-cluster1    kind-mlops-cluster1                               

### kind command will automatically add kind as prefix,
### thus, when you try to load docker image, remove kind prefix
$ kind load docker-image $DOCKER_IMG:$DOCKER_TAG --name mlops-cluster1
```


```
## Build the pipeline
$ docker build -t diabetes-mlops:latest -f Dockerfile.mlops .
$ kind load docker-image diabetes-mlops:latest --name mlops-cluster1
```
```
kubectl rollout status deployment/diabetes-model-server --timeout=120s

kubectl port-forward svc/diabetes-model-server-svc 5002:80
(screenshot - k8s-healthcheck attached)

curl -X POST http://localhost:5002/predict \
  -H "Conten-type: application/json" \
  -d '[{ "age": 0.05, "sec": 0.05, "bmi": 0.05, "bp": 0.05, "s1": 0.05, "s2": 0.05, "s3": 0.05, "s4": 0.05, "s5": 0.05, "s6": 0.05 }]'

```