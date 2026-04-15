import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import argparse

def train_model(alias_name):
    # 1. Load Dataset (Iris) 
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

    # 2. Start MLflow Run
    with mlflow.start_run() as run:
        # Train Random Forest 
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        # Log Model to MLflow [cite: 14]
        mlflow.sklearn.log_model(model, "iris-model", registered_model_name="IrisModel")
        
        # 3. Assign Alias (The "Pro" Task) 
        client = mlflow.tracking.MlflowClient()
        model_version = client.get_latest_versions("IrisModel", stages=["None"])[0].version
        
        # Sir ki PDF ke mutabiq alias set karna
        client.set_registered_model_alias("IrisModel", alias_name, model_version)
        print(f"Model Version {model_version} registered with Alias: {alias_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--alias", type=str, default="Challenger")
    args = parser.parse_args()
    train_model(args.alias)