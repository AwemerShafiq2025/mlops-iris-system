# Iris MLOps Deployment (MLflow + Jenkins + Shared Library)

This repository implements a **multi-branch Jenkins MLOps pipeline** for training, testing, registering, and deploying a **Random Forest** model on the **Iris dataset** using **MLflow Model Registry** and **MLflow deployments**.

It supports three environments with strict Git events:

- **Dev**: push to `dev` branch
- **Pre-prod**: merge/push to `main` branch
- **Prod**: push a **release tag** (e.g., `v1.0.0`) on a commit

---

## 🛠 Technical Stack

- **Language:** Python 3.x
- **CI/CD:** Jenkins Multibranch Pipeline
- **Shared CI Logic:** Jenkins Shared Library
- **Model Tracking & Registry:** MLflow
- **Model:** Random Forest Classifier
- **Dataset:** Iris dataset (classic ML dataset)

---

## ✅ Requirements (High Level)

1. Create a GitHub repository (optionally add collaborator: *sikaner*).
2. Create a Jenkins **Multibranch Pipeline**.
3. Ensure Jenkins discovers:
   - `dev` branch
   - `main` branch
   - **release tags** (e.g., `v1.0.0`)
4. Pipelines must run based on Git events:
   - push to `dev` → **Dev pipeline**
   - merge/push to `main` → **Pre-prod pipeline**
   - tag a commit (release tag) → **Prod pipeline**
5. Use MLflow for:
   - experiment logging
   - registering models to Model Registry
   - assigning/updating aliases: `Challenger`, `Challenger pre-test`, `Challenger post-test`, `Champion`
6. On failure → notify via **Email**

---

## 🔧 System Configuration

### 1) MLflow Tracking Server

Start MLflow server (example):

```bash
mlflow server --host 0.0.0.0 --port 5000
```

Set `MLFLOW_TRACKING_URI` in Jenkins (as an environment variable) or inside the Jenkinsfile.

> **Note:** If Jenkins runs in Docker / another VM, ensure networking allows Jenkins → MLflow.

### 2) Jenkins Setup (Multibranch Pipeline)

- Create a **Multibranch Pipeline** job.
- Connect it to your GitHub repo credentials.
- Enable branch discovery for:
  - `dev`
  - `main`
- Enable tag discovery for:
  - release tags (e.g., `v1.*`, `v*`, or all tags depending on your policy)
- Configure Email notification credentials/settings (SMTP) in Jenkins.
- Configure Jenkins Shared Library:
  - `Manage Jenkins → System → Global Pipeline Libraries`
  - Add the shared library name and repo.

---

## 📌 Branch / Tag Strategy

| Git Ref Type | Name / Pattern | Environment | Expected Pipeline |
|-------------|-----------------|------------|-------------------|
| Branch      | `dev`           | Dev        | Dev Pipeline      |
| Branch      | `main`          | Pre-prod   | Pre-prod Pipeline |
| Tag         | `v*` (example)  | Prod       | Prod Pipeline     |

---

## 🔄 Pipeline Workflows (As Required)

### Dev Pipeline (Triggered by push to `dev`)

**Goal:** Train + test a fresh model, deploy, and register as `Challenger`.

**Steps:**
1. **Data Ingest**
2. **Model Train**
3. **Model Deploy (MLflow)**
4. **Model Test**
5. If **Success**:
   - Save/register model in MLflow Registry
   - Assign alias: **`Challenger`**
6. If **Failed**:
   - Notify via **Email**

---

### Pre-prod Pipeline (Triggered by merge/push to `main`)

**Goal:** Validate the current best dev model and promote alias through test lifecycle.

**Steps:**
1. **Load model** from MLflow Registry using alias: **`Challenger`**
2. **Log and Register** (new version) and assign alias: **`Challenger pre-test`**
3. **Model Deploy (MLflow)**
4. **Model Test**
5. If **Success**:
   - Update alias of model to: **`Challenger post-test`**
6. If **Failed**:
   - Notify via **Email**

---

### Prod Pipeline (Triggered by release tag, e.g., `v1.0.0`)

**Goal:** Promote a fully validated model to production champion.

**Steps:**
1. **Load model** from MLflow Registry using alias: **`Challenger post-test`**
2. **Log and Register** (new version) and assign alias: **`Champion`**
3. **Model Deploy (MLflow)**

---

## 🚦 Execution Guide

### 1) Dev Deployment (Dev Pipeline)

```bash
git checkout dev
git add .
git commit -m "dev: update training"
git push origin dev
```

### 2) Pre-prod Deployment (Pre-prod Pipeline)

```bash
git checkout main
git merge dev
git push origin main
```

### 3) Prod Deployment (Prod Pipeline via Tag)

```bash
# Create release tag on the desired commit
git tag v1.0.0

# Push tag to trigger prod pipeline
git push origin v1.0.0
```

---

## 📂 Repository Structure (Recommended)

```text
.
├── src/
│   ├── ingest.py           # Data ingestion & preprocessing
│   ├── train.py            # Train model + log metrics/params
│   ├── evaluate.py         # Model testing/evaluation checks
│   ├── deploy_mlflow.py    # Deploy model using MLflow (or serve)
│   └── registry_alias.py   # MLflow Registry alias operations
├── Jenkinsfile             # Multibranch pipeline entrypoint
├── vars/                   # (Shared Library) global vars (if library lives here)
├── resources/              # (Optional) templates/configs
├── requirements.txt
└── README.md
```

---

## ✅ Alias Policy Summary

| Stage      | Alias Used / Assigned |
|------------|------------------------|
| Dev        | `Challenger`           |
| Pre-test   | `Challenger pre-test`  |
| Post-test  | `Challenger post-test` |
| Prod       | `Champion`             |

---

## 📧 Notifications

Any stage failure must trigger an email notification with:

- Pipeline name + environment (Dev / Pre-prod / Prod)
- Failing stage name (ingest/train/deploy/test/registry)
- Link to Jenkins build logs

---

## Notes / Assumptions

- “Deploy (MLflow)” can mean **MLflow serving**, a **deployment target**, or a controlled **model promotion** depending on your setup.
- Alias operations depend on MLflow Model Registry being enabled and reachable from Jenkins.
