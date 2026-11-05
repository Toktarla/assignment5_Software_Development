# Assignment 5. Sentiment scorer

Small Python service for the Kazakh and Russian public-sentiment project. Jenkins tests it, builds a Docker image, and can deploy that image to a local kind cluster.

Repository: https://github.com/Toktarla/assignment5_Software_Development

## Run the tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## Build and run the image

```bash
docker build -t qogam-sentiment:latest .
docker run --rm -p 8000:8000 qogam-sentiment:latest
```

Health check: http://127.0.0.1:8000/api/health

## Jenkins

Jenkins runs in Docker and uses the Docker socket so it can build images. The setup wizard is turned off. A local admin user is created on first start by a script that is not committed.

```bash
docker build -t assignment5-jenkins jenkins
docker run -d --name assignment5-jenkins \
  -p 8080:8080 -p 50000:50000 \
  -u root \
  -v assignment5-jenkins-home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD/jenkins/init.groovy:/usr/share/jenkins/ref/init.groovy.d/01-admin.groovy:ro" \
  -e JAVA_OPTS=-Djenkins.install.runSetupWizard=false \
  -e JENKINS_ADMIN_PASSWORD \
  assignment5-jenkins
```

`jenkins/init.groovy` is gitignored. It creates the user `toktar` from `JENKINS_ADMIN_PASSWORD` on the first start. The container runs as root so the Docker socket on Docker Desktop can be used.

The job reads `Jenkinsfile` from `main`. It polls GitHub every two minutes. A laptop Jenkins cannot receive GitHub webhooks without a public address.

Push to Docker Hub is in the Jenkinsfile and stays off until `DOCKERHUB_USER` and `DOCKERHUB_TOKEN` are set on the job.

## Kubernetes

```bash
kind create cluster --name assignment5
sh scripts/deploy-kind.sh
```

The deploy step loads the image into the kind node with `ctr`, then runs `kubectl apply`. Kind does not pull `qogam-sentiment:latest` from Docker Hub, because that image exists only on this machine.
