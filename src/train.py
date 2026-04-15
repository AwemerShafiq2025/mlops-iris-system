import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import argparse
import os

def train_model(alias_name):
    # MLflow Tracking URI update for remote access
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://192.168.100.17:5000")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("Iris-Deployment")

    # Data loading
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        # Log and Register
        mlflow.sklearn.log_model(model, "iris-model", registered_model_name="IrisModel")
        
        client = mlflow.tracking.MlflowClient()
        versions = client.get_latest_versions("IrisModel", stages=["None"])
        
        if versions:
            model_version = versions[0].version
            client.set_registered_model_alias("IrisModel", alias_name, model_version)
            print(f"Model Version {model_version} registered with Alias: {alias_name}")
        else:
            print("Model version not found for aliasing.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--alias", type=str, default="Challenger")
    args = parser.parse_args()
    train_model(args.alias)