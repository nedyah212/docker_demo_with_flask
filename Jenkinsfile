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

        stage('Push to Staging Server') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'staging-credentials',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    )
                ]) {
                    script {
                        echo "Logging into staging server..."
                        sh """
                            docker login -u $USERNAME -p $PASSWORD staging.server.com
                            docker tag ${NEXUS_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} staging.server.com/${IMAGE_NAME}:${BUILD_NUMBER}
                            docker push staging.server.com/${IMAGE_NAME}:${BUILD_NUMBER}
                        """
                        echo "✓✓✓✓ Image pushed to staging server"
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