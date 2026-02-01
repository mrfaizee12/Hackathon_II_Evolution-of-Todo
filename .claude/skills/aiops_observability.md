# AIOps-Observability-Skill

Skill to monitor and debug using AI Agents. It must:
1. Use 'Kagent' to analyze pod logs during 'ImagePullBackOff' or 'CrashLoopBackOff'
2. Execute 'kubectl-ai' commands to describe failed resources
3. Provide automated optimization suggestions for resource limits (CPU/Memory)

## Purpose
This skill implements AI-powered observability and debugging capabilities for Kubernetes deployments, enabling automated analysis and resolution of common deployment issues.

## Capabilities
- Analyze pod logs and events to identify root causes of deployment failures
- Diagnose common Kubernetes issues like ImagePullBackOff and CrashLoopBackOff
- Execute intelligent kubectl-ai commands for resource inspection
- Provide automated recommendations for resource optimization
- Monitor deployment health and performance metrics
- Generate actionable insights for performance improvements

## Expected Outputs
- Diagnostic reports for failed deployments
- Root cause analysis for common Kubernetes issues
- Optimization recommendations for CPU and memory limits
- Health status reports for deployed resources
- Automated remediation suggestions

## Constraints
- Must effectively use Kagent for log analysis and issue diagnosis
- Should leverage kubectl-ai for intelligent resource inspection
- Recommendations must be practical and implementable
- Should focus on common deployment failure scenarios
- Must provide clear, actionable insights for developers