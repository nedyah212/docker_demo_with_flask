pipeline {
    agent any
    
    environment {
        // Your infrastructure
        NEXUS_URL = "10.0.0.224:8081"
        IMAGE_NAME = "flask-demo" 
        
        // VM details
        STAGING_VM = "10.0.0.225"
        PROD_VM = "10.0.0.226"
        VM_USER = "nedyah"
        
        // Docker image tags
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_FULL = "${NEXUS_URL}/${IMAGE_NAME}:${IMAGE_TAG}"
        IMAGE_LATEST = "${NEXUS_URL}/${IMAGE_NAME}:latest"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_FULL}"
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_LATEST}"
                }
            }
        }
        
        stage('Push to Nexus') {
            steps {
                script {
                    echo "Pushing to Nexus..."
                    sh "docker push ${IMAGE_FULL}"
                    sh "docker push ${IMAGE_LATEST}"
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                script {
                    echo "Deploying to Staging VM (${STAGING_VM})..."
                    sh """
                        ssh ${VM_USER}@${STAGING_VM} '
                            docker pull ${IMAGE_LATEST} && \
                            docker stop ${IMAGE_NAME} || true && \
                            docker rm ${IMAGE_NAME} || true && \
                            docker run -d --name ${IMAGE_NAME} -p 5000:5000 ${IMAGE_LATEST}
                        '
                    """
                }
            }
        }
        
        stage('Test Staging') {
            steps {
                script {
                    echo "Testing Staging deployment..."
                    sleep 5  // Give container time to start
                    sh "curl -f http://${STAGING_VM}:5000 || exit 1"
                    echo "Staging deployment successful!"
                }
            }
        }
        
        stage('Deploy to Production') {
            steps {
                input message: 'Deploy to Production?', ok: 'Deploy'
                script {
                    echo "Deploying to Production VM (${PROD_VM})..."
                    sh """
                        ssh ${VM_USER}@${PROD_VM} '
                            docker pull ${IMAGE_LATEST} && \
                            docker stop ${IMAGE_NAME} || true && \
                            docker rm ${IMAGE_NAME} || true && \
                            docker run -d --name ${IMAGE_NAME} -p 5000:5000 ${IMAGE_LATEST}
                        '
                    """
                }
            }
        }
        
        stage('Verify Production') {
            steps {
                script {
                    echo "Verifying Production deployment..."
                    sleep 5
                    sh "curl -f http://${PROD_VM}:80 || exit 1"  // Test via Caddy
                    echo "Production deployment successful!"
                }
            }
        }
    }
    
    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs above."
        }
    }
}