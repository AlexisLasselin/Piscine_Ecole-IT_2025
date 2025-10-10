Parfait 💡, je vais te rédiger un **README complet et structuré** qui explique ton projet, comment lancer en local et en prod, et le rôle de chaque partie (frontend / backend / CI-CD). Tu pourras le mettre directement à la racine de ton repo GitHub.

---

# 🐳 Projet : Lang Interpreter IDE (Frontend + Backend en Docker)

## 📌 Description

Ce projet est une **application web composée de deux parties** :

* **Backend (FastAPI)** : interprète du langage `.pisc`, gère le parsing et l’exécution de code.
* **Frontend (React/Vite + Nginx)** : IDE web permettant d’éditer du code, de l’envoyer au backend et d’afficher les résultats.

L’ensemble est conteneurisé avec **Docker Compose**, et déployé automatiquement via **GitHub Actions (CI/CD)** sur une VM.

---

## ⚙️ Architecture

```
root/
│── backend/              # Code backend FastAPI (app, lexer, parser, interpreter)
│   ├── Dockerfile_back
│   ├── requirements.txt
│   └── tests/            # Tests Pytest
│
│── frontend/             # Code frontend React (Vite)
│   ├── Dockerfile_front
│   ├── package.json
│   └── src/
│
│── docker-compose.yml    # Décrit l’infrastructure (frontend + backend + réseau)
│── .github/workflows/
│   ├── ci.yml            # CI : tests automatiques (Pytest)
│   └── cd.yml            # CD : déploiement automatique sur la VM
```

---

## 🚀 Lancement en local

### 1. Prérequis

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/)

### 2. Lancer les conteneurs

À la racine du projet :

```bash
docker compose up -d --build
```

* Frontend disponible sur : [http://localhost](http://localhost)
* Backend exposé uniquement dans le réseau Docker (appelé via `http://interpreter:5000` depuis Nginx).

### 3. Arrêter les conteneurs

```bash
docker compose down
```

---

## 🌐 Déploiement en production (VM)

1. La VM exécute un **GitHub Actions Runner self-hosted**.
2. Sur un `push` vers `main`, la pipeline **CD** (`cd.yml`) :

   * clone le repo,
   * build les images (`frontend` + `backend`),
   * lance `docker compose up -d --build`.
3. Le site est accessible via `http://IP_VM/`.

   * Frontend servi par Nginx.
   * Backend joignable uniquement via `/api/` (proxy Nginx).

---

## 🔧 Détails techniques

### Backend (FastAPI)

* Port interne : `5000`
* Routes principales :

  * `GET /health` → test de disponibilité
  * `POST /parse-json` → analyse du code envoyé en JSON
  * `POST /parse` → analyse d’un fichier `.pisc`
* Gère CORS (configuré pour autoriser l’accès depuis le frontend).

### Frontend (React + Nginx)

* Build multi-stage Docker :

  * Étape 1 → `npm run build` avec Node.js
  * Étape 2 → fichiers statiques servis par Nginx
* Proxy configuré (`nginx.conf`) :

  * `location /api/ { proxy_pass http://interpreter:5000; }`
* Ainsi, toutes les requêtes API passent par `http://IP_VM/api/...`.

---

## ✅ CI (tests automatiques)

Workflow : `.github/workflows/ci.yml`

* Exécuté sur **chaque push** et **pull request**.
* Teste avec **Python 3.12** et **3.13**.
* Installe les dépendances backend et exécute `pytest`.
* Résumé des résultats directement dans GitHub Actions.

---

## 🚀 CD (déploiement auto)

Workflow : `.github/workflows/cd.yml`

* Déclenché uniquement sur `push` vers `main`.
* Exécuté sur le runner **self-hosted** (VM).
* Étapes :

  1. `docker compose down`
  2. `docker compose up -d --build`
* Les services sont reconstruits et relancés automatiquement.

---

## 🧪 Lancer les tests manuellement

```bash
cd backend
pytest -v
```

---

## 📖 Exemple d’utilisation

1. Ouvrir le site sur `[la VM](http://195.15.242.242/)`. (la VM ne sera plus accessible d'ici ce weekend)
2. Écrire du code dans l’éditeur ou importer un fichier `.pisc` déjà fait (⚠️ bien suivre les instructions concernant la création de fichier dans [instructions.md](./docs/informations.md).
3. Cliquer sur **Exécuter** → envoie le code au backend (`/api/parse-json`).
4. Le terminal reverra alors:
   * la sortie du programme,
   * les erreurs éventuelles.
