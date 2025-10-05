pipeline {
    agent any

    environment {
        NEXUS_REGISTRY = '10.0.0.224:8082'
        NEXUS_CREDENTIAL_ID = 'nexus_credentials'
        IMAGE_NAME = 'flask-demo'
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

        stage('Verify in Nexus') {
            steps {
                script {
                    echo "Image should now be visible in Nexus at:"
                    echo "http://localhost:8081 → Browse → docker-private → ${IMAGE_NAME}"
                }
            }
        }

        stage('Deploy to Staging Server') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'staging-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    script {
                        echo "Deploying to staging server..."
                        sh """
                            ssh -o StrictHostKeyChecking=no -i \$SSH_KEY \$SSH_USER@10.0.0.225 '
                                docker pull ${NEXUS_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                                docker stop ${IMAGE_NAME} || true
                                docker rm ${IMAGE_NAME} || true
                                docker run -d --name ${IMAGE_NAME} -p 80:5000 ${NEXUS_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                            '
                        """
                        echo "Container deployed on staging"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! Check Nexus to verify image."
        }
        failure {
            echo "Pipeline failed. Check console output above for errors."
        }
    }
}