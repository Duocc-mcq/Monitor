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
          docker.withRegistry( 'https://hub.cxview.ai', registryCredential ) {
            dockerImage = docker.build registry + ":$BUILD_NUMBER"
            dockerImage.push() 
            dockerImage.push('latest') 
          }
        }
      }
    }
    stage('Deploy Image') {
      steps{
        script {
          sh "docker run -itd --net=host --name people-gateway \
  		--shm-size=10.05gb \
  		-v /mnt/sda2/ExternalHardrive/edge-ai/people-counting-heatmap-service:/people-counting-heatmap-service \
  		hub.cxview.ai/people-gateway:0.1-base"
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