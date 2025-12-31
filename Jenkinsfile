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
            echo "HMS Backend Deployed Successfully!"
        }
        failure {
            echo "Something went wrong! Check the logs."
        }
    }
}
