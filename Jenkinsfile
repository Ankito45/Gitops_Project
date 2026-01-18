pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = 'YOUR_DOCKERHUB_USERNAME'
        IMAGE_NAME = 'flask-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
        GITHUB_CREDENTIALS = credentials('github-credentials')
        CONFIG_REPO = 'https://github.com/Ankito45/Gitops_Project.git'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
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
                    sh """
                        git config --global user.email "jenkins@example.com"
                        git config --global user.name "Jenkins"
                        
                        rm -rf flask-k8s-config
                        git clone ${CONFIG_REPO}
                        cd flask-k8s-config
                        
                        sed -i 's|image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:.*|image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}|g' manifests/deployment.yaml
                        
                        git add manifests/deployment.yaml
                        git commit -m "Update image to ${IMAGE_TAG}"
                        git push https://${GITHUB_CREDENTIALS_USR}:${GITHUB_CREDENTIALS_PSW}@github.com/YOUR_USERNAME/flask-k8s-config.git main
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
        }
    }
}