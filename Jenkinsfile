pipeline {
    agent any

    stages {

        stage('Prepare') {
            steps {
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
