
docker image pull public.ecr.aws/aws-cli/aws-cli
sleep 10
kubectl apply -f debugpod.yaml
sleep 10
kubectl exec --stdin --tty debug-pod -- /bin/bash