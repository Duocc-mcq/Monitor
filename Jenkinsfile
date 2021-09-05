pipeline {
  environment {
    registry = "hub.cxview.ai/people-gateway-lab"
    registryCredential = 'dockerhub'
    dockerImage = '' 
  }
  agent any
  stages {
    stage('Cloning Git') {
      steps {
        script {
          def Git_Tag = "${params.Git_Tag}"
          def Git_Branch = "${params.Git_Branch}"
          git 'https://github.com/Duocc-mcq/Monitor.git' --extra-var Git_Tag=${Git_Tag} --extra-var Git_Branch=${Git_Branch}
        }
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
    stage('pass env') {
      steps {
        script {
          dir("${env.WORKSPACE}"){
            sh 'echo "TAG=$BUILD_NUMBER" > .env && scp .env jenkins@192.168.30.127:/home/jenkins/people-counting-heatmap-service'
          }
        }
      }
    }        
    stage('SSH serve_deploy') {
      steps {
        sshagent(['ssh-remote']) {
          sh 'ssh -o StrictHostKeyChecking=no -l jenkins 192.168.30.127 "cd /home/jenkins/people-counting-heatmap-service && docker-compose up -d"'
        }
      }
    }            
  }
  post {
    success {
      sh "curl -s -X POST https://api.telegram.org/bot1779154197:AAH7evUsAgpF8TsXcuWuoHODkWttOovpseg/sendMessage -d chat_id=-549042452 -d text=build_people_counting_done"
    }
    failure {
      sh "curl -s -X POST https://api.telegram.org/bot1779154197:AAH7evUsAgpF8TsXcuWuoHODkWttOovpseg/sendMessage -d chat_id=-549042452 -d text=build_peopele_counting_failure"
    }
  }
}
