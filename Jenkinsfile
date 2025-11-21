pipeline {
    agent any

    environment {
        PATH = "/var/jenkins_home/.local/bin:${PATH}"
    }

    stages {

        stage('Prepare') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y qemu-system-arm chromium chromium-driver unzip wget
                    pip3 install --break-system-packages -r tests/requirements.txt
                '''
            }
        }

        stage('Start QEMU') {
            steps {
                sh '''
                    chmod +x scripts/start_qemu.sh
                    scripts/start_qemu.sh
                '''
            }
        }

        stage('Redfish Tests') {
            steps {
                sh '''
                    chmod +x scripts/run_redfish_tests.sh
                    scripts/run_redfish_tests.sh
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test_report_redfish.html'
                }
            }
        }

        stage('WebUI Tests') {
            steps {
                sh '''
                    chmod +x scripts/run_webui_tests.sh
                    scripts/run_webui_tests.sh
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'webui_report.html'
                }
            }
        }

        stage('Load Tests') {
            steps {
                sh '''
                    chmod +x scripts/run_load_tests.sh
                    scripts/run_load_tests.sh
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'locust_stats.csv'
                }
            }
        }
    }
}
