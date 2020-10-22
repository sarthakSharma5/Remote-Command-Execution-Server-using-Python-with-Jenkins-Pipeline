def TEST_STATUS_CODE = 1

pipeline{
    agent any
    environment {
        DEV_EMAIL = 'sarthaksharma575@gmail.com'
        ADMIN_EMAIL = 'sarthaksharma575@gmail.com'
    }

    stages{
        stage("Developing"){
            steps{
                sh '''
                    echo "copy codes to workspace"
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

        stage("Testing"){       // image = apache-php-api:test
            steps{
                echo "testing codes via docker"
                sh '''
                    if sudo docker ps -a | grep deploy-test-api
                    then
                        sudo docker rm deploy-test-api
                    fi
                    sudo docker run -dit -p 85:80 -v /root/deployAPI/*.html:/var/www/html -v /root/deployAPI/*.py:/var/www/cgi-bin --name deploy-test-api sarthaksharma5/api-linux:latest
                '''
                script{
                    // if SUCCESS then TEST_STATUS_CODE = 0 | i.e., sh returns 0 iff curl returns 200
                    TEST_STATUS_CODE = sh returnStatus: true, script: 'curl -o /dev/null -s -w "%{http_code}" -i 0.0.0.0:85'
                }
                sh '''
                    sudo docker stop deploy-test-api
                    sudo docker rm deploy-test-api
                '''
            }

            post{
                always{
                    echo "Testing complete"
                }
            }
        }

        stage ('Notify Devs of FAILURE') {
            when{
                expression {
                    TEST_STATUS_CODE != 0;       // i.e., STATUS_CODE != 200 : Q/A Failed
                }
            }
            steps {
                echo "mailing developer: Issue with Code, STATUS_CODE != 200"
                sh 'exit 1'                     // force FAILURE: force exit Pipeline execution
            }
            post{
                always{
                    emailext body: '''
                        Check console output to view the results.\n\n 
                        ${CHANGES}\n 
                        --------------------------------------------------\n
                        ${BUILD_LOG, maxLines=100, escapeHtml=false}
                        ''', 
                        to: "${DEV_EMAIL}", 
                        subject: 'Build failed in Jenkins: $PROJECT_NAME - #$BUILD_NUMBER'
                }
            }
        }

        stage ('Notify Devs of SUCCESS') {
            when{
                expression {
                    TEST_STATUS_CODE == 0;
                }
            }
            steps {
                echo "mailing developer: STATUS_CODE = 200"
                sh 'exit 0'
            }
            post{
                success{
                    emailext body: '''
                        Initiating deployment ... \n\n
                        Check console output to view the results.\n\n 
                        ${CHANGES}\n 
                        --------------------------------------------------\n
                        ${BUILD_LOG, maxLines=100, escapeHtml=false}
                        \n\n
                        Building and Pushing new image to DockerHub
                        ''', 
                        to: "${DEV_EMAIL}", 
                        subject: 'Build SUCCESS in Jenkins: $PROJECT_NAME - #$BUILD_NUMBER'
                }
            }
        }

        stage("Deployment"){
            steps{
                echo "Deploying over Kubernetes Cluster"
                sh '''
                    var=$(sudo kubectl get deploy api-linux --ignore-not-found)

                    if [[ "$var" == "" ]]
                    then
                        kubectl create -f /root/deployAPI/form.yml
                        kubectl create -f /root/deployAPI/api.yml
                    else
                        kubectl apply -f /root/deployAPI/form.yml
                        kubectl apply -f /root/deployAPI/api.yml 
                    fi

                    pod=$(sudo kubectl get pods -l app=api-linux -o jsonpath="{.items[0].metadata.name}")
                    sleep 30
                    sudo kubectl cp /root/deployAPI/*.html $pod:/var/www/html
                    sudo kubectl cp /root/deployAPI/*.py $pod:/var/www/cgi-bin
                '''
            }

            post{
                success{
                    echo "Deployment launched successfully"
                }
                failure{
                    echo "Deployment launch failed"
                }
            }
        }

    post{
        success{
            echo "Pipeline executed successfully"
            echo "-- mailing Admin --"
            emailext body: '''
                        App updated successfully
                        Last update by: ${DEV_EMAIL}
                        Check console output to view the results.\n\n 
                        ${CHANGES}\n 
                        --------------------------------------------------\n
                        ${BUILD_LOG, maxLines=100, escapeHtml=false}
                        \n\n
                        Pipeline executed successfully
                        ''', 
                    to: "${ADMIN_EMAIL}", 
                    subject: 'Build SUCCESS in Jenkins: $PROJECT_NAME - #$BUILD_NUMBER'

        }
    }
}