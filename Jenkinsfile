pipeline {
    agent any

    environment {
        PATH = "/var/jenkins_home/.local/bin:/usr/local/bin:${env.PATH}"
        QEMU_PID = ""
    }

    stages {
        stage('Prepare') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y qemu-system-arm chromium-browser chromium-driver unzip wget curl python3-pip
                    pip3 install --user -r tests/requirements.txt
                '''
            }
        }

        stage('Start QEMU') {
            steps {
                script {
                    QEMU_PID = sh(script: "scripts/start_qemu.sh & echo \$!", returnStdout: true).trim()
                    env.QEMU_PID = QEMU_PID
                }
                sh 'sleep 60'
            }
        }

        stage('Redfish Tests') {
            steps {
                sh 'scripts/run_redfish_tests.sh'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'redfish_report.html', allowEmptyArchive: true
                }
            }
        }

        stage('WebUI Tests') {
            steps {
                sh 'scripts/run_webui_tests.sh'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'webui_report.html', allowEmptyArchive: true
                }
            }
        }

        stage('Load Tests') {
            steps {
                sh 'scripts/run_load_tests.sh'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'locust_report.html', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            sh 'kill ${QEMU_PID} || true'
            sh 'pkill -9 qemu-system-arm || true'
        }
    }
}