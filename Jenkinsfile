pipeline {
    agent any

    environment {
        NEXUS_REGISTRY = 'localhost:8082'
        NEXUS_CREDENTIAL_ID = 'nexus-credentials'
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
                    ),
                    usernamePassword(
                        credentialsId: 'nexus-credentials',
                        usernameVariable: 'NEXUS_CREDS_USR',
                        passwordVariable: 'NEXUS_CREDS_PSW'
                    )
                ]) {
                    script {
                        echo "Deploying to staging server..."
                        sh """
                            ssh -o StrictHostKeyChecking=no -i \$SSH_KEY \$SSH_USER@10.0.0.225 '
                                echo "\$NEXUS_CREDS_PSW" | docker login 10.0.0.224:8082 -u \$NEXUS_CREDS_USR --password-stdin
                                docker pull 10.0.0.224:8082/flask-demo:${BUILD_NUMBER}
                                docker stop flask-demo || true
                                docker rm flask-demo || true
                                docker run -d --name flask-demo -p 80:5000 10.0.0.224:8082/flask-demo:${BUILD_NUMBER}
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
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}