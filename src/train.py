import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import argparse

def train_model(alias_name):
    # Load the Iris dataset as per project requirements
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

    # Start an MLflow run to track the training process
    with mlflow.start_run() as run:
        # Initialize and train the Random Forest Classifier
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        # Log the model to the MLflow registry
        mlflow.sklearn.log_model(model, "iris-model", registered_model_name="IrisModel")
        
        # Get the latest model version to assign the alias
        client = mlflow.tracking.MlflowClient()
        model_version = client.get_latest_versions("IrisModel", stages=["None"])[0].version
        
        # Assign the specific alias (Challenger/Champion) based on the pipeline stage
        client.set_registered_model_alias("IrisModel", alias_name, model_version)
        print(f"Model Version {model_version} registered with Alias: {alias_name}")

if __name__ == "__main__":
    # Use argparse to receive the alias name from the Jenkins pipeline
    parser = argparse.ArgumentParser()
    parser.add_argument("--alias", type=str, default="Challenger")
    args = parser.parse_args()
    train_model(args.alias)