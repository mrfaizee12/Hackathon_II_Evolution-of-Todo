# Containerization-Skill

Skill to containerize FastAPI and Next.js applications. It must:
1. Generate multi-stage Dockerfiles to minimize image size
2. Use 'Gordon' (Docker AI) to optimize layer caching
3. Output 'docker-compose.yaml' for local orchestration testing before K8s deployment

## Purpose
This skill enables the transformation of FastAPI and Next.js applications into optimized container images using best practices for multi-stage builds and efficient layer caching.

## Capabilities
- Generate optimized multi-stage Dockerfiles for both backend (FastAPI) and frontend (Next.js) applications
- Implement layer caching strategies to minimize rebuild times
- Create docker-compose.yaml for local testing and validation
- Ensure minimal image sizes through proper base image selection and cleanup steps
- Apply security best practices in container configurations

## Expected Outputs
- Multi-stage Dockerfile for FastAPI backend
- Multi-stage Dockerfile for Next.js frontend
- docker-compose.yaml for local orchestration testing
- Build scripts and configuration files

## Constraints
- Must prioritize image size minimization
- Should leverage Gordon's optimization capabilities
- Dockerfiles must support local testing before Kubernetes deployment
- Must follow security best practices (non-root users, minimal attack surface)