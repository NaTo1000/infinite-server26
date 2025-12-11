# Infinite Server26 - Kubernetes Deployment

Kubernetes manifests for deploying Infinite Server26 Fortress.

## Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Storage provisioner (for PVCs)
- Optional: Ingress controller (nginx)
- Optional: cert-manager (for TLS)

## Quick Deploy

### Apply all manifests

```bash
kubectl apply -f k8s/
```

### Or apply individually

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create persistent volumes
kubectl apply -f k8s/persistent-volumes.yaml

# Create configmaps
kubectl apply -f k8s/configmap.yaml

# Create deployments
kubectl apply -f k8s/deployment.yaml

# Create services
kubectl apply -f k8s/service.yaml

# Create ingress (optional)
kubectl apply -f k8s/ingress.yaml
```

## Verify Deployment

```bash
# Check namespace
kubectl get namespace infinite-server26

# Check pods
kubectl get pods -n infinite-server26

# Check services
kubectl get svc -n infinite-server26

# Check ingress
kubectl get ingress -n infinite-server26

# View logs
kubectl logs -n infinite-server26 -l app=infinite-server26 -f
```

## Access Services

### Via LoadBalancer (if configured)

```bash
# Get external IP
kubectl get svc infinite-server26-service -n infinite-server26

# Access via external IP
curl http://<EXTERNAL-IP>:8000/health
```

### Via Port Forwarding

```bash
# Forward main service
kubectl port-forward -n infinite-server26 svc/infinite-server26-service 8000:8000

# Access locally
curl http://localhost:8000/health
```

### Via Ingress (if configured)

Access via configured domain:
- https://fortress.infiniteserver26.com

## Scaling

```bash
# Scale deployment
kubectl scale deployment infinite-server26 -n infinite-server26 --replicas=3

# Scale web UI
kubectl scale deployment web-ui -n infinite-server26 --replicas=5
```

## Update Deployment

```bash
# Update image
kubectl set image deployment/infinite-server26 -n infinite-server26 \
  fortress=nato1000/infinite-server26:26.2

# Check rollout status
kubectl rollout status deployment/infinite-server26 -n infinite-server26

# Rollback if needed
kubectl rollout undo deployment/infinite-server26 -n infinite-server26
```

## Monitoring

```bash
# Watch pods
kubectl get pods -n infinite-server26 -w

# Describe pod
kubectl describe pod <pod-name> -n infinite-server26

# Get logs
kubectl logs -n infinite-server26 <pod-name>

# Execute into pod
kubectl exec -it -n infinite-server26 <pod-name> -- /bin/bash
```

## Clean Up

```bash
# Delete all resources
kubectl delete -f k8s/

# Or delete namespace (removes everything)
kubectl delete namespace infinite-server26
```

## Helm Chart (Alternative)

For easier management, consider using Helm:

```bash
# Create Helm chart
helm create infinite-server26

# Install with Helm
helm install fortress ./infinite-server26 -n infinite-server26 --create-namespace

# Upgrade
helm upgrade fortress ./infinite-server26 -n infinite-server26

# Uninstall
helm uninstall fortress -n infinite-server26
```

## Resource Requests

- **Fortress Container**: 2Gi RAM, 1 CPU (request) | 4Gi RAM, 2 CPU (limit)
- **Web UI**: 128Mi RAM, 0.1 CPU (request) | 256Mi RAM, 0.2 CPU (limit)

## Storage

- **Fortress Data**: 10Gi
- **Vault Storage**: 50Gi
- **Logs**: 5Gi
- **Rancher Data**: 20Gi

## Security Considerations

1. Update default passwords in ConfigMap/Secrets
2. Enable RBAC
3. Use NetworkPolicies
4. Enable Pod Security Standards
5. Regular security scans
6. Keep images updated

## Troubleshooting

### Pod not starting

```bash
kubectl describe pod <pod-name> -n infinite-server26
kubectl logs <pod-name> -n infinite-server26
```

### Service not accessible

```bash
kubectl get endpoints -n infinite-server26
kubectl describe svc infinite-server26-service -n infinite-server26
```

### PVC not bound

```bash
kubectl get pvc -n infinite-server26
kubectl describe pvc <pvc-name> -n infinite-server26
```

## Author

Built by NaTo1000 - Version 26.1 FORTRESS
