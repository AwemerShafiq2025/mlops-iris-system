pipeline {
    agent any
    
    environment {
        MODEL_NAME = "IrisModel"
        NOTIFICATION_EMAIL = "awemershafiq1@gmail.com"
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
                // Using single quotes for simple strings and double quotes only where needed
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
            when { branch 'main' }
            steps {
                echo "Updating alias to Challenger-post-test"
                sh "python3 src/update_alias.py --alias Challenger-post-test"
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed. Sending email..."
            mail to: "${env.NOTIFICATION_EMAIL}",
                 subject: "FAILED: ${env.PIPELINE_TYPE} - Build #${env.BUILD_NUMBER}",
                 body: "Bhai, pipeline fail ho gayi hai. Please check Jenkins logs."
        }
        success {
            echo "Pipeline completed successfully!"
        }
    }
}