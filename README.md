# 🚀 Flask API Deployment with Docker, Kubernetes & CI/CD

## 📌 Description

Ce projet démontre le déploiement d’une application **Flask** conteneurisée avec **Docker**, orchestrée avec **Kubernetes**, et automatisée via un pipeline **CI/CD avec GitHub Actions**.

L’objectif est de simuler un environnement réel de déploiement cloud, en appliquant les bonnes pratiques DevOps.

---

## 🧱 Architecture du projet

* 🐍 **Flask** → API backend
* 🐳 **Docker** → conteneurisation de l’application
* ☸️ **Kubernetes (Docker Desktop)** → orchestration des conteneurs
* 🔄 **GitHub Actions** → pipeline CI/CD
* 📦 **Docker Hub** → stockage des images

---

## ⚙️ Fonctionnalités

* Création d’une API Flask simple
* Dockerisation avec un `Dockerfile`
* Déploiement sur Kubernetes avec :

  * `Deployment` (gestion des pods)
  * `Service` (exposition via NodePort)
* Pipeline CI/CD :

  * Build automatique de l’image Docker
  * Push vers Docker Hub
* Gestion sécurisée des credentials avec GitHub Secrets

---

## 📁 Structure du projet

```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── .github/
    └── workflows/
        └── deploy.yml
```

---

## 🐳 Lancer le projet en local (Docker)

```bash
docker build -t app-ker .
docker run -p 5000:5000 app-ker
```

👉 Accès :

```
http://localhost:5000
```

---

## ☸️ Déploiement sur Kubernetes

### 1. Activer Kubernetes (Docker Desktop)

### 2. Appliquer les fichiers :

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 3. Vérifier :

```bash
kubectl get pods
kubectl get services
```

### 4. Accéder à l’application :

```
http://localhost:30007
```

---

## 🔐 Configuration CI/CD (GitHub)

Ajouter les secrets dans GitHub :

* `DOCKER_USERNAME`
* `DOCKER_PASSWORD`

---

## 🔄 Pipeline CI/CD

À chaque push sur GitHub :

1. Build de l’image Docker
2. Authentification Docker Hub
3. Push de l’image
4. (optionnel) Déploiement Kubernetes

---

## 🧠 Compétences démontrées

* Docker & conteneurisation
* Kubernetes (Deployment, Service)
* CI/CD avec GitHub Actions
* Gestion des secrets
* Architecture Cloud / DevOps

---

## 📌 Améliorations possibles

* Ajouter un **Ingress (URL propre)**
* Déployer sur **AWS EKS**
* Monitoring avec **Prometheus / Grafana**
* Gestion des environnements (dev / prod)

---

## 👨‍💻 Auteur

**Mamadou Sy**

---

## ⭐ Conclusion

Ce projet illustre un workflow complet DevOps, de la création d’une application à son déploiement automatisé dans un environnement Kubernetes.

---
