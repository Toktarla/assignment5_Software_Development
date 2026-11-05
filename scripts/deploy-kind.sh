#!/bin/sh
# Load the local image into the kind cluster and apply the manifests.
# Jenkins calls this after the image build. It needs the Docker socket,
# because the cluster node is itself a container named assignment5-control-plane.

set -eu

NODE=assignment5-control-plane
IMAGE=qogam-sentiment:latest

if ! docker ps --format '{{.Names}}' | grep -qx "$NODE"; then
  echo "Kind node $NODE is not running. Start it with: kind create cluster --name assignment5"
  exit 1
fi

echo "Loading $IMAGE into $NODE"
docker save "$IMAGE" | docker exec -i "$NODE" ctr -n k8s.io images import -

echo "Applying Kubernetes manifests"
{
  cat k8s/deployment.yaml
  printf '\n---\n'
  cat k8s/service.yaml
} | docker exec -i "$NODE" kubectl --kubeconfig=/etc/kubernetes/admin.conf apply -f -

echo "Restarting the deployment so the new image is the one that runs"
docker exec "$NODE" \
  kubectl --kubeconfig=/etc/kubernetes/admin.conf \
  rollout restart deployment/qogam-sentiment

echo "Waiting for the rollout"
docker exec "$NODE" \
  kubectl --kubeconfig=/etc/kubernetes/admin.conf \
  rollout status deployment/qogam-sentiment --timeout=180s

docker exec "$NODE" \
  kubectl --kubeconfig=/etc/kubernetes/admin.conf get pods,svc
