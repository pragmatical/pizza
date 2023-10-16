# Deployment notes

## Create Required K8s Secret

```bash
kubectl create secret generic pizza-api-secret \
  --from-literal=OPENAI_ENDPOINT='your endpoint' \
  --from-literal=OPENAI_API_KEY='your api key'

```
