pipeline {
    agent {
        kubernetes {
            cloud 'kubernetes'  // This MUST match the 'Name' field in Jenkins UI
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24.0.7-dind
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""
  - name: jnlp
    image: jenkins/inbound-agent:latest
'''
        }
    }
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = 'ankito45'
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
                container('docker') { // This executes the command inside the docker sidecar
                    script {
                        echo "Building Docker image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
                        sh """
                            docker build -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} .
                            docker tag ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                container('docker') {
                    script {
                        sh """
                            echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin
                            docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                // Git commands can run in the default jnlp container
                script {
                    sh """
                        git config --global user.email "jenkins@example.com"
                        git config --global user.name "Jenkins"
                        rm -rf gitops-temp
                        git clone ${CONFIG_REPO} gitops-temp
                        cd gitops-temp
                        sed -i 's|image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:.*|image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}|g' flask-k8s-config/manifests/deployment.yaml
                        git add .
                        git commit -m "Jenkins: Update image to ${IMAGE_TAG}" || echo "No changes"
                        git push https://${GITHUB_CREDENTIALS_USR}:${GITHUB_CREDENTIALS_PSW}@github.com/Ankito45/Gitops_Project.git master
                    """
                }
            }
        }
    }
    post {
        always {
            container('docker') {
                sh 'docker logout || true'
            }
        }
    }
}