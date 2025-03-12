pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'  // The name of the virtual environment folder
        CHROME_DRIVER = 'C:\\path\\to\\chromedriver.exe'  // Adjust path for ChromeDriver
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

        stage('Run Selenium Tests') {
            steps {
                script {
                    // Run Selenium tests with pytest (ensure your test script name is correct)
                    bat '''
                    ${VENV_DIR}\\Scripts\\activate && pytest test_selenium.py --maxfail=1 --disable-warnings -q
                    '''
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                // Publish test results (make sure pytest generates XML output)
                junit '**/reports/test-results.xml'  // Update path as necessary
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    // Add your deployment logic here
                    echo 'Deploying to staging environment...'
                    // E.g., use flask run or deploy to a staging server
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace after the build
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
