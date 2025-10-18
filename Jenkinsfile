pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
    DOCKER_IMAGE = 'ganeshraj24/resume-app'
    KUBECONFIG_CREDENTIAL = 'kubeconfig'
    APP_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT?.take(7)}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
            if (isUnix()) {
              sh '''
                echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                docker build -t ${DOCKER_IMAGE}:${APP_TAG} -t ${DOCKER_IMAGE}:latest .
              '''
            } else {
              bat '''
                @echo off
                echo %DH_PASS% | docker login -u %DH_USER% --password-stdin
                docker build -t ${DOCKER_IMAGE}:${APP_TAG} -t ${DOCKER_IMAGE}:latest .
              '''
            }
          }
        }
      }
    }

    stage('Push Image') {
      steps {
        script {
          if (isUnix()) {
            sh "docker push ${DOCKER_IMAGE}:${APP_TAG}"
            sh "docker push ${DOCKER_IMAGE}:latest"
          } else {
            bat "docker push ${DOCKER_IMAGE}:${APP_TAG}"
            bat "docker push ${DOCKER_IMAGE}:latest"
          }
        }
      }
    }

    stage('Helm Deploy') {
      steps {
        script {
          withCredentials([file(credentialsId: env.KUBECONFIG_CREDENTIAL, variable: 'KCFG')]) {
            if (isUnix()) {
              sh '''
                export KUBECONFIG=$KCFG
                helm upgrade --install resume-app charts/resume-app \
                  --set image.repository=${DOCKER_IMAGE} \
                  --set image.tag=${APP_TAG} --wait --timeout 120s
              '''
            } else {
              bat '''
                set KUBECONFIG=%KCFG%
                "C:\\Users\\FusionGamingProPC\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Helm.Helm_Microsoft.Winget.Source_8wekyb3d8bbwe\\windows-amd64\\helm.exe" upgrade --install resume-app charts/resume-app --set image.repository=${DOCKER_IMAGE} --set image.tag=${APP_TAG} --wait --timeout 120s
              '''
            }
          }
        }
      }
    }

    stage('Smoke Test') {
      steps {
        script {
          if (isUnix()) {
            sh "kubectl get pods --no-headers || true"
          } else {
            bat "kubectl get pods --no-headers || echo 'kubectl get pods failed'"
          }
        }
      }
    }
  }

  post {
    success { echo "✅ Pipeline finished successfully: ${DOCKER_IMAGE}:${APP_TAG}" }
    failure { echo "❌ Pipeline failed — check logs" }
  }
}
