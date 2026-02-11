# Todo Platform - Event-Driven Architecture

## Security Configuration

This platform uses environment variables and Kubernetes secrets to manage sensitive configuration. **Never hardcode credentials in configuration files or Docker images.**

### Setting up Secrets

Before deploying, you must create the required secrets with your actual values:

#### 1. Create Kubernetes Secrets

```bash
# Create the secrets with your actual values (base64 encoded)
kubectl create secret generic todo-secrets \
  --from-literal=database-url=$(echo -n 'your-postgres-url' | base64) \
  --from-literal=secret-key=$(echo -n 'your-secret-key' | base64) \
  --from-literal=openrouter-api-key=$(echo -n 'your-openrouter-api-key' | base64)
```

#### 2. Using Environment Files

For local development, create a `.env` file with your credentials:

```env
DATABASE_URL=your_postgres_url
SECRET_KEY=your_secret_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

Then load it when running services:

```bash
export $(grep -v '^#' .env | xargs)
```

### Required Secrets

The following secrets are required for the platform to function:

- `database-url`: PostgreSQL connection string
- `secret-key`: Secret key for JWT signing
- `openrouter-api-key`: API key for OpenRouter

### Security Best Practices

1. **Never commit secrets to version control**
2. **Use strong, randomly generated secrets**
3. **Rotate secrets regularly**
4. **Use different secrets for different environments**
5. **Restrict access to secrets using RBAC**

### Deployment

When deploying to Kubernetes, ensure that the `todo-secrets` secret exists in the target namespace before deploying the platform:

```bash
# Verify secrets exist
kubectl get secret todo-secrets

# Deploy the platform
helm install todo-platform ./helm-charts/todo-platform
```