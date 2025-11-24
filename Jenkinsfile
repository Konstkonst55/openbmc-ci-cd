pipeline {
    agent any

    stages {
        stage('Установка зависимостей') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y python3 python3-pip python3-venv qemu-system-arm wget unzip curl
                    python3 -m venv /opt/venv
                    . /opt/venv/bin/activate
                    pip install -r tests/requirements.txt
                '''
            }
        }

        stage('Скачивание OpenBMC образа') {
            steps {
                sh '''
                    mkdir -p romulus
                    cd romulus
                    wget -q "https://jenkins.openbmc.org/job/ci-openbmc/lastSuccessfulBuild/distro=ubuntu,label=docker-builder,target=romulus/artifact/openbmc/build/tmp/deploy/images/romulus/*zip*/romulus.zip" -O romulus.zip
                    unzip -o romulus.zip
                    find . -name "*.static.mtd" -exec mv {} . \\;
                '''
            }
        }

        stage('Запуск QEMU с OpenBMC') {
            steps {
                sh '''
                    ./scripts/stop_qemu.sh || true
                    ./scripts/start_qemu.sh
                '''
            }
        }

        stage('Redfish API тесты') {
            steps {
                sh '''
                    . /opt/venv/bin/activate
                    ./scripts/run_redfish_tests.sh
                '''
            }
        }

        stage('WebUI тесты OpenBMC') {
            steps {
                sh '''
                    . /opt/venv/bin/activate
                    ./scripts/run_webui_tests.sh
                '''
            }
        }

        stage('Нагрузочное тестирование') {
            steps {
                sh '''
                    . /opt/venv/bin/activate
                    ./scripts/run_load_tests.sh
                '''
            }
        }
    }

    post {
        always {
            sh './scripts/stop_qemu.sh || true'
            archiveArtifacts artifacts: '*.html', allowEmptyArchive: true
        }
    }
}