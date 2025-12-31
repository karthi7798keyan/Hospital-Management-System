pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'feature/rest-api-foundation',
                    url: 'https://github.com/karthi7798keyan/Hospital-Management-System.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t hms-backend .
                '''
            }
        }

        stage('Stop Existing Container') {
            steps {
                sh '''
                docker stop hms-backend || true
                docker rm hms-backend || true
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                docker run -d -p 8000:8000 --name hms-backend hms-backend
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Something went wrong! Check the logs.'
        }
    }
}
