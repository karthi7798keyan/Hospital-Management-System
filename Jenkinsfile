pipeline {
    agent any

    environment {
        IMAGE_NAME = "hms-backend"
        CONTAINER_NAME = "hms-backend-container"
        DOCKER_REGISTRY = ""  // Leave empty for local Docker
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/karthi7798keyan/Hospital-Management-System.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:latest")
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker run -d -p 8000:8000 --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        success {
            echo "HMS Backend Deployed Successfully!"
        }
        failure {
            echo "Something went wrong! Check the logs."
        }
    }
}
