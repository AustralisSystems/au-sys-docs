# Secrets Management: External Key Vaults & Credential Managers Best Practices

**Version**: v1.0.0
**Last Updated**: 2025-11-18

This document provides comprehensive best practices for integrating external key vaults and credential managers in production environments for modern applications (Python/FastAPI, Node.js/Next.js/NestJS), covering HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager, Kubernetes Secrets, Docker Secrets, integration patterns, selection guidance, and production deployment strategies.

**Related Documentation**: For local and development credential management, see [Secrets Management: Local & Development Best Practices](./secrets-management-local-development-best-practices-2025.md).

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [External Secrets Manager Selection Guide](#external-secrets-manager-selection-guide)
3. [HashiCorp Vault Integration](#hashicorp-vault-integration)
4. [AWS Secrets Manager Integration](#aws-secrets-manager-integration)
5. [Azure Key Vault Integration](#azure-key-vault-integration)
6. [Google Secret Manager Integration](#google-secret-manager-integration)
7. [Kubernetes Secrets Integration](#kubernetes-secrets-integration)
8. [Docker Secrets Integration](#docker-secrets-integration)
9. [Unified Integration Pattern](#unified-integration-pattern)
10. [Credential Rotation with External Systems](#credential-rotation-with-external-systems)
11. [Audit Logging & Monitoring](#audit-logging--monitoring)
12. [Production Deployment](#production-deployment)
13. [Security Best Practices](#security-best-practices)

---

## Architecture Principles

### External Secrets Manager Philosophy

**REQUIRED**: Understand external secrets management principles:

1. **Production First**: External secrets managers are REQUIRED for production
2. **Zero Trust**: Never trust, always verify - authenticate to secrets manager
3. **Least Privilege**: Minimum necessary access to secrets
4. **Audit Everything**: All secret access logged and monitored
5. **Rotation Ready**: Support automatic credential rotation
6. **Fail Secure**: Fail closed if secrets manager unavailable (with fallback strategy)

### When to Use External Secrets Managers

**REQUIRED**: Use external secrets managers when:

- **Production Environment**: All production deployments
- **Compliance Requirements**: SOC2, HIPAA, PCI-DSS, GDPR compliance
- **Multi-Environment**: Managing secrets across dev/staging/prod
- **Team Access**: Multiple teams need secure secret access
- **Audit Requirements**: Need comprehensive audit trails
- **Credential Rotation**: Automatic or scheduled credential rotation
- **High Security**: Sensitive data requiring enterprise-grade security

---

## External Secrets Manager Selection Guide

### Comparison Matrix

| Feature | HashiCorp Vault | AWS Secrets Manager | Azure Key Vault | Google Secret Manager | Kubernetes Secrets | Docker Secrets |
|---------|----------------|---------------------|-----------------|----------------------|-------------------|----------------|
| **Deployment** | Self-hosted or Cloud | AWS Managed | Azure Managed | GCP Managed | Kubernetes Native | Docker Native |
| **Cost** | Free (self-hosted) | Pay per secret/month | Pay per operation | Pay per secret/month | Free | Free |
| **Scalability** | High | High | High | High | Medium | Low |
| **Multi-Cloud** | ✅ Yes | ❌ AWS Only | ❌ Azure Only | ❌ GCP Only | ✅ Yes | ✅ Yes |
| **Dynamic Secrets** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Automatic Rotation** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Audit Logging** | ✅ Comprehensive | ✅ CloudTrail | ✅ Log Analytics | ✅ Cloud Logging | ⚠️ Limited | ⚠️ Limited |
| **Access Control** | ✅ Policies | ✅ IAM | ✅ RBAC | ✅ IAM | ⚠️ RBAC | ⚠️ Limited |
| **Best For** | Multi-cloud, complex | AWS-native apps | Azure-native apps | GCP-native apps | Kubernetes apps | Docker Swarm |

### Selection Criteria

**REQUIRED**: Choose based on your infrastructure:

1. **Cloud Provider**: Use native secrets manager if single cloud (AWS → AWS Secrets Manager, Azure → Azure Key Vault, GCP → Google Secret Manager)
2. **Multi-Cloud**: Use HashiCorp Vault for multi-cloud deployments
3. **Container Orchestration**: Use Kubernetes Secrets for K8s-native deployments
4. **Docker Swarm**: Use Docker Secrets for Swarm deployments
5. **Compliance**: Choose based on compliance requirements (Vault offers most flexibility)

---

## HashiCorp Vault Integration

### Overview

**HashiCorp Vault** is a self-hosted or cloud-managed secrets management solution offering dynamic secrets, encryption as a service, and comprehensive audit logging.

### Python/FastAPI Integration

**REQUIRED**: HashiCorp Vault integration:

```python
# services/secrets/vault_provider.py
import hvac
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)


class VaultProvider:
    """HashiCorp Vault secrets provider."""

    def __init__(self):
        self.client = None
        self.vault_url = os.getenv("VAULT_ADDR", "http://localhost:8200")
        self.vault_token = os.getenv("VAULT_TOKEN")
        self.vault_path = os.getenv("VAULT_SECRET_PATH", "secret/data/application")

    async def initialize(self):
        """Initialize Vault client."""
        try:
            self.client = hvac.Client(url=self.vault_url)

            # Authenticate
            if self.vault_token:
                self.client.token = self.vault_token
            else:
                # Try AppRole authentication
                role_id = os.getenv("VAULT_ROLE_ID")
                secret_id = os.getenv("VAULT_SECRET_ID")
                if role_id and secret_id:
                    self.client.auth.approle.login(
                        role_id=role_id,
                        secret_id=secret_id
                    )

            # Verify connection
            if not self.client.is_authenticated():
                raise ValueError("Vault authentication failed")

            logger.info(f"Vault provider initialized: {self.vault_url}")

        except Exception as e:
            logger.error(f"Vault initialization failed: {e}")
            raise

    async def get_secret(self, secret_name: str) -> Optional[str]:
        """Get secret from Vault."""
        try:
            # Read secret from KV v2 engine
            response = self.client.secrets.kv.v2.read_secret_version(
                path=f"{self.vault_path}/{secret_name}"
            )

            if response and 'data' in response and 'data' in response['data']:
                return response['data']['data'].get(secret_name)

        except Exception as e:
            logger.error(f"Failed to get secret '{secret_name}' from Vault: {e}")
            return None

    async def set_secret(self, secret_name: str, secret_value: str):
        """Set secret in Vault."""
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=f"{self.vault_path}/{secret_name}",
                secret={secret_name: secret_value}
            )
            logger.info(f"Secret '{secret_name}' updated in Vault")
        except Exception as e:
            logger.error(f"Failed to set secret '{secret_name}' in Vault: {e}")
            raise
```

### Node.js/TypeScript Integration

```typescript
// services/secrets/vaultProvider.ts
import * as vault from 'node-vault';
import { VaultOptions } from 'node-vault';

export class VaultProvider {
  private client: vault.client;
  private vaultPath: string;

  constructor() {
    const vaultUrl = process.env.VAULT_ADDR || 'http://localhost:8200';
    const vaultToken = process.env.VAULT_TOKEN;

    this.vaultPath = process.env.VAULT_SECRET_PATH || 'secret/data/application';

    const options: VaultOptions = {
      apiVersion: 'v1',
      endpoint: vaultUrl,
      token: vaultToken,
    };

    this.client = vault(options);
  }

  async initialize(): Promise<void> {
    try {
      // Verify connection
      const health = await this.client.health();
      if (!health.initialized) {
        throw new Error('Vault not initialized');
      }

      console.log('Vault provider initialized');
    } catch (error) {
      console.error('Vault initialization failed:', error);
      throw error;
    }
  }

  async getSecret(secretName: string): Promise<string | null> {
    try {
      const response = await this.client.read(
        `${this.vaultPath}/${secretName}`
      );

      if (response?.data?.data) {
        return response.data.data[secretName];
      }

      return null;
    } catch (error) {
      console.error(`Failed to get secret '${secretName}' from Vault:`, error);
      return null;
    }
  }

  async setSecret(secretName: string, secretValue: string): Promise<void> {
    try {
      await this.client.write(`${this.vaultPath}/${secretName}`, {
        [secretName]: secretValue,
      });
      console.log(`Secret '${secretName}' updated in Vault`);
    } catch (error) {
      console.error(`Failed to set secret '${secretName}' in Vault:`, error);
      throw error;
    }
  }
}
```

### Configuration

```bash
# Environment variables for Vault
VAULT_ADDR=https://vault.example.com:8200
VAULT_TOKEN=hvs.xxxxxxxxxxxxx
VAULT_SECRET_PATH=secret/data/application

# Or use AppRole authentication
VAULT_ROLE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
VAULT_SECRET_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## AWS Secrets Manager Integration

### Overview

**AWS Secrets Manager** is a fully managed service for storing and rotating secrets in AWS environments.

### Python/FastAPI Integration

**REQUIRED**: AWS Secrets Manager integration:

```python
# services/secrets/aws_secrets_provider.py
import boto3
from botocore.exceptions import ClientError
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)


class AWSSecretsProvider:
    """AWS Secrets Manager provider."""

    def __init__(self):
        self.client = boto3.client('secretsmanager', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        self.secret_prefix = os.getenv('AWS_SECRET_PREFIX', 'application')

    async def initialize(self):
        """Initialize AWS Secrets Manager client."""
        try:
            # Verify connection by listing secrets (with pagination)
            self.client.list_secrets(MaxResults=1)
            logger.info("AWS Secrets Manager provider initialized")
        except ClientError as e:
            logger.error(f"AWS Secrets Manager initialization failed: {e}")
            raise

    async def get_secret(self, secret_name: str) -> Optional[str]:
        """Get secret from AWS Secrets Manager."""
        try:
            full_secret_name = f"{self.secret_prefix}/{secret_name}"

            response = self.client.get_secret_value(SecretId=full_secret_name)

            # Secrets Manager can store JSON or plain text
            if 'SecretString' in response:
                secret_string = response['SecretString']
                try:
                    # Try to parse as JSON
                    secret_json = json.loads(secret_string)
                    # If JSON, return the value for the key matching secret_name
                    return secret_json.get(secret_name, secret_string)
                except json.JSONDecodeError:
                    # Plain text secret
                    return secret_string
            elif 'SecretBinary' in response:
                return response['SecretBinary'].decode('utf-8')

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.warning(f"Secret '{secret_name}' not found in AWS Secrets Manager")
            else:
                logger.error(f"Failed to get secret '{secret_name}' from AWS Secrets Manager: {e}")
            return None

    async def set_secret(self, secret_name: str, secret_value: str):
        """Set secret in AWS Secrets Manager."""
        try:
            full_secret_name = f"{self.secret_prefix}/{secret_name}"

            # Check if secret exists
            try:
                self.client.describe_secret(SecretId=full_secret_name)
                # Update existing secret
                self.client.update_secret(
                    SecretId=full_secret_name,
                    SecretString=secret_value
                )
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    # Create new secret
                    self.client.create_secret(
                        Name=full_secret_name,
                        SecretString=secret_value,
                        Description=f"Application secret: {secret_name}"
                    )
                else:
                    raise

            logger.info(f"Secret '{secret_name}' updated in AWS Secrets Manager")
        except ClientError as e:
            logger.error(f"Failed to set secret '{secret_name}' in AWS Secrets Manager: {e}")
            raise
```

### Node.js/TypeScript Integration

```typescript
// services/secrets/awsSecretsProvider.ts
import {
  SecretsManagerClient,
  GetSecretValueCommand,
  CreateSecretCommand,
  UpdateSecretCommand,
  DescribeSecretCommand,
} from '@aws-sdk/client-secrets-manager';

export class AWSSecretsProvider {
  private client: SecretsManagerClient;
  private secretPrefix: string;

  constructor() {
    const region = process.env.AWS_REGION || 'us-east-1';
    this.client = new SecretsManagerClient({ region });
    this.secretPrefix = process.env.AWS_SECRET_PREFIX || 'application';
  }

  async initialize(): Promise<void> {
    try {
      // Verify connection
      await this.client.send(new DescribeSecretCommand({ SecretId: 'test' }));
      console.log('AWS Secrets Manager provider initialized');
    } catch (error: any) {
      if (error.name !== 'ResourceNotFoundException') {
        console.error('AWS Secrets Manager initialization failed:', error);
        throw error;
      }
      // ResourceNotFoundException is expected for test secret
      console.log('AWS Secrets Manager provider initialized');
    }
  }

  async getSecret(secretName: string): Promise<string | null> {
    try {
      const fullSecretName = `${this.secretPrefix}/${secretName}`;

      const command = new GetSecretValueCommand({
        SecretId: fullSecretName,
      });

      const response = await this.client.send(command);

      if (response.SecretString) {
        try {
          const secretJson = JSON.parse(response.SecretString);
          return secretJson[secretName] || response.SecretString;
        } catch {
          return response.SecretString;
        }
      }

      if (response.SecretBinary) {
        return Buffer.from(response.SecretBinary).toString('utf-8');
      }

      return null;
    } catch (error: any) {
      if (error.name === 'ResourceNotFoundException') {
        console.warn(`Secret '${secretName}' not found in AWS Secrets Manager`);
      } else {
        console.error(`Failed to get secret '${secretName}':`, error);
      }
      return null;
    }
  }

  async setSecret(secretName: string, secretValue: string): Promise<void> {
    try {
      const fullSecretName = `${this.secretPrefix}/${secretName}`;

      try {
        await this.client.send(
          new DescribeSecretCommand({ SecretId: fullSecretName })
        );
        // Update existing
        await this.client.send(
          new UpdateSecretCommand({
            SecretId: fullSecretName,
            SecretString: secretValue,
          })
        );
      } catch (error: any) {
        if (error.name === 'ResourceNotFoundException') {
          // Create new
          await this.client.send(
            new CreateSecretCommand({
              Name: fullSecretName,
              SecretString: secretValue,
              Description: `Application secret: ${secretName}`,
            })
          );
        } else {
          throw error;
        }
      }

      console.log(`Secret '${secretName}' updated in AWS Secrets Manager`);
    } catch (error) {
      console.error(`Failed to set secret '${secretName}':`, error);
      throw error;
    }
  }
}
```

### Configuration

```bash
# Environment variables for AWS Secrets Manager
AWS_REGION=us-east-1
AWS_SECRET_PREFIX=application
AWS_ACCESS_KEY_ID=xxxxxxxxxxxxx  # Or use IAM role
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxx  # Or use IAM role
```

---

## Azure Key Vault Integration

### Overview

**Azure Key Vault** is a cloud service for securely storing and accessing secrets, keys, and certificates in Azure environments.

### Python/FastAPI Integration

**REQUIRED**: Azure Key Vault integration:

```python
# services/secrets/azure_keyvault_provider.py
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AzureKeyVaultProvider:
    """Azure Key Vault provider."""

    def __init__(self):
        vault_url = os.getenv('AZURE_KEYVAULT_URL')
        if not vault_url:
            raise ValueError("AZURE_KEYVAULT_URL environment variable required")

        # Use Managed Identity in production, DefaultAzureCredential for local
        if os.getenv('AZURE_USE_MANAGED_IDENTITY', 'false').lower() == 'true':
            credential = ManagedIdentityCredential()
        else:
            credential = DefaultAzureCredential()

        self.client = SecretClient(vault_url=vault_url, credential=credential)
        self.secret_prefix = os.getenv('AZURE_SECRET_PREFIX', 'application')

    async def initialize(self):
        """Initialize Azure Key Vault client."""
        try:
            # Verify connection by listing secrets
            list(self.client.list_properties_of_secrets(max_page_size=1))
            logger.info("Azure Key Vault provider initialized")
        except Exception as e:
            logger.error(f"Azure Key Vault initialization failed: {e}")
            raise

    async def get_secret(self, secret_name: str) -> Optional[str]:
        """Get secret from Azure Key Vault."""
        try:
            full_secret_name = f"{self.secret_prefix}-{secret_name}"
            secret = self.client.get_secret(full_secret_name)
            return secret.value
        except Exception as e:
            logger.error(f"Failed to get secret '{secret_name}' from Azure Key Vault: {e}")
            return None

    async def set_secret(self, secret_name: str, secret_value: str):
        """Set secret in Azure Key Vault."""
        try:
            full_secret_name = f"{self.secret_prefix}-{secret_name}"
            self.client.set_secret(full_secret_name, secret_value)
            logger.info(f"Secret '{secret_name}' updated in Azure Key Vault")
        except Exception as e:
            logger.error(f"Failed to set secret '{secret_name}' in Azure Key Vault: {e}")
            raise
```

### Node.js/TypeScript Integration

```typescript
// services/secrets/azureKeyVaultProvider.ts
import { SecretClient } from '@azure/keyvault-secrets';
import { DefaultAzureCredential, ManagedIdentityCredential } from '@azure/identity';

export class AzureKeyVaultProvider {
  private client: SecretClient;
  private secretPrefix: string;

  constructor() {
    const vaultUrl = process.env.AZURE_KEYVAULT_URL;
    if (!vaultUrl) {
      throw new Error('AZURE_KEYVAULT_URL environment variable required');
    }

    const useManagedIdentity =
      process.env.AZURE_USE_MANAGED_IDENTITY?.toLowerCase() === 'true';
    const credential = useManagedIdentity
      ? new ManagedIdentityCredential()
      : new DefaultAzureCredential();

    this.client = new SecretClient(vaultUrl, credential);
    this.secretPrefix = process.env.AZURE_SECRET_PREFIX || 'application';
  }

  async initialize(): Promise<void> {
    try {
      // Verify connection
      await this.client.listPropertiesOfSecrets().next();
      console.log('Azure Key Vault provider initialized');
    } catch (error) {
      console.error('Azure Key Vault initialization failed:', error);
      throw error;
    }
  }

  async getSecret(secretName: string): Promise<string | null> {
    try {
      const fullSecretName = `${this.secretPrefix}-${secretName}`;
      const secret = await this.client.getSecret(fullSecretName);
      return secret.value || null;
    } catch (error) {
      console.error(`Failed to get secret '${secretName}':`, error);
      return null;
    }
  }

  async setSecret(secretName: string, secretValue: string): Promise<void> {
    try {
      const fullSecretName = `${this.secretPrefix}-${secretName}`;
      await this.client.setSecret(fullSecretName, secretValue);
      console.log(`Secret '${secretName}' updated in Azure Key Vault`);
    } catch (error) {
      console.error(`Failed to set secret '${secretName}':`, error);
      throw error;
    }
  }
}
```

### Configuration

```bash
# Environment variables for Azure Key Vault
AZURE_KEYVAULT_URL=https://your-vault.vault.azure.net/
AZURE_SECRET_PREFIX=application
AZURE_USE_MANAGED_IDENTITY=true  # For production
# Or use DefaultAzureCredential (Azure CLI, VS Code, etc.)
```

---

## Google Secret Manager Integration

### Overview

**Google Secret Manager** is a secure and convenient storage system for API keys, passwords, certificates, and other sensitive data in GCP environments.

### Python/FastAPI Integration

**REQUIRED**: Google Secret Manager integration:

```python
# services/secrets/gcp_secrets_provider.py
from google.cloud import secretmanager
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class GCPSecretsProvider:
    """Google Secret Manager provider."""

    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.getenv('GCP_PROJECT_ID')
        self.secret_prefix = os.getenv('GCP_SECRET_PREFIX', 'application')

        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID environment variable required")

    async def initialize(self):
        """Initialize Google Secret Manager client."""
        try:
            # Verify connection by listing secrets
            parent = f"projects/{self.project_id}"
            list(self.client.list_secrets(request={"parent": parent, "page_size": 1}))
            logger.info("Google Secret Manager provider initialized")
        except Exception as e:
            logger.error(f"Google Secret Manager initialization failed: {e}")
            raise

    async def get_secret(self, secret_name: str) -> Optional[str]:
        """Get secret from Google Secret Manager."""
        try:
            full_secret_name = f"{self.secret_prefix}-{secret_name}"
            name = f"projects/{self.project_id}/secrets/{full_secret_name}/versions/latest"

            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode('UTF-8')
        except Exception as e:
            logger.error(f"Failed to get secret '{secret_name}' from Google Secret Manager: {e}")
            return None

    async def set_secret(self, secret_name: str, secret_value: str):
        """Set secret in Google Secret Manager."""
        try:
            full_secret_name = f"{self.secret_prefix}-{secret_name}"
            parent = f"projects/{self.project_id}"

            # Check if secret exists
            try:
                secret_path = f"{parent}/secrets/{full_secret_name}"
                self.client.get_secret(request={"name": secret_path})
            except Exception:
                # Create new secret
                self.client.create_secret(
                    request={
                        "parent": parent,
                        "secret_id": full_secret_name,
                        "secret": {"replication": {"automatic": {}}},
                    }
                )

            # Add new version
            self.client.add_secret_version(
                request={
                    "parent": f"{parent}/secrets/{full_secret_name}",
                    "payload": {"data": secret_value.encode('UTF-8')},
                }
            )

            logger.info(f"Secret '{secret_name}' updated in Google Secret Manager")
        except Exception as e:
            logger.error(f"Failed to set secret '{secret_name}' in Google Secret Manager: {e}")
            raise
```

### Node.js/TypeScript Integration

```typescript
// services/secrets/gcpSecretsProvider.ts
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

export class GCPSecretsProvider {
  private client: SecretManagerServiceClient;
  private projectId: string;
  private secretPrefix: string;

  constructor() {
    this.client = new SecretManagerServiceClient();
    this.projectId = process.env.GCP_PROJECT_ID || '';
    this.secretPrefix = process.env.GCP_SECRET_PREFIX || 'application';

    if (!this.projectId) {
      throw new Error('GCP_PROJECT_ID environment variable required');
    }
  }

  async initialize(): Promise<void> {
    try {
      // Verify connection
      const [secrets] = await this.client.listSecrets({
        parent: `projects/${this.projectId}`,
        pageSize: 1,
      });
      console.log('Google Secret Manager provider initialized');
    } catch (error) {
      console.error('Google Secret Manager initialization failed:', error);
      throw error;
    }
  }

  async getSecret(secretName: string): Promise<string | null> {
    try {
      const fullSecretName = `${this.secretPrefix}-${secretName}`;
      const name = `projects/${this.projectId}/secrets/${fullSecretName}/versions/latest`;

      const [version] = await this.client.accessSecretVersion({ name });
      return version.payload?.data?.toString() || null;
    } catch (error) {
      console.error(`Failed to get secret '${secretName}':`, error);
      return null;
    }
  }

  async setSecret(secretName: string, secretValue: string): Promise<void> {
    try {
      const fullSecretName = `${this.secretPrefix}-${secretName}`;
      const parent = `projects/${this.projectId}`;

      try {
        await this.client.getSecret({
          name: `${parent}/secrets/${fullSecretName}`,
        });
      } catch (error: any) {
        if (error.code === 5) {
          // Secret doesn't exist, create it
          await this.client.createSecret({
            parent,
            secretId: fullSecretName,
            secret: {
              replication: {
                automatic: {},
              },
            },
          });
        } else {
          throw error;
        }
      }

      // Add new version
      await this.client.addSecretVersion({
        parent: `${parent}/secrets/${fullSecretName}`,
        payload: {
          data: Buffer.from(secretValue, 'utf-8'),
        },
      });

      console.log(`Secret '${secretName}' updated in Google Secret Manager`);
    } catch (error) {
      console.error(`Failed to set secret '${secretName}':`, error);
      throw error;
    }
  }
}
```

### Configuration

```bash
# Environment variables for Google Secret Manager
GCP_PROJECT_ID=your-project-id
GCP_SECRET_PREFIX=application
# Use Application Default Credentials (ADC) or service account key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

---

## Kubernetes Secrets Integration

### Overview

**Kubernetes Secrets** are native Kubernetes resources for storing sensitive information like passwords, OAuth tokens, and SSH keys.

### Secret Definition

**REQUIRED**: Kubernetes Secret YAML:

```yaml
# kubernetes/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: application-secrets
  namespace: default
type: Opaque
stringData:
  admin-username: admin
  admin-password: CHANGE_ME
  database-password: CHANGE_ME
  cache-password: CHANGE_ME
```

### Deployment Integration

**REQUIRED**: Reference secrets in deployment:

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: application
spec:
  template:
    spec:
      containers:
      - name: api
        image: application:latest
        env:
        - name: ADMIN_USERNAME
          valueFrom:
            secretKeyRef:
              name: application-secrets
              key: admin-username
        - name: ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: application-secrets
              key: admin-password
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: application-secrets
              key: database-password
        # Or mount as volume
        volumeMounts:
        - name: secrets
          mountPath: /run/secrets
          readOnly: true
      volumes:
      - name: secrets
        secret:
          secretName: application-secrets
```

### Python/FastAPI Integration

**REQUIRED**: Read secrets from mounted volume or environment:

```python
# config/credentials.py
import os
from pathlib import Path

def get_secret_from_kubernetes(secret_name: str) -> Optional[str]:
    """
    Get secret from Kubernetes (mounted as file or environment variable).

    Priority:
    1. Mounted secret file (/run/secrets/{secret_name})
    2. Environment variable (from secretKeyRef)
    """
    # Try mounted secret file first
    secret_file = Path(f"/run/secrets/{secret_name}")
    if secret_file.exists():
        return secret_file.read_text().strip()

    # Fall back to environment variable
    env_key = secret_name.upper().replace("-", "_")
    return os.getenv(env_key)
```

---

## Docker Secrets Integration

### Overview

**Docker Secrets** are encrypted at rest and in transit, and are only accessible to services that have been granted explicit access.

### Docker Compose Configuration

**REQUIRED**: Docker Secrets setup:

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    image: application:latest
    secrets:
      - admin_password
      - database_password
    environment:
      - ADMIN_PASSWORD_FILE=/run/secrets/admin_password
      - DATABASE_PASSWORD_FILE=/run/secrets/database_password

secrets:
  admin_password:
    external: true
  database_password:
    external: true
```

### Create Secrets

```bash
# Create Docker secrets
echo "secure_password" | docker secret create admin_password -
echo "secure_db_password" | docker secret create database_password -
```

### Python/FastAPI Integration

**REQUIRED**: Read secrets from mounted files:

```python
# config/credentials.py
from pathlib import Path

def get_secret_from_docker(secret_name: str) -> Optional[str]:
    """Get secret from Docker secrets (mounted at /run/secrets/)."""
    secret_file = Path(f"/run/secrets/{secret_name}")
    if secret_file.exists():
        return secret_file.read_text().strip()
    return None
```

---

## Unified Integration Pattern

### Abstract Provider Interface

**REQUIRED**: Unified interface for all providers:

```python
# services/secrets/base_provider.py
from abc import ABC, abstractmethod
from typing import Optional

class ISecretsProvider(ABC):
    """Abstract interface for secrets providers."""

    @abstractmethod
    async def initialize(self):
        """Initialize the secrets provider."""
        pass

    @abstractmethod
    async def get_secret(self, secret_name: str) -> Optional[str]:
        """Get secret from provider."""
        pass

    @abstractmethod
    async def set_secret(self, secret_name: str, secret_value: str):
        """Set secret in provider."""
        pass
```

### Provider Factory

**REQUIRED**: Factory pattern for provider selection:

```python
# services/secrets/provider_factory.py
from typing import Optional
import os

class SecretsProviderFactory:
    """Factory for creating secrets providers."""

    @staticmethod
    def create_provider() -> Optional[ISecretsProvider]:
        """Create appropriate secrets provider based on environment."""
        environment = os.getenv("ENVIRONMENT", "development")
        secrets_backend = os.getenv("SECRETS_BACKEND", "").lower()

        # Production: Use external secrets manager
        if environment == "production":
            if secrets_backend == "vault":
                from services.secrets.vault_provider import VaultProvider
                return VaultProvider()
            elif secrets_backend == "aws":
                from services.secrets.aws_secrets_provider import AWSSecretsProvider
                return AWSSecretsProvider()
            elif secrets_backend == "azure":
                from services.secrets.azure_keyvault_provider import AzureKeyVaultProvider
                return AzureKeyVaultProvider()
            elif secrets_backend == "gcp":
                from services.secrets.gcp_secrets_provider import GCPSecretsProvider
                return GCPSecretsProvider()
            elif secrets_backend == "kubernetes":
                # Kubernetes secrets handled via environment variables
                return None
            elif secrets_backend == "docker":
                # Docker secrets handled via mounted files
                return None

        # Development: Use local secrets manager or environment variables
        return None
```

### Central Credential Function with External Support

**REQUIRED**: Updated credential function with external provider:

```python
# config/credentials.py

async def get_credential_with_external(credential_name: str) -> str:
    """
    Get credential with external secrets manager support.

    Priority order (highest to lowest):
    1. External Secrets Manager (HashiCorp Vault, AWS, Azure, GCP)
    2. Kubernetes Secrets (mounted files or environment)
    3. Docker Secrets (mounted files)
    4. Environment Variables
    5. Encrypted Local Storage
    6. Validated Config
    7. Development Defaults (ONLY for dev)
    """
    environment = os.getenv("ENVIRONMENT", "development")

    # Priority 1: External Secrets Manager (production)
    if environment == "production":
        provider = SecretsProviderFactory.create_provider()
        if provider:
            await provider.initialize()
            secret = await provider.get_secret(credential_name)
            if secret:
                return secret

    # Priority 2: Kubernetes Secrets
    k8s_secret = get_secret_from_kubernetes(credential_name)
    if k8s_secret:
        return k8s_secret

    # Priority 3: Docker Secrets
    docker_secret = get_secret_from_docker(credential_name)
    if docker_secret:
        return docker_secret

    # Priority 4-7: Continue with existing priority chain...
    # (Environment variables, local storage, config, defaults)

    raise ValueError(f"Credential '{credential_name}' not found")
```

---

## Credential Rotation with External Systems

### Automatic Rotation

**RECOMMENDED**: Leverage external secrets manager rotation:

#### AWS Secrets Manager Rotation

```python
# AWS Secrets Manager supports automatic rotation via Lambda
# Configure rotation in AWS Console or via CloudFormation

# Application code handles rotation gracefully
async def get_secret_with_rotation(secret_name: str) -> str:
    """Get secret, handling rotation automatically."""
    provider = AWSSecretsProvider()
    await provider.initialize()

    # AWS Secrets Manager automatically rotates and updates version
    secret = await provider.get_secret(secret_name)
    return secret
```

#### HashiCorp Vault Dynamic Secrets

```python
# Vault can generate dynamic credentials that auto-rotate
async def get_dynamic_database_credentials():
    """Get dynamically generated database credentials from Vault."""
    vault_client = VaultProvider()
    await vault_client.initialize()

    # Request dynamic credentials
    response = vault_client.client.secrets.database.generate_credentials(
        name="database-role",
        mount_point="database"
    )

    return {
        "username": response.data["username"],
        "password": response.data["password"]
    }
```

### Rotation Workflow

```bash
# 1. Configure automatic rotation in secrets manager
# 2. Application automatically uses new credentials
# 3. Old credentials remain valid during grace period
# 4. Secrets manager revokes old credentials after grace period
```

---

## Audit Logging & Monitoring

### External Secrets Manager Audit Logs

**REQUIRED**: Leverage provider audit logs:

#### HashiCorp Vault Audit Logs

```python
# Vault automatically logs all secret access
# Enable audit devices in Vault configuration
# Application should also log credential access

async def get_secret_with_audit(secret_name: str) -> str:
    """Get secret with audit logging."""
    logger.info(
        "Secret access requested",
        extra={
            "secret_name": secret_name,
            "source": "vault",
            "timestamp": datetime.now().isoformat()
        }
    )

    secret = await vault_provider.get_secret(secret_name)

    logger.info(
        "Secret accessed",
        extra={
            "secret_name": secret_name,
            "source": "vault",
            "success": secret is not None
        }
    )

    return secret
```

#### AWS CloudTrail Integration

```python
# AWS Secrets Manager access is automatically logged to CloudTrail
# Application should also log for correlation

async def get_secret_with_cloudtrail(secret_name: str) -> str:
    """Get secret (CloudTrail logs automatically)."""
    # CloudTrail logs: GetSecretValue API call
    # Application logs: For application-level correlation
    logger.info(f"Accessing secret '{secret_name}' from AWS Secrets Manager")
    return await aws_provider.get_secret(secret_name)
```

---

## Production Deployment

### Deployment Checklist

**REQUIRED**: Production deployment steps:

- [ ] Choose appropriate secrets manager (AWS/Azure/GCP/Vault)
- [ ] Configure authentication (IAM roles, service accounts, tokens)
- [ ] Set up secret naming conventions
- [ ] Configure access policies (least privilege)
- [ ] Enable audit logging
- [ ] Set up credential rotation (if supported)
- [ ] Test failover and fallback strategies
- [ ] Document secret locations and access patterns
- [ ] Set up monitoring and alerting
- [ ] Create runbooks for secret management

### Environment Configuration

```bash
# Production environment variables
ENVIRONMENT=production
SECRETS_BACKEND=aws  # or vault, azure, gcp

# AWS Secrets Manager
AWS_REGION=us-east-1
AWS_SECRET_PREFIX=application/production

# HashiCorp Vault
VAULT_ADDR=https://vault.example.com:8200
VAULT_SECRET_PATH=secret/data/application/production

# Azure Key Vault
AZURE_KEYVAULT_URL=https://vault.vault.azure.net/
AZURE_USE_MANAGED_IDENTITY=true

# Google Secret Manager
GCP_PROJECT_ID=production-project
GCP_SECRET_PREFIX=application-production
```

---

## Security Best Practices

### Authentication

**REQUIRED**: Secure authentication:

1. **Use Managed Identities**: Prefer IAM roles, managed identities, service accounts
2. **Rotate Credentials**: Regularly rotate authentication credentials
3. **Least Privilege**: Minimum necessary permissions
4. **No Hardcoded Tokens**: Never hardcode vault tokens or keys

### Access Control

**REQUIRED**: Proper access control:

1. **Policy-Based Access**: Use policies (Vault), IAM (AWS), RBAC (Azure/GCP)
2. **Secret-Level Permissions**: Different permissions for different secrets
3. **Time-Limited Access**: Use temporary credentials when possible
4. **Audit Access**: Log all access attempts

### Secret Management

**REQUIRED**: Secure secret handling:

1. **Encryption in Transit**: Always use TLS/HTTPS
2. **Encryption at Rest**: Secrets manager handles this
3. **No Logging**: Never log secret values
4. **Secure Memory**: Clear secrets from memory when done

---

## Summary

### Key Takeaways

1. **Production Requirement**: External secrets managers are REQUIRED for production
2. **Provider Selection**: Choose based on cloud provider and requirements
3. **Unified Interface**: Use abstract provider interface for flexibility
4. **Automatic Rotation**: Leverage provider rotation capabilities
5. **Audit Everything**: All secret access logged and monitored
6. **Fail Secure**: Proper fallback strategies
7. **Security First**: Authentication, access control, encryption

### Implementation Checklist

- [ ] Select appropriate secrets manager
- [ ] Implement provider interface
- [ ] Configure authentication
- [ ] Set up access policies
- [ ] Enable audit logging
- [ ] Configure credential rotation
- [ ] Test failover scenarios
- [ ] Document secret locations
- [ ] Set up monitoring
- [ ] Create runbooks

### Related Documentation

- [Secrets Management: Local & Development Best Practices](./secrets-management-local-development-best-practices-2025.md)

---

**Version**: v1.0.0
**Last Updated**: 2025-11-18
