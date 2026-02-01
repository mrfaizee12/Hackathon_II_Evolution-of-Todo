# Quickstart Guide: Phase IV Cloud-Native Deployment

**Feature**: Phase IV Cloud-Native Deployment
**Date**: 2026-01-29
**Status**: Draft

## Overview

This guide provides step-by-step instructions to deploy the Phase III Todo Chatbot application to a local Kubernetes cluster (Minikube) using AI-driven tools.

## Prerequisites

### System Requirements
- Docker Desktop with Beta features enabled
- Minikube (latest version)
- kubectl
- kubectl-ai plugin
- Helm v3
- Gordon (Docker AI tooling)
- Docker Hub account

### Resource Requirements
- 4 CPU cores minimum
- 8GB RAM minimum
- 20GB free disk space

## Setup Instructions

### 1. Start Minikube

```bash
# Start Minikube with adequate resources
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Configure Docker to use Minikube's Docker daemon
eval $(minikube docker-env)
```

### 2. Prepare Docker Images

```bash
# Navigate to backend directory
cd backend

# Use Gordon to generate optimized Dockerfile
# (This should be done via Gordon AI tooling)
# gordon analyze ./backend
# gordon generate-dockerfile --multi-stage

# Build backend image
docker build -t faizananjum/backend:v1 .

# Navigate to frontend directory
cd ../frontend

# Use Gordon to generate optimized Dockerfile
# (This should be done via Gordon AI tooling)
# gordon analyze ./frontend
# gordon generate-dockerfile --multi-stage

# Build frontend image
docker build -t faizananjum/frontend:v1 .

# Verify images were built
docker images | grep faizananjum
```

### 3. Create Kubernetes Namespace

```bash
# Create the required namespace
kubectl create namespace todo-chatbot

# Verify namespace creation
kubectl get namespaces
```

### 4. Configure Secrets

```bash
# Create secrets for OpenRouter API keys
kubectl create secret generic openrouter-secrets \
  --from-literal=OPENROUTER_API_KEY=<your-openrouter-api-key> \
  --namespace=todo-chatbot

# Create database credentials secret (if needed)
kubectl create secret generic database-secrets \
  --from-literal=DATABASE_URL=<your-db-url> \
  --namespace=todo-chatbot
```

### 5. Deploy PostgreSQL

```bash
# Use kubectl-ai to generate and apply PostgreSQL deployment
kubectl-ai "deploy postgresql with persistent storage in todo-chatbot namespace"

# Or manually create:
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
  namespace: todo-chatbot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:15
        envFrom:
        - secretRef:
            name: database-secrets
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgresql-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgresql-storage
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql
  namespace: todo-chatbot
spec:
  selector:
    app: postgresql
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
  type: ClusterIP
EOF
```

### 6. Generate and Apply Application Manifests

```bash
# Use kubectl-ai to generate manifests for backend (2 replicas)
kubectl-ai "create backend deployment with 2 replicas, service, and health checks in todo-chatbot namespace"

# Use kubectl-ai to generate manifests for frontend (1 replica)
kubectl-ai "create frontend deployment with 1 replica, service, and load balancer in todo-chatbot namespace"

# Or apply using Helm chart (after creating it):
helm install todo-chatbot ./helm-charts/todo-chatbot --namespace todo-chatbot --create-namespace
```

### 7. Package as Helm Chart

```bash
# Create Helm chart structure
helm create todo-chatbot

# Customize the chart with your manifests
# (Replace the default templates with your generated manifests)

# Package and install the chart
helm package todo-chatbot
helm install todo-chatbot ./todo-chatbot-0.1.0.tgz --namespace todo-chatbot --create-namespace
```

### 8. Verify Deployment

```bash
# Check all pods are running
kubectl get pods --namespace todo-chatbot

# Check all services are available
kubectl get services --namespace todo-chatbot

# Use kagent to analyze cluster health
kagent "analyze cluster health in todo-chatbot namespace"
```

### 9. Access the Application

```bash
# Get the frontend service external IP
kubectl get services --namespace todo-chatbot

# If using LoadBalancer, wait for external IP assignment
kubectl get service frontend-service --namespace todo-chatbot --watch

# Or use port forwarding for testing
kubectl port-forward svc/frontend-service 8080:80 --namespace todo-chatbot
```

## Troubleshooting

### Common Issues

**Issue**: Pods stuck in Pending state
**Solution**: Check Minikube resources and ensure adequate CPU/RAM allocated

**Issue**: Images not found in Minikube
**Solution**: Ensure Docker is configured to use Minikube's daemon: `eval $(minikube docker-env)`

**Issue**: Services not accessible
**Solution**: Use `minikube tunnel` to expose LoadBalancer services

### Diagnostic Commands

```bash
# Check pod status and logs
kubectl get pods --namespace todo-chatbot
kubectl logs <pod-name> --namespace todo-chatbot

# Analyze cluster with kagent
kagent "describe issues in todo-chatbot namespace"

# Check service endpoints
kubectl get endpoints --namespace todo-chatbot
```

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-chatbot --namespace todo-chatbot

# Delete namespace
kubectl delete namespace todo-chatbot

# Stop Minikube
minikube stop
```