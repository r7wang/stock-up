## Production
Terraform is used to automate deployment to the cloud provider. It keeps track of the current deployment state and what
must be done to achieve the desired state.

### Install Terraform
Installation can be done manually by downloading the binary or using Homebrew. Ensure that it's located within your
_PATH_ environment variable.
```bash
brew install terraform
```

### Select Deployment Type
The following deployment types are supported.
 * Google Compute Engine
 * Google Kubernetes Engine

For a more in-depth analysis on the advantages and disadvantages, see the [architecture notes](/doc/architecture/cloud/deployment-types).

#### Google Compute Engine
Make sure that you have the following files in `terraform/gce`.
 * [credentials.json](#credentialsjson)
 * [terraform.tfvars](#terraformtfvars)
 * [secrets.auto.tfvars](#secretsautotfvars)
 * [default-cert.pem](#default-certpem)
 * [default-key.pem](#default-keypem)

From `terraform/gce`, run the following commands.
```bash
terraform init
terraform apply
```

#### Google Kubernetes Engine
The GKE cluster must first be created before initializing the Kubernetes resources.

Make sure that you have the following files in `terraform/gke-cluster`.
 * [credentials.json](#credentialsjson)
 * [terraform.tfvars](#terraformtfvars)

From `terraform/gke-cluster`, run the following commands.
```bash
terraform init
terraform apply
```

Make sure that the cluster configuration has been downloaded.
```bash
# Verify that the cluster configuration exists. The command below outputs the following:
#   CURRENT   NAME    CLUSTER                 AUTHINFO                NAMESPACE
#   *         stock   gke_XXX_stock-cluster   gke_XXX_stock-cluster   prod
kubectl config get-contexts

# Download the cluster configuration, if it doesn't yet exist.
gcloud container clusters get-credentials stock-cluster
```

Make sure that you are currently pointing to the correct context.
```bash
# Check the current context.
kubectx

# Set the context, if not currently using the correct one.
kubectx <context-name>
``` 

Make sure that you have the following files in `terraform/gke`.
 * [terraform.tfvars](#terraformtfvars)
 * [secrets.auto.tfvars](#secretsautotfvars)
 * [default-cert.pem](#default-certpem)
 * [default-key.pem](#default-keypem)

From `terraform/gke`, run the following commands.
```bash
terraform init
terraform apply
```
 
### File Formats
#### credentials.json
Before running any `terraform` commands, a service account must be created. Upon creation, the file will be
automatically downloaded and saved as `credentials.json`. This file must be kept safe.

#### terraform.tfvars
```hcl-terraform
project          = "..."  # GCP project identifier
credentials_file = "credentials.json"
```

#### secrets.auto.tfvars
```hcl-terraform
grafana_password  = "..."  # administrative password for Grafana
influxdb_password = "..."  # administrative password for InfluxDB
quote_api_token   = "..."  # API token to access stock quotes for finnhub.io
```

#### default-cert.pem
TLS certificate in PEM format.

#### default-key.pem
TLS private key in PEM format.
