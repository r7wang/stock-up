## Secrets
Sensitive configuration exists in the following forms.
 * API tokens for accessing external services
 * user credentials for accessing internal services
 * private keys used for generating TLS certificates

### Best Practices
 * Keep all secrets out of your repositories and repository history by adding secret files to `.gitignore` and making
   use of variables within deployment tools.
 * Regenerate any externally exposed secrets.
 * Consider storing secrets within [secret managers](https://cloud.google.com/secret-manager/docs).

### docker-compose
When deploying locally, use a `.secrets` file to store sensitive configuration.

```bash
SERVICE_PASSWORD=thepassword
```

### Terraform
When deploying to production, use a `secrets.auto.tfvars` to store sensitive configuration.

```bash
service_password = "thepassword"
```
