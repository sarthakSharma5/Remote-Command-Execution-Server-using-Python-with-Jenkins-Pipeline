def TEST_STATUS_CODE = 0

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
            environment {
                TEST_STATUS_CODE = 0
            }

            steps{
                echo "testing codes via docker"

                sh '''
if sudo docker ps -a | grep testweb
then
  sudo docker rm -f testweb
fi
sudo docker run -dit -p 85:80 -v /root/deployAPI:/usr/local/apache/htdocs --name testweb httpd
                '''
            }

            steps {
                TEST_STATUS_CODE = sh(script: 'curl -o /dev/null -s -w "%{http_code}" -i 0.0.0.0:85', returnStdout: true).trim()
                echo "${TEST_STATUS_CODE}"
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