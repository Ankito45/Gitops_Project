pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME   = 'ankito45'
        IMAGE_NAME           = 'flask-app'
        IMAGE_TAG            = "${BUILD_NUMBER}"
        GITHUB_CREDENTIALS   = credentials('github-credentials')
        CONFIG_REPO          = 'https://github.com/Ankito45/Gitops_Project.git'
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build \
                      -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest \
                      .
                """
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh """
                    echo \$DOCKERHUB_CREDENTIALS_PSW | docker login \
                      -u \$DOCKERHUB_CREDENTIALS_USR \
                      --password-stdin

                    docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                """
            }
        }

        stage('Update GitOps Manifests') {
            steps {
                sh """
                    git config --global user.email "jenkins@example.com"
                    git config --global user.name "Jenkins"

                    rm -rf gitops-temp
                    git clone ${CONFIG_REPO} gitops-temp
                    cd gitops-temp

                    sed -i 's|image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:.*|image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}|g' \
                      flask-k8s-config/manifests/deployment.yaml

                    git add .
                    git commit -m "ci: update image tag to ${IMAGE_TAG}" || echo "No changes"
                    git push https://${GITHUB_CREDENTIALS_USR}:${GITHUB_CREDENTIALS_PSW}@github.com/Ankito45/Gitops_Project.git master
                """
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}


