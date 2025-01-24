#!/bin/bash
kubectl delete configmap --all &&
kubectl create configmap pyfile --from-file pyfile=~/mymodule.py --output yaml > pyfile-configmap.yaml &&
kubectl create configmap outputkey \
    --from-literal REDIS_OUTPUT_KEY=henriqueferreira-proj3-output \
    --output yaml > outputkey-configmap.yaml &&
kubectl delete deployment serverless-redis && # Comment this on the first running
kubectl apply -f ~/deployment.yaml 


# kubectl create configmap zipfile --from-file=zipfile.zip=/home/gabrielreis/opt/zipfile.zip -n gabrielreis --output yaml  > ~/TP3/k8s/configMap6.yaml &&