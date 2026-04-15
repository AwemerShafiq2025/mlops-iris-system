pipeline {
    agent any
    
    environment {
        MODEL_NAME = "IrisModel"
        NOTIFICATION_EMAIL = "awemershafiq1@gmail.com"
        MLFLOW_TRACKING_URI = "http://192.168.100.17:5000"
    }
    
    stages {
        stage('Identify Branch & Set Alias') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        env.PIPELINE_TYPE = "Dev Pipeline"
                        env.MODEL_ALIAS = "Challenger"
                    } else if (env.BRANCH_NAME == 'main') {
                        env.PIPELINE_TYPE = "Pre-prod Pipeline"
                        env.MODEL_ALIAS = "Challenger-pre-test"
                    } else if (env.TAG_NAME) {
                        env.PIPELINE_TYPE = "Prod Pipeline"
                        env.MODEL_ALIAS = "Champion"
                    } else {
                        env.PIPELINE_TYPE = "Other"
                        env.MODEL_ALIAS = "None"
                    }
                }
            }
        }

        stage('Data Ingest') {
            steps {
                echo "Ingesting data..."
                sh "python3 src/ingest.py" 
            }
        }

        stage('Model Train & Register') {
            steps {
                echo "Training Random Forest Classifier..."
                sh "python3 src/train.py --alias ${env.MODEL_ALIAS}"
            }
        }

        stage('Model Test') {
            steps {
                echo "Running Model Tests..."
                sh "python3 src/test.py"
            }
        }

        stage('Update Alias on Success') {
            when {
                anyOf {
                    branch 'main'
                    buildingTag()
                }
            }
            steps {
                script {
                    // Agar tag hai to 'Champion', warna 'Challenger-post-test'
                    def finalAlias = env.TAG_NAME ? "Champion" : "Challenger-post-test"
                    echo "Updating MLflow alias to ${finalAlias}"
                    sh "python3 src/update_alias.py --alias ${finalAlias}"
                }
            }
        }
    }

    post {
        success {
            script {
                mail to: "${env.NOTIFICATION_EMAIL}",
                     mimeType: 'text/html',
                     subject: "SUCCESS: ${env.PIPELINE_TYPE} Deployment - Build #${env.BUILD_NUMBER}",
                     body: """
                        <html>
                        <body style="font-family: Arial, sans-serif; padding: 20px;">
                            <h2 style="color: #28a745;">Build Successful!</h2>
                            <p>The <b>${env.PIPELINE_TYPE}</b> has finished. Model alias <b>${env.MODEL_ALIAS}</b> is set.</p>
                            <p>View Build: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                            <br>
                            <i>Automated MLOps Notification | University of Lahore</i>
                        </body>
                        </html>
                     """
            }
        }
        failure {
            script {
                mail to: "${env.NOTIFICATION_EMAIL}",
                     mimeType: 'text/html',
                     subject: "FAILURE: ${env.PIPELINE_TYPE} - Build #${env.BUILD_NUMBER}",
                     body: "Build failed. Check logs: ${env.BUILD_URL}console"
            }
        }
    }
}