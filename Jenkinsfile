pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'  // Virtual environment folder
        CHROME_DRIVER = 'C:\\Users\\Prajakta\\Downloads\\chromedriver\\chromedriver-win64\\chromedriver.exe'
        PYTHON_PATH = 'C:\\Program Files\\Python313\\python.exe'
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

        stage('Create Virtual Environment') {
            steps {
                script {
                    bat '''
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pip install --upgrade pip
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pip install --no-cache-dir -r requirements.txt
                    pip install --no-cache-dir torch torchvision torchaudio
                    '''
                }
            }
        }

        stage('Start Flask App') {
            steps {
                script {
                    bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    start /B python app.py
                    '''
                }
            }
        }

        stage('Wait for Flask to Start') {
            steps {
                script {
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
                    bat '''
                    if exist flask.pid (
                        for /F "tokens=*" %%i in (flask.pid) do taskkill /F /PID %%i
                        del flask.pid
                    )
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
