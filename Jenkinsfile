pipeline {
  environment {
    registry = "hub.cxview.ai/people-gateway:0.1-base"
    registryCredential = 'dockerhub'
    dockerImage = ''
  }
  agent any
  stages {
    stage('Cloning Git') {
      steps {
        git 'https://github.com/Duocc-mcq/Monitor.git'
      }
    }
    stage('Building image') {
      steps{
        script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
          docker.withRegistry( 'https://hub.cxview.vn', registryCredential ) {
          dockerImage.push() 
          dockerImage.push('latest') 
          }
        }
      }
    }
    stage('Deploy Image') {
      steps{
        script {
          def image_people = registry_people + ":$BUILD_NUBER"
          sh "ansible-playbook  playbook.yaml --extra-vars \"image_people=${image_people} \""
        }
      }
    }
    stage('Remove Unused docker image') {
      steps{
        sh "docker rmi $registry:$BUILD_NUMBER"
      }
    }
  }
}