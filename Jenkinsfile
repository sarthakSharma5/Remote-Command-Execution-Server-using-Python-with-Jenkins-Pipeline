def TEST_FORM_STATUS_CODE = 1
def TEST_API_STATUS_CODE = 1

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

        stage("Testing"){
            steps{
                echo "testing codes via docker"
                sh '''
                    if sudo docker ps -a | grep deploy-test-api
                    then
                        sudo docker rm deploy-test-api
                    fi
                    sudo docker run -dit -p 85:80 -v /root/deployAPI:/var/www/html --name test-deploy-form sarthaksharma5/webapp:latest
                    sudo docker run -dit -p 90:80 -v /root/deployAPI:/var/www/cgi-bin --name test-deploy-api sarthaksharma5/api-webcgi:latest
                    sudo docker exec test-deploy-api chmod +x /var/www/cgi-bin/cmdapi.py
                '''
                script{
                    // if SUCCESS then TEST_FORM_STATUS_CODE = 0 | i.e., sh returns 0 iff curl returns 200
                    TEST_FORM_STATUS_CODE = sh returnStatus: true, script: 'curl -o /dev/null -s -w "%{http_code}" -i 0.0.0.0:85'
                    TEST_API_STATUS_CODE = sh returnStatus: true, script: 'curl -o /dev/null -s -w "%{http_code}" -i 0.0.0.0:90/cgi-bin/cmdapi.py?cmd=date'
                }
                sh '''
                    sudo docker stop test-deploy-api
                    sudo docker stop test-deploy-form
                    sudo docker rm test-deploy-form
                    sudo docker rm test-deploy-api
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
                    TEST_FORM_STATUS_CODE != 0 || TEST_API_STATUS_CODE != 0;     // i.e., STATUS_CODE != 200 : Q/A Failed
                }
            }
            steps {
                echo "mailing developer: Issue with Code, STATUS_CODE != 200"
                sh 'exit 1'                     // force FAILURE: force exit Pipeline execution
            }
            post{
                failure{
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
                    TEST_FORM_STATUS_CODE == 0 && TEST_API_STATUS_CODE ==0;
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
        
        stage('Deploying'){
            steps{
                echo 'Deploying over Cluster'
                sh '''
                    var=$(sudo kubectl get deploy cmd-api --ignore-not-found)
                    if [[ "$var" == "" ]]
                    then
                        sudo kubectl create -f /root/deployAPI/form.yml
                        sudo kubectl create -f /root/deployAPI/api.yml
                    else
                        sudo kubectl apply -f /root/deployAPI/form.yml
                        sudo kubectl apply -f /root/deployAPI/api.yml 
                    fi
                    sleep 30
                    pod_api=$(sudo kubectl get pods -l app=cmd-api -o jsonpath="{.items[0].metadata.name}")
                    pod_form=$(sudo kubectl get pods -l app=cmd-form -o jsonpath="{.items[0].metadata.name}")
                    sudo kubectl cp /root/deployAPI/*.html $pod_api:/var/www/html
                    sudo kubectl cp /root/deployAPI/*.py $pod_api:/var/www/cgi-bin
                    sudo kubectl exec $pod_api -- chmod +x /var/www/cgi-bin/cmdapi.py
                '''
            }
            post{
                success{
                    echo 'Deployment success'
                }
                failure{
                    echo 'Deployment failed'
                }
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
                    \n\nPipeline executed successfully ''',
                    to: "${ADMIN_EMAIL}",
                    subject: 'Build SUCCESS in Jenkins: $PROJECT_NAME - #$BUILD_NUMBER'
        }
    }
}

/*

def TEST_FORM_STATUS_CODE = 1
def TEST_API_STATUS_CODE = 1

*/
