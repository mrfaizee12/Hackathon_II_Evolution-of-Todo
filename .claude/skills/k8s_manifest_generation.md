# K8s-Manifest-Skill

Skill to transform application specs into Kubernetes manifests. It must:
1. Generate Deployment, Service, and Ingress resources
2. Integrate 'kubectl-ai' prompts for automated scaling logic (replicas)
3. Ensure compatibility with Minikube local storage classes

## Purpose
This skill converts application specifications into properly configured Kubernetes manifests suitable for deployment on local Minikube clusters.

## Capabilities
- Generate Kubernetes Deployments with appropriate resource requests and limits
- Create Services for internal and external communication
- Configure Ingress resources for traffic routing
- Integrate kubectl-ai for intelligent replica scaling decisions
- Ensure compatibility with Minikube's local storage classes and networking
- Implement health checks and readiness/liveness probes

## Expected Outputs
- deployment.yaml for application deployments
- service.yaml for service discovery and load balancing
- ingress.yaml for traffic routing and external access
- ConfigMaps and Secrets as needed
- Resource configurations compatible with Minikube

## Constraints
- Must work seamlessly with Minikube local development environment
- Should integrate kubectl-ai for intelligent scaling
- Storage classes must be compatible with local Minikube setup
- Manifests must follow Kubernetes best practices and security guidelines