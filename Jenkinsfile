pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-u root:root'
        }
    }

    stages {

        stage('Prepare') {
            steps {
                sh 'apt update'
                sh 'apt install -y qemu-system-arm chromium chromium-driver locust jq'
                sh 'pip install --upgrade pip'
                sh 'pip install -r tests/requirements.txt'
            }
        }

        stage('Start QEMU') {
            steps {
                sh 'chmod +x scripts/start_qemu.sh'
                sh 'scripts/start_qemu.sh'
            }
        }

        stage('Redfish Tests') {
            steps {
                sh 'chmod +x scripts/run_redfish_tests.sh'
                sh 'scripts/run_redfish_tests.sh'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test_report_redfish.html', allowEmptyArchive: true
                }
            }
        }

        stage('WebUI Tests') {
            steps {
                sh 'chmod +x scripts/run_webui_tests.sh'
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
                sh 'chmod +x scripts/run_load_tests.sh'
                sh 'scripts/run_load_tests.sh'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'locust_stats.csv', allowEmptyArchive: true
                }
            }
        }
    }
}
