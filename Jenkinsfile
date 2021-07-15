pipeline {
  environment {
    registry_people = "hub.cxview.ai/people-gateway:0.1-base"
    registryCredential = "dockerhub"
    dockerImage = ''
  }
  agent any
  stages {
    stage ('cloning Git'){
      steps {
        git 'https://github.com/Duocc-mcq/Monitor.git'
      }
    }
    stage('Building image') {
      steps{
        scripts {
            dockerImage = docker.build registry + ":$BUILD_NUMBER"
            docker.withRegistry( 'https://hub.cxview.ai', registryCredential ) {
                dockerImage.push() 
                dockerImage.push('latest') 
            }
        }
      }
    }
    stage('Deploy') {
      steps{
        script {
            def image_people = registry_people + ":$BUILD_NUBER"
            sh "ansible-playbook  playbook.yaml --extra-vars \"image_people=${image_people} \""
        }
      }
    }
  }
}