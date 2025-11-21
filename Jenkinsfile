pipeline {
    agent any
    
    parameters {
        string(name: 'BMC_URL', defaultValue: 'https://localhost:2443', description: 'OpenBMC URL')
        string(name: 'BMC_USERNAME', defaultValue: 'root', description: 'OpenBMC username')
        string(name: 'BMC_PASSWORD', defaultValue: '0penBmc', description: 'OpenBMC password')
        string(name: 'QEMU_IMAGE', defaultValue: 'romulus/obmc-phosphor-image-romulus-20251003025918.static.mtd', description: 'QEMU image path')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Start QEMU with OpenBMC') {
            steps {
                script {
                    sh '''
                        chmod +x scripts/start_qemu.sh
                        scripts/start_qemu.sh
                    '''
                }
                sleep time: 60, unit: 'SECONDS'
            }
        }
        
        stage('Run Redfish API Tests') {
            steps {
                script {
                    sh '''
                        chmod +x scripts/run_redfish_tests.sh
                        scripts/run_redfish_tests.sh
                    '''
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'redfish_test_report.html',
                        reportName: 'Redfish Tests Report'
                    ])
                    archiveArtifacts artifacts: 'redfish_test_report.html', fingerprint: true
                }
            }
        }
        
        stage('Run WebUI Tests') {
            steps {
                script {
                    sh '''
                        chmod +x scripts/run_webui_tests.sh
                        scripts/run_webui_tests.sh
                    '''
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'webui_test_report.html',
                        reportName: 'WebUI Tests Report'
                    ])
                    archiveArtifacts artifacts: 'reports/webui_test_report.html', fingerprint: true
                    archiveArtifacts artifacts: 'test_log.log', fingerprint: true
                }
            }
        }
        
        stage('Run Load Testing') {
            steps {
                script {
                    sh '''
                        chmod +x scripts/run_load_tests.sh
                        scripts/run_load_tests.sh
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'locust_report.html', fingerprint: true
                }
            }
        }
    }
    
    post {
        always {
            sh 'pkill -f qemu-system-arm || true'
            
            cleanWs()
        }
    }
}