import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import argparse
import os

def train_model(alias_name):
    # MLflow Tracking URI set karein (Jenkins env se uthaye ga ya default local)
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("Iris-Deployment")

    # Load the Iris dataset
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

    # Start an MLflow run
    with mlflow.start_run() as run:
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        # Log the model
        mlflow.sklearn.log_model(model, "iris-model", registered_model_name="IrisModel")
        
        # Client initialize karein alias assign karne ke liye
        client = mlflow.tracking.MlflowClient()
        
        # Latest version fetch karein
        versions = client.get_latest_versions("IrisModel", stages=["None"])
        if versions:
            model_version = versions[0].version
            # Alias assign karein (Challenger/Champion/Challenger-pre-test)
            client.set_registered_model_alias("IrisModel", alias_name, model_version)
            print(f"Model Version {model_version} registered with Alias: {alias_name}")
        else:
            print("No model versions found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--alias", type=str, default="Challenger")
    args = parser.parse_args()
    train_model(args.alias)