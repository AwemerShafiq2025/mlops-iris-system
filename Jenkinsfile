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
            when { branch 'main' }
            steps {
                echo "Updating alias to Challenger-post-test"
                sh "python3 src/update_alias.py --alias Challenger-post-test"
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
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                                <div style="background-color: #28a745; color: white; padding: 20px; text-align: center;">
                                    <h1 style="margin: 0;">Build Successful!</h1>
                                </div>
                                <div style="padding: 20px; background-color: white;">
                                    <p>Hello <b>Awe-mer</b>,</p>
                                    <p>The <b>${env.PIPELINE_TYPE}</b> has completed successfully. Your MLOps workflow has finished all stages without errors.</p>
                                    <table style="width: 100%; border-collapse: collapse;">
                                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><b>Build Number:</b></td><td style="padding: 8px; border-bottom: 1px solid #eee;">#${env.BUILD_NUMBER}</td></tr>
                                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><b>Branch:</b></td><td style="padding: 8px; border-bottom: 1px solid #eee;">${env.BRANCH_NAME}</td></tr>
                                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><b>MLflow Alias:</b></td><td style="padding: 8px; border-bottom: 1px solid #eee;">${env.MODEL_ALIAS}</td></tr>
                                    </table>
                                    <div style="text-align: center; margin-top: 30px;">
                                        <a href="${env.BUILD_URL}" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">View Jenkins Build</a>
                                    </div>
                                </div>
                                <div style="background-color: #f8f9fa; color: #777; padding: 10px; text-align: center; font-size: 12px;">
                                    Automated MLOps Notification System | University of Lahore
                                </div>
                            </div>
                        </body>
                        </html>
                     """
            }
        }
        failure {
            script {
                mail to: "${env.NOTIFICATION_EMAIL}",
                     mimeType: 'text/html',
                     subject: "CRITICAL FAILURE: ${env.PIPELINE_TYPE} - Build #${env.BUILD_NUMBER}",
                     body: """
                        <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                                <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
                                    <h1 style="margin: 0;">Pipeline Failure</h1>
                                </div>
                                <div style="padding: 20px; background-color: white;">
                                    <p>Hello <b>Awe-mer</b>,</p>
                                    <p style="color: #dc3545;"><b>Attention:</b> The build for <b>${env.PIPELINE_TYPE}</b> has failed. Please investigate the logs immediately.</p>
                                    <table style="width: 100%; border-collapse: collapse;">
                                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><b>Build Number:</b></td><td style="padding: 8px; border-bottom: 1px solid #eee;">#${env.BUILD_NUMBER}</td></tr>
                                        <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><b>Status:</b></td><td style="padding: 8px; border-bottom: 1px solid #eee; color: #dc3545;">FAILED</td></tr>
                                    </table>
                                    <div style="text-align: center; margin-top: 30px;">
                                        <a href="${env.BUILD_URL}console" style="background-color: #343a40; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Check Console Logs</a>
                                    </div>
                                </div>
                            </div>
                        </body>
                        </html>
                     """
            }
        }
    }
}