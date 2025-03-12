pipeline {
    agent any
    
    environment {
        VIRTUAL_ENV = 'venv'
        PYTHON_PATH = 'C:\\Program Files\\Python313\\python.exe'
        GIT_REPO_URL = 'https://github.com/Prajakta713/Smart-Waste-Sorter.git'
        GIT_BRANCH = 'main'
    }
    
    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout scm
            }
        }
        
        stage('Checkout Code') {
            steps {
                script {
                    echo 'Checking out the latest code'
                    git branch: env.GIT_BRANCH, url: env.GIT_REPO_URL
                }
            }
        }
        
        stage('Verify Python Installation') {
            steps {
                script {
                    echo 'Verifying Python Installation'
                    bat "${env.PYTHON_PATH} --version"
                }
            }
        }
        
        stage('Set Up Virtual Environment') {
            steps {
                script {
                    echo 'Setting up virtual environment'
                    bat """
                        if not exist venv\\Scripts\\activate (
                            ${env.PYTHON_PATH} -m venv venv
                        )
                    """
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Installing dependencies'
                    bat """
                        call venv\\Scripts\\activate.bat
                        pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Verify PyTorch Installation') {
            steps {
                script {
                    echo 'Verifying PyTorch installation'
                    bat """
                        call venv\\Scripts\\activate.bat
                        python -c "import torch; print(torch.__version__)"
                    """
                }
            }
        }

        stage('Start Flask App') {
            steps {
                script {
                    echo 'Starting Flask app'
                    bat """
                        call venv\\Scripts\\activate.bat
                        python app.py &
                    """
                }
            }
        }
        
        stage('Wait for Flask to Start') {
            steps {
                script {
                    echo 'Waiting for Flask app to start'
                    // Implement the wait logic for your app to start
                    // E.g., using a sleep or a wait condition for server readiness
                    sleep(time: 20, unit: 'SECONDS')
                }
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                script {
                    echo 'Running Selenium tests'
                    // Add the necessary logic to run your Selenium tests
                }
            }
        }

        stage('Stop Flask App') {
            steps {
                script {
                    echo 'Stopping Flask app'
                    // Add logic to stop your Flask app
                    // E.g., by killing the Python process or sending a termination signal
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
