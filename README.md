# 📝 Iris MLOps Enterprise System

This project implements an automated, end-to-end MLOps pipeline using **MLflow**, **Jenkins**, and **Python**. It automates the entire lifecycle of a Random Forest Classifier trained on the Iris dataset, from data ingestion to model promotion in a production-ready registry.

## 🚀 Key Features
* **Automated CI/CD:** Seamless model training triggered by Jenkins on every code push or tag creation.
* **Model Versioning:** Systematic tracking of model versions and parameters via MLflow.
* **Dynamic Aliasing:** Automated assignment of model aliases based on the Git branch or tag context.
* **Automated Notifications:** Real-time email alerts for pipeline success or failure.

---

## 🛠 Technical Stack
* **Language:** Python 3.x
* **Orchestration:** Jenkins (Multibranch Pipeline)
* **Model Tracking:** MLflow
* **Version Control:** Git & GitHub

---

## 📋 System Configuration

### 1. MLflow Tracking Server
Before running the pipeline, ensure the MLflow server is active:
```bash
mlflow server --host 0.0.0.0 --port 5000
Note: Update the MLFLOW_TRACKING_URI in the Jenkinsfile to point to your server's IP address.
. Jenkins Setup
Create a Multibranch Pipeline in Jenkins.

Connect your GitHub repository.

Configure necessary environment variables and SMTP credentials for email notifications.
🔄 Pipeline Workflow & Aliases
The system distinguishes between development, testing, and production environments through branch-specific logic:
Pipeline Type,Trigger Event,MLflow Alias Assigned
Dev Pipeline,Push to dev branch,@Challenger
Pre-prod Pipeline,Push to main branch,@Challenger-post-test
Prod Pipeline,"Git Tag (e.g., v1.3)",@Champion
🚦 Execution Guide
How to Promote a Model to "Champion"
When a model is deemed ready for production, push a version tag to GitHub. This triggers the production pipeline which promotes the model in the MLflow Registry:
# Create a new version tag
git tag v1.3

# Push tag to GitHub to trigger Champion promotion
git push origin v1.3
.
├── src/
│   ├── ingest.py        # Data ingestion and preprocessing
│   ├── train.py         # Training logic and MLflow registration
│   ├── test.py          # Automated model evaluation
│   └── update_alias.py  # Logic for alias promotion/assignment
├── Jenkinsfile          # Jenkins declarative pipeline definition
└── requirements.txt     # Project dependencies
