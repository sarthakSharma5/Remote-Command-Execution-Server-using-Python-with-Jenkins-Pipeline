pipeline{
    agent any

    stages{
        stage("Developing"){
            steps{
                echo "copy codes to workspace"
                sh '''
if sudo ls /root/ | grep deployAPI
then
  echo "dir exists, copying code"
else
  sudo mkdir /root/deployAPI
fi
sudo cp -rvf * /root/deployAPI/
                '''
            }
            post{
                success{
                    echo "codes copied to workspace"
                }
                failure{
                    echo "error in process"
                }
            }
        }

        stage("Testing"){
            steps{
                echo "testing codes via docker"
            }
            post{
                always{
                    echo "testing complete"
                }
                success{
                    echo "image created and pushed to Docker Hub"
                }
                failure{
                    echo "issue with Testing"
                }
        
            }
        }

        stage("Deployment"){
            steps{
                echo "====++++executing Deployment++++===="
            }
            post{
                always{
                    echo "====++++always++++===="
                }
                success{
                    echo "====++++Deployment executed successfully++++===="
                }
                failure{
                    echo "====++++Deployment execution failed++++===="
                }        
            }
        }
    }

    post{
        always{
            echo "========always========"
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}