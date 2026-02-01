---
id: "001"
title: "Phase IV Cloud-Native Deployment"
stage: "constitution"
date_iso: "2026-01-29"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-frontend-ui-upgrade"
user: "Faizaan"
command: "/sp.constitution"
labels: ["constitution", "cloud-native", "deployment", "kubernetes", "minikube"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
  - "None"
outcome: "Successfully updated constitution to include Phase IV Cloud-Native Deployment requirements, authorizing containerization with Docker, orchestration with Kubernetes/Helm on Minikube, and AIOps tools like Gordon, kubectl-ai, and Kagent. Implemented Spec-Driven approach for all deployment artifacts with no manual coding allowed."
evaluation: "Complete"
---

# Phase IV Cloud-Native Deployment Constitution

## User Input
```
# Phase IV: Cloud-Native Deployment Constitution

You are an Expert DevOps AI Orchestrator. Your mission is to migrate the Phase III Todo Chatbot to a Local Kubernetes Environment (Minikube) using a strictly Spec-Driven approach.

## 1. Core Mandate
- **No Manual Coding:** All Dockerfiles, Helm Charts, and K8s Manifests must be generated via Agent Skills or AI Tools (Gordon/kubectl-ai).
- **Tool Preference:** Use 'Gordon' (Docker AI) for all containerization tasks and 'kubectl-ai' or 'Kagent' for all Kubernetes operations.
- **Verification First:** Before any deployment, you must verify that Minikube is running and Docker Desktop (Beta) is active.

## 2. Technology Stack & Constraints
- **Containerization:** Use Multi-stage builds for Frontend (Next.js) and Backend (FastAPI).
- **Orchestration:** Deploy on Minikube using Helm Charts.
- **AIOps Integration:** - Use `docker ai` for image optimization suggestions.
    - Use `kubectl-ai` for generating K8s resources (e.g., "deploy frontend with 2 replicas").
    - Use `kagent` for debugging cluster health and resource optimization.

## 3. Workflow Protocol
1. **Spec Writing:** Always start by updating the architecture spec in `.claudespec`.
2. **Plan Generation:** Generate a step-by-step plan before execution.
3. **Task Execution:** Break down the plan into atomic tasks (e.g., Build Backend -> Build Frontend -> Setup Helm -> Deploy).
4. **Validation:** After every deployment, run `kubectl get pods` and `kagent "analyze cluster"` to ensure 100% health.

## 4. Error Handling
- If a pod fails (CrashLoopBackOff), do not guess. Invoke the 'AIOps-Observability-Skill' to diagnose using Kagent logic.
- If `kubectl-ai` fails, check the API Key configuration and cluster context.

## 5. Deployment Naming Convention
- Image Tags: `faizananjum/<app-name>:v1`
- Namespace: `todo-chatbot`
```

## Response Summary
Updated the project constitution to include Phase IV Cloud-Native Deployment requirements. The new version (3.0.0) introduces:

- Authorization for containerization using Docker with Multi-stage builds
- Orchestration on Minikube using Helm Charts
- AIOps tools including Gordon, kubectl-ai, and Kagent for automation
- Strict Spec-Driven approach for all deployment artifacts
- No manual coding requirement for Dockerfiles, Helm Charts, and K8s Manifests
- Proper phase isolation maintaining all existing functionality
- Updated technology stack to include containerization and orchestration tools

The constitution now properly governs the transition from Phase III AI Todo Chatbot to Phase IV Cloud-Native Deployment while maintaining backward compatibility and following Spec-Driven Development principles.