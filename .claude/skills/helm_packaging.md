# Helm-Packaging-Skill

Skill to package manifests into Helm Charts. It must:
1. Create a standardized folder structure (templates/, values.yaml, Chart.yaml)
2. Parametrize environment variables (DB_URL, API_KEYS) in values.yaml
3. Implement dry-run validation to check for template errors

## Purpose
This skill packages Kubernetes manifests into standardized, configurable Helm Charts that can be deployed across different environments.

## Capabilities
- Generate standardized Helm chart structure with templates, values.yaml, and Chart.yaml
- Parameterize environment-specific configurations in values.yaml
- Create reusable and configurable templates for different deployment scenarios
- Implement validation mechanisms including dry-run checks
- Support multiple environments (dev, staging, prod) through values files
- Handle dependencies between charts when needed

## Expected Outputs
- Chart.yaml with chart metadata and version information
- values.yaml with configurable parameters and default values
- templates/ directory with parametrized Kubernetes manifest templates
- Optional: requirements.yaml or Chart.yaml dependencies
- Validation scripts for dry-run testing

## Constraints
- Must follow Helm best practices and standard folder structure
- Environment variables must be properly parameterized in values.yaml
- Templates must support dry-run validation without errors
- Should maintain backward compatibility when updating charts
- Must handle sensitive data appropriately (using Kubernetes secrets)