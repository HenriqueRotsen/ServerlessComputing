#!/bin/bash
kubectl delete configmap --all &&
kubectl create configmap pyfile --from-file pyfile=~/mymodule.py --output yaml > pyfile-configmap.yaml &&
kubectl create configmap outputkey \
    --from-literal REDIS_OUTPUT_KEY=henriqueferreira-proj3-output \
    --output yaml > outputkey-configmap.yaml &&
kubectl delete deployment serverless-redis &&
kubectl apply -f ~/deployment.yaml 