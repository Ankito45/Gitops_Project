pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = 'ankito45'  // ← Replace with YOUR actual Docker Hub username
        IMAGE_NAME = 'flask-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        GITHUB_CREDENTIALS = credentials('github-credentials')
        CONFIG_REPO = 'https://github.com/Ankito45/Gitops_Project.git'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh """
                        docker build -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing image to Docker Hub...'
                    sh """
                        echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin
                        docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    echo 'Updating Kubernetes manifests in git repository...'
                    sh """
                        git config --global user.email "jenkins@example.com"
                        git config --global user.name "Jenkins"
                        
                        # Clone the config repo into a temporary directory
                        rm -rf gitops-temp
                        git clone ${CONFIG_REPO} gitops-temp
                        cd gitops-temp
                        
                        # Update the image in deployment.yaml
                        sed -i 's|image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:.*|image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}|g' flask-k8s-config/manifests/deployment.yaml
                        
                        # Show the changes
                        git diff flask-k8s-config/manifests/deployment.yaml
                        
                        # Commit and push
                        git add flask-k8s-config/manifests/deployment.yaml
                        git commit -m "Jenkins: Update image to ${IMAGE_TAG}" || echo "No changes to commit"
                        git push https://${GITHUB_CREDENTIALS_USR}:${GITHUB_CREDENTIALS_PSW}@github.com/Ankito45/Gitops_Project.git master
                        
                        # Cleanup
                        cd ..
                        rm -rf gitops-temp
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'docker logout || true'
        }
        success {
            echo '✅ Pipeline completed successfully!'
            echo "Image pushed: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo '❌ Pipeline failed! Check logs above.'
        }