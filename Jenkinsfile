pipeline {
  environment {
    registry = "hub.iview.vn/heatmapservice_goview_staging"
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
          docker.withRegistry( 'https://hub.cxview.vn', registryCredential ) {
            dockerImage.push() 
            dockerImage.push('latest') 
          }
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
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