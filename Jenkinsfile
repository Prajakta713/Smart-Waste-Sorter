pipeline {
    agent any

    environment {
        // Define the directory for the virtual environment
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout your Flask app repository from GitHub
                git 'https://github.com/Prajakta713/Smart-Waste-Sorter.git'
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    // Create virtual environment if not already created
                    bat '''
                    if not exist ${VENV_DIR}\\Scripts\\activate (
                        python -m venv ${VENV_DIR}
                    )
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Activate the virtual environment and install dependencies
                    bat '''
                    ${VENV_DIR}\\Scripts\\activate && pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run automated tests using pytest
                    bat '''
                    ${VENV_DIR}\\Scripts\\activate && pytest --maxfail=1 --disable-warnings -q
                    '''
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                // Publish test results (ensure that pytest generates a test report in XML format)
                junit '**/test-*.xml'  // Adjust the test report path if necessary
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    // Add your deployment logic here, for example:
                    echo 'Deploying to staging environment...'
                    // E.g., use `flask run` or deploy to a staging server
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace after the build to avoid junk files
            cleanWs()
        }

        success {
            echo 'Build and tests passed successfully!'
        }

        failure {
            echo 'Build or tests failed. Please check the logs.'
        }
    }
}
