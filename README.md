# Jaeger for distributed tracing in Kubernetes

## Structure

```sh
.
├── README.md
├── deploy
│   ├── backend
│   │   ├── deployment.yaml
│   │   ├── kustomization.yaml
│   │   └── service.yaml
│   ├── frontend
│   │   ├── deployment.yaml
│   │   └── kustomization.yaml
│   └── kustomization.yaml
└── src
    ├── backend
    │   ├── Dockerfile
    │   └── main.py
    └── frontend
        ├── Dockerfile
        └── main.py
```

## Prerequisites
- minikube
- kustomize

## Step by step

### Install Jaeger to Kubernetes cluster

Operations

- Cluster scope
  - `demo` namespace
  - custom resource definition (CRD)
- `demo` namespace scope
  - service account
  - role
  - role binding
  - Jaeger operator (custom resource: `Jaeger`)

```sh
kubectl create namespace demo
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.29.0/config/crd/bases/jaegertracing.io_jaegers.yaml
kubectl create -n demo -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.29.0/config/rbac/service_account.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.29.0/config/rbac/role.yaml
kubectl apply -f ./deploy/cluster/role_binding.yaml
# kubectl create -n demo -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.29.0/examples/simplest.yaml
kubectl create -n demo -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.29.0/examples/operator-with-tracing.yaml
```

Set default namespace
```sh
kubectl config set-context --current --namespace=demo
```

**`jaeger-operator` for a specific namespace**

### Build Docker images for applications

There are two versions put in separate branches. Switch to corresponding branch to build target version of the applications.
- `0.1`: branch `release/0.1`
  - `frontend` and `backend` applications are grouped into 1 service (original idea)
- `0.2`: branch `release/0.2`
  - `frontend` and `backend` applications are logged as two different services
  - Support request latency breakdown demonstration

Change local Docker image repository to minikube's one

```sh
eval $(minikube -p minikube docker-env)
```

Set version

```sh
export COUNTER_VERSION="$(cat ./version)"
```

Backend

```sh
docker build src/backend -t counter-backend:${COUNTER_VERSION} --no-cache
```

Frontend

```sh
docker build src/frontend -t counter-frontend:${COUNTER_VERSION} --no-cache
```

### Deploy applications
```
kustomize build deploy/ | kubectl -n demo apply -f -
```

### Checks
Port forwarding for Jaeger dashboard's port

```sh

```

Port forwarding for frontend application (to call as a client)

```sh

```
