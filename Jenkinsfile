pipeline {
    agent any

    environment {
        IMAGE_NAME = "hms-backend"
        CONTAINER_NAME = "hms-backend"
        PORT_MAPPING = "8080:8080"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                echo "Cleaning workspace..."
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                echo "Checking out code from Git..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Stop Existing Container') {
            steps {
                echo "Stopping and removing existing container if running..."
                sh '''
                if [ $(docker ps -q -f name=${CONTAINER_NAME}) ]; then
                    docker stop ${CONTAINER_NAME}
                    docker rm ${CONTAINER_NAME}
                fi
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Running new Docker container..."
                sh "docker run -d -p ${PORT_MAPPING} --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Pipeline failed! Check logs for details.'
        }
    }
}
