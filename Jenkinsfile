pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'  // The name of the virtual environment folder
        CHROME_DRIVER = 'C:\\Users\\Prajakta\\Downloads\\chromedriver\\chromedriver-win64\\chromedriver.exe'  // Adjust path for ChromeDriver
        PYTHON_PATH = '"C:\\Program Files\\Python313\\python.exe"'  // Full path to Python
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github-token', url: 'https://github.com/Prajakta713/Smart-Waste-Sorter.git', branch: 'main'
            }
        }

        stage('Verify Python Installation') {
            steps {
                script {
                    bat "%PYTHON_PATH% --version"
                }
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    bat '''
                    if not exist %VENV_DIR%\\Scripts\\activate (
                        %PYTHON_PATH% -m venv %VENV_DIR%
                    )
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat && pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Start Flask App') {
            steps {
                script {
                    // Start the Flask app in the background (adjust the command if necessary)
                    bat '''
                    start python app.py  // Adjust this to your app's startup script
                    '''
                }
            }
        }

        stage('Wait for Flask to Start') {
            steps {
                script {
                    // Wait for Flask to start by introducing a short delay
                    bat 'timeout /t 10'  // Wait for 10 seconds before running tests
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat && pytest test_selenium.py --maxfail=1 --disable-warnings -q
                    '''
                }
            }
        }
    }

    post {
        always {
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
