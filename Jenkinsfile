pipeline {
    agent any

    environment {
        PYTHON_VENV = '.venv'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo 'Cleaning workspace...'
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                echo 'Checking out code from Git...'
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/feature/rest-api-foundation']],
                          userRemoteConfigs: [[url: 'https://github.com/karthi7798keyan/Hospital-Management-System.git']]])
            }
        }

        stage('Run Django Commands') {
            steps {
                echo 'Running Django commands...'
                bat """
                call ${PYTHON_VENV}\\Scripts\\activate
                python manage.py makemigrations
                python manage.py migrate
                python manage.py test
                """
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        failure {
            echo 'Pipeline failed! Check logs for details.'
        }
    }
}
