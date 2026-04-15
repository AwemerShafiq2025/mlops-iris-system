pipeline {
    agent any
    
    environment {
        // Define common variables
        MODEL_NAME = "IrisModel"
        NOTIFICATION_EMAIL = "awemershafiq1@gmail.com" // Your email from previous sessions
    }
    
    stages {
        stage('Identify Branch & Set Alias') {
            steps {
                script {
                    // Page 2: Allow dev, main and release tag [cite: 5]
                    if (env.BRANCH_NAME == 'dev') {
                        env.PIPELINE_TYPE = "Dev Pipeline"
                        env.MODEL_ALIAS = "Challenger" // As per Page 3 [cite: 20]
                    } else if (env.BRANCH_NAME == 'main') {
                        env.PIPELINE_TYPE = "Pre-prod Pipeline"
                        env.MODEL_ALIAS = "Challenger-pre-test" // As per Page 4 [cite: 24]
                    } else if (env.TAG_NAME) {
                        env.PIPELINE_TYPE = "Prod Pipeline"
                        env.MODEL_ALIAS = "Champion" // As per Page 5 [cite: 37]
                    }
                }
            }
        }

        stage('Data Ingest') {
            steps {
                echo "Ingesting data for ${env.PIPELINE_TYPE}..."
                // Logic as per Page 3 [cite: 12]
                sh "python3 src/ingest.py" 
            }
        }

        stage('Model Train & Register') {
            steps {
                echo "Training Random Forest Classifier..." [cite: 9]
                // Pass the dynamic alias to our train.py script
                sh "python3 src/train.py --alias ${env.MODEL_ALIAS}"
            }
        }

        stage('Model Test') {
            steps {
                echo "Running Model Tests..." [cite: 16, 27]
                sh "python3 src/test.py"
            }
        }

        stage('Update Alias on Success') {
            when { branch 'main' }
            steps {
                // Page 4: Update to post-test alias after success [cite: 33]
                echo "Updating alias to Challenger-post-test"
                sh "python3 src/update_alias.py --alias Challenger-post-test"
            }
        }
    }

    post {
        failure {
            // Requirement: Notify through Email on failure 
            mail to: "${env.NOTIFICATION_EMAIL}",
                 subject: "FAILED: ${env.PIPELINE_TYPE} - Build #${env.BUILD_NUMBER}",
                 body: "Bhai, pipeline fail ho gayi hai. Please check Jenkins logs for ${env.PIPELINE_TYPE}."
        }
        success {
            echo "Pipeline completed successfully for ${env.PIPELINE_TYPE}!"
        }
    }
}