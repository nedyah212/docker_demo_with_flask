pipeline {
    agent any
    
    environment {
        // Your infrastructure
        NEXUS_REGISTRY = '10.0.0.224:8081'
        NEXUS_CREDENTIAL_ID = 'nexus_credentials'
        IMAGE_NAME = 'flask-demo'
        
        // VM details
        STAGING_VM = "10.0.0.225"
        PROD_VM = "10.0.0.226"
        VM_USER = "nedyah"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building image: ${NEXUS_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    dockerImage = docker.build("${NEXUS_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                    echo "✓ Image built successfully"
                }
            }
        }
        
        stage('Push to Nexus') {
            steps {
                script {
                    echo "Logging into registry: ${NEXUS_REGISTRY}"
                    docker.withRegistry("http://${NEXUS_REGISTRY}", NEXUS_CREDENTIAL_ID) {
                        echo "Pushing ${BUILD_NUMBER} tag..."
                        dockerImage.push("${BUILD_NUMBER}")
                        echo "✓ Pushed build number tag"
                        
                        echo "Pushing latest tag..."
                        dockerImage.push('latest')
                        echo "✓ Pushed latest tag"
                    }
                    echo "✓✓✓ All pushes completed successfully!"
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                script {
                    echo "Deploying to Staging VM (${STAGING_VM})..."
                    sh """
                        ssh ${VM_USER}@${STAGING_VM} '
                            docker pull ${NEXUS_REGISTRY}/${IMAGE_NAME}:latest && \
                            docker stop ${IMAGE_NAME} || true && \
                            docker rm ${IMAGE_NAME} || true && \
                            docker run -d --name ${IMAGE_NAME} -p 5000:5000 ${NEXUS_REGISTRY}/${IMAGE_NAME}:latest
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
                            docker pull ${NEXUS_REGISTRY}/${IMAGE_NAME}:latest && \
                            docker stop ${IMAGE_NAME} || true && \
                            docker rm ${IMAGE_NAME} || true && \
                            docker run -d --name ${IMAGE_NAME} -p 5000:5000 ${NEXUS_REGISTRY}/${IMAGE_NAME}:latest
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