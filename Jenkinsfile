pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        IMAGE = 'qogam-sentiment:latest'
    }

    stages {
        stage('Test') {
            steps {
                sh '''
                    tar -cf - --exclude .git --exclude .venv --exclude report . \
                      | docker run -i --rm python:3.12-slim \
                        bash -lc "mkdir /work && tar -C /work -xf - && cd /work && pip install --no-cache-dir -r requirements-dev.txt && python -m pytest -q"
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t "$IMAGE" .'
            }
        }

        stage('Push image') {
            when {
                expression { return env.DOCKERHUB_USER?.trim() }
            }
            steps {
                sh '''
                    echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                    docker tag "$IMAGE" "$DOCKERHUB_USER/qogam-sentiment:latest"
                    docker push "$DOCKERHUB_USER/qogam-sentiment:latest"
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    if docker ps --format "{{.Names}}" | grep -qx assignment5-control-plane; then
                      sh scripts/deploy-kind.sh
                    else
                      echo "Kind cluster assignment5 is not running. Skipping deploy."
                    fi
                '''
            }
        }
    }
}
