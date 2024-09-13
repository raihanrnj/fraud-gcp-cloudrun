from fastapi import FastAPI, Request
from pydantic import BaseModel
import pandas as pd
import mlflow
import mlflow.sklearn
import uvicorn

# Initiate FastAPI app
app = FastAPI()

# Function to load the best model from MLflow
def load_best_model():
    # Define your MLflow tracking URI and experiment name (if needed)
    mlflow.set_tracking_uri("http://34.128.92.38:5000")  # Update with your MLflow server URI
    experiment_name = "model_fraud"  # Update with your experiment name

    # Get the experiment ID
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

    df = mlflow.search_runs(experiment_ids=[experiment_id])

    # Initialize variables
    best_metric = -float('inf')
    best_run = None

    # Iterate through DataFrame and find the best model by accuracy
    for index, row in df.iterrows():
        test_accuracy = row['metrics.accuracy']
        if test_accuracy > best_metric:
            best_metric = test_accuracy
            best_run = row
    if best_run is None:
        raise RuntimeError("No runs found in the specified experiment.")

    # Load the model from the best run
    model_uri = f"runs:/{best_run['run_id']}/{best_run['tags.mlflow.runName']}_pipeline_model"
    return mlflow.sklearn.load_model(model_uri)

# Load the best model when the app starts
pipeline = load_best_model()

# Define a request model using Pydantic
class DataModel(BaseModel):
    data: list

# Route for predictions
@app.post('/predict')
async def predict(request: DataModel):
    global pipeline
    if pipeline is None:
        return {"error": "Model not loaded"}

    data = pd.DataFrame(request.data)

    # Make predictions
    predictions = pipeline.predict(data)

    return {"predictions": predictions.tolist()}

# Default route to display "Hello, World"
@app.get('/')
async def home():
    return {"message": "Hello, World! This is the main page."}

# Run the app with Uvicorn's server
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
