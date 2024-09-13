from flask import Flask, request, jsonify
import pandas as pd
import mlflow
import mlflow.sklearn

# Initiate Flask app
app = Flask(__name__)

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

# Route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    global pipeline
    if pipeline is None:
        return jsonify({"error": "Model not loaded"}), 400

    data = pd.DataFrame(request.json['data'])
    
    # Make predictions
    predictions = pipeline.predict(data)
    
    return jsonify({"predictions": predictions.tolist()})

# Default route to display "Hello, World"
@app.route('/')
def home():
    return "<h1>Hello, World!</h1><p>This is the main page.</p>"

# Run the API
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
