pipeline {
   agent any
   environment {
       registry_heatmap = "hub.iview.vn/heatmapservice_goview_staging"
       GOCACHE = "/tmp"
   }
   stages {

       stage('Publish Frontend') {
           environment {
               registryCredential = 'dockerhub'
           }

           steps{
               script {
                   def appimage = docker.build("${registry_heatmap}:${BUILD_NUMBER}")
                   docker.withRegistry( 'https://hub.iview.vn', registryCredential ) {
                       appimage.push()
                       appimage.push('latest')
                   }
               }
           }
       }

       stage ('Deploy') {
           steps {
               script{
                   def registry_heatmap_build = registry_heatmap + ":$BUILD_NUMBER"
                   sh "ansible-playbook  playbook.yaml --extra-vars \"image=${registry_heatmap_build}\""
               }
           }
       }
    }
   
}