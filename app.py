from flask import Flask, request, jsonify
import mlflow.sklearn
import pandas as pd
import os
from dotenv import load_dotenv

app = Flask(__name__)


URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:8081")
MODEL_NAME = "DEM"
model = None
mlflow.set_tracking_uri(URI)

def load_model():
  try:
    model_uri = f"model:/{MODEL_NAME}/latest"
    client = mlflow.tracking.MlflowClient()
    latest_version = client.get_latest_versions(MODEL_NAME)

    if not latest_version:
      print("Model not found")
      return None
    model = mlflow.sklearn.load_model(model_uri)
    return model
  except Exception as e:
    print(f"[Error] - loading on the model: {e}")
    return None
  


@app.route("/health", methods=["GET"])
def health():
  return jsonify({
    "status": "healthy",
    "model_loaded": model is not None
  })

@app.route("/predict", methods=["POST"])
def predict():
  global model
  if model is None:
    print("Model not loaded, attempting to reload...")
    model = load_model()

  if model is None:
    return jsonify({
      "Error": "Model not loaded, please ensure MLflow is running and the model is registered"
    })
  
  try:
    data = request.get_json()
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return jsonify({
      "prediction": prediction.tolist()
    })
  except Exception as e:
    return jsonify({
      "error": str(e)
    }), 400
  
if __name__ == "__main__":
  print("start the server", flush=True)
  model = load_model()
  app.run(host="0.0.0.0", port=5001)