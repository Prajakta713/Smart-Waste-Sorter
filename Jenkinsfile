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
                    // Start Flask app using `flask run`
                    bat '''
                    start /B python -m flask run --host=0.0.0.0 --port=5000
                    '''
                }
            }
        }

        stage('Wait for Flask to Start') {
            steps {
                script {
                    // Retry until Flask responds
                    bat '''
                    :loop
                    curl -s http://localhost:5000 > nul
                    if %ERRORLEVEL%==0 (
                        echo Flask is up and running.
                        goto done
                    )
                    echo Waiting for Flask to start...
                    timeout /t 5
                    goto loop
                    :done
                    '''
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

        stage('Stop Flask App') {
            steps {
                script {
                    // Force kill any Python processes (including Flask app)
                    bat '''
                    taskkill /F /IM python.exe
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
