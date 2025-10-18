pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
    DOCKER_IMAGE = "ganeshraj24/resume-app"
    KUBECONFIG_CREDENTIAL = 'kubeconfig'
    APP_TAG = "-"
  }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Build Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh "echo  | docker login -u  --password-stdin"
          sh "docker build -t : ."
        }
      }
    }
    stage('Push Image') { steps { sh "docker push :" } }
    stage('Helm Deploy') {
      steps {
        withCredentials([file(credentialsId: env.KUBECONFIG_CREDENTIAL, variable: 'KUBECONFIG_FILE')]) {
          sh '''
            export KUBECONFIG=
            helm upgrade --install resume-app charts/resume-app \
              --set image.repository= \
              --set image.tag=
          '''
        }
      }
    }
    stage('Smoke Test') { steps { sh "kubectl get pods" } }
  }
}
