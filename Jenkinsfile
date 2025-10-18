pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
    DOCKER_IMAGE = 'ganeshraj24/resume-app'
    KUBECONFIG_CREDENTIAL = 'kubeconfig'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh 'echo $DH_PASS | docker login -u $DH_USER --password-stdin'
          sh "docker build -t ${env.DOCKER_IMAGE}:latest ."
        }
      }
    }

    stage('Push Image') {
      steps {
        sh "docker push ${env.DOCKER_IMAGE}:latest"
      }
    }

    stage('Helm Deploy') {
      steps {
        withCredentials([file(credentialsId: env.KUBECONFIG_CREDENTIAL, variable: 'KCFG')]) {
          sh '''
            export KUBECONFIG=$KCFG
            helm upgrade --install resume-app charts/resume-app \
              --set image.repository=${DOCKER_IMAGE} \
              --set image.tag=latest --wait --timeout 120s
          '''
        }
      }
    }

    stage('Smoke Test') {
      steps {
        sh 'kubectl get pods --no-headers || true'
      }
    }
  }

  post {
    success { echo "✅ Pipeline finished successfully" }
    failure { echo "❌ Pipeline failed — check logs" }
  }
}
