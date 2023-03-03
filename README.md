# k8s-poc-pvc

#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <context_name>"
  exit 1
fi

# Set the context to the given name
kubectl config use-context "$1"

# Get the clusterroles and save them to a file
kubectl get clusterroles -o json | jq '.items' > "$1-clusterroles.json"

# Get the clusterrolebindings and save them to a file
kubectl get clusterrolebindings -o json | jq '.items' > "$1-clusterrolebindings.json"

# Call the Node.js script with the file paths and context name
node index.js "$1-clusterroles.json" "$1-clusterrolebindings.json" "$1"
