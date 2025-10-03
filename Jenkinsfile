pipeline {
    agent any
    
    environment {
        NEXUS_REGISTRY = 'localhost:8082'
        NEXUS_CREDENTIAL_ID = 'nexus_credentials'
        IMAGE_NAME = 'flask-demo'
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${NEXUS_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Push to Nexus') {
            steps {
                script {
                    docker.withRegistry("http://${NEXUS_REGISTRY}", NEXUS_CREDENTIAL_ID) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
}
