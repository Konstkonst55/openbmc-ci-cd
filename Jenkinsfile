pipeline {
    agent any

    environment {
        BMC_URL = 'https://localhost:2443'
    }

    stages {
        stage('Подготовка окружения') {
            steps {
                sh '''
                    mkdir -p ${WORKSPACE}/artifacts/webui_tests
                    mkdir -p ${WORKSPACE}/artifacts/redfish_tests
                    mkdir -p ${WORKSPACE}/artifacts/load_tests
                    mkdir -p ${WORKSPACE}/artifacts/qemu_logs
                    
                    chmod +x ${WORKSPACE}/scripts/*.sh
                    chmod +x ${WORKSPACE}/chromedriver/chromedriver
                '''
            }
        }

        stage('Запуск QEMU с OpenBMC') {
            steps {
                sh '${WORKSPACE}/scripts/start_qemu.sh'
                sh '''
                    timeout 300 bash -c "until curl -k -s ${BMC_URL} > /dev/null; do sleep 10; done"
                '''
            }
        }

        stage('Web UI Тесты') {
            steps {
                sh '${WORKSPACE}/scripts/run_webui_tests.sh'
            }
        }

        stage('Redfish API Тесты') {
            steps {
                sh '${WORKSPACE}/scripts/run_redfish_tests.sh'
            }
        }

        stage('Нагрузочное тестирование') {
            steps {
                sh '${WORKSPACE}/scripts/run_load_tests.sh'
            }
        }
    }

    post {
        always {
            sh '${WORKSPACE}/scripts/stop_qemu.sh'
            archiveArtifacts artifacts: '**/artifacts/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: '**/artifacts/**/*.html', allowEmptyArchive: true
        }
    }
}