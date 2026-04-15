import mlflow
import argparse

def update_model_alias(alias_name):
    # Connect to MLflow and update the model alias after successful testing
    client = mlflow.tracking.MlflowClient()
    model_name = "IrisModel"
    
    # Get the latest version to promote
    latest_version = client.get_latest_versions(model_name, stages=["None"])[0].version
    
    # Update alias to 'Challenger-post-test' or 'Champion'
    client.set_registered_model_alias(model_name, alias_name, latest_version)
    print(f"Model {model_name} version {latest_version} updated to Alias: {alias_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--alias", type=str, required=True)
    args = parser.parse_args()
    update_model_alias(args.alias)