# 📊 Socium HR-Tech - MongoDB to Datadog Data Pipeline

> **Projet de candidature** - Data & Analytics Intern @ Socium  
> Transformation de données RH brutes en KPIs exploitables

[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green?logo=mongodb)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Datadog](https://img.shields.io/badge/Datadog-Metrics%20API-purple?logo=datadog)](https://www.datadoghq.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)

---

## 🎯 Contexte & Objectif

Ce projet démontre ma capacité à construire une **infrastructure de données complète** pour une HR-Tech, en transformant des millions de points de données MongoDB en indicateurs stratégiques visualisés sur Datadog.

### Les 5 Produits Socium couverts
- **JOB** - Recrutement & ATS (Applicant Tracking System)
- **DOC** - Gestion documentaire RH
- **PAYROLL** - Traitement de la paie
- **PERF** - Évaluations de performance
- **WORKFLOW** - Validation des processus RH

---

## 🏗️ Architecture Technique

```
┌─────────────────────────────────────────────────────────────────┐
│                     SOCIUM DATA PLATFORM                        │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
    │   MongoDB    │   →    │   Pipeline   │   →    │   Datadog    │
    │   (Source)   │        │   (Python)   │        │ (Dashboards) │
    └──────────────┘        └──────────────┘        └──────────────┘
         ↓                          ↓                       ↓
    Collections              Extract KPIs           Visualisation
    - companies              - Aggregations         - Time Series
    - employees              - Calculations         - Donut Charts
    - applications           - Tagging              - Bar Charts
    - payrolls                                      - Alerts
    - workflows
```

### Stack Technologique
- **Base de données** : MongoDB 7.0 (NoSQL orienté documents)
- **Orchestration** : Docker Compose (multi-conteneurs)
- **Backend** : Python 3.11 (Faker, PyMongo)
- **Observabilité** : Datadog Metrics API v2
- **Génération** : Pipeline automatisé de données synthétiques

---

## 📈 KPIs Implémentés

### 1. JOB - Recrutement
| Métrique | Description | Tag Exemple |
|----------|-------------|-------------|
| `socium.v10.job.applications.count` | Volume de candidatures quotidiennes | `granularity:day` |
| `socium.v10.job.funnel` | Conversion par statut | `status:hired` |
| `socium.v10.job.postings.by_title` | Postes ouverts par rôle | `title:Dev` |

**Visualisation** : Funnel de recrutement (applied → hired)

### 2. PAYROLL - Paie
| Métrique | Description | Tag Exemple |
|----------|-------------|-------------|
| `socium.v10.payroll.gross_salary` | Masse salariale brute | `period:2025-09` |
| `socium.v10.payroll.net_salary` | Masse salariale nette | `period:2025-09` |
| `socium.v10.payroll.bulletins.count` | Nombre de fiches de paie générées | `period:2025-09` |

**Visualisation** : Évolution mensuelle de la masse salariale

### 3. PERFORMANCE
| Métrique | Description |
|----------|-------------|
| `socium.v10.performance.avg_score` | Score moyen des évaluations (1-5) |
| `socium.v10.performance.reviews.count` | Nombre d'évaluations réalisées |

**Visualisation** : Score moyen et volume d'évaluations

### 4. WORKFLOWS
| Métrique | Description | Tag Exemple |
|----------|-------------|-------------|
| `socium.v10.workflows.count` | Volume par statut | `status:pending` |
| `socium.v10.workflows.pending` | Workflows en attente | - |

**Visualisation** : Distribution par statut (pending/approved/rejected)

### 5. DOCUMENTS
| Métrique | Description | Tag Exemple |
|----------|-------------|-------------|
| `socium.v10.documents.count` | Volume par statut | `status:signed` |
| `socium.v10.documents.expired` | Documents expirés | - |

### 6. SYSTEM
| Métrique | Description | Tag Exemple |
|----------|-------------|-------------|
| `socium.v10.system.collection.count` | Volumétrie MongoDB | `collection:employees` |

---

## 🚀 Démarrage Rapide

### Prérequis
- Docker & Docker Compose installés
- Compte Datadog (API Key + APP Key)

### 1. Configuration

```bash
# Cloner le repository
git clone https://github.com/Hamath-dieudonne/socium-hrtech-datadog-pipeline
cd HR Data Analytic

# Créer le fichier .env
cat > .env << 'EOF'
# MongoDB
MONGO_INITDB_ROOT_USERNAME=socium_admin
MONGO_INITDB_ROOT_PASSWORD=secure_password_here
MONGODB_URI=mongodb://socium_admin:secure_password_here@mongo:27017/socium?authSource=admin
MONGODB_DATABASE=socium

# Datadog
DATADOG_API_KEY=votre_api_key_ici
DATADOG_APP_KEY=votre_app_key_ici
DATADOG_SITE=datadoghq.com
EOF
```

### 2. Lancement

```bash
# Démarrer l'infrastructure
docker-compose up -d

# Vérifier les logs du générateur de données
docker logs socium_data_generator

# Lancer le pipeline de métriques
docker exec socium_metrics_agent python socium_datadog_pipeline.py
```

### 3. Résultats Attendus

```
💼 JOB KPIs
📄 DOCUMENT KPIs
💰 PAYROLL KPIs
⭐ PERFORMANCE KPIs
🔄 WORKFLOW KPIs
📊 SYSTEM KPIs
==================================================
✅ DONE in 2.34s
📤 Sent: 156
❌ Failed: 0
==================================================
```

---

## 📊 Dashboards Datadog

### Dashboard 1 : PERFORMANCE KPIs
![Performance Dashboard](./screenshots/Perf_kpis.png)

**Widgets clés** :
- 🌟 **Évaluations réalisées** : 780 (Query Value)
- 📊 **Score moyen** : 2.99/5 (Query Value)
- 📈 **Workflows par statut** : Répartition rejected/pending/approved (Bar Chart)
- 🥧 **Volume MongoDB** : 6.99k documents répartis (Donut Chart)

### Dashboard 2 : PAYROLL KPIs
![Payroll Dashboard](./screenshots/Payroll.png)

**Widgets clés** :
- 💰 **Masse salariale nette** : 386.9M XOF (Time Series)
- 📄 **Bulletins générés** : 746 (Time Series)
- 🎨 **Masse salariale brute par période** : TreeMap multi-périodes

### Dashboard 3 : JOB KPIs - Recrutement
![Job Dashboard](./screenshots/Job.png)

**Widgets clés** :
- 📋 **Documents RH par statut** : 439 pending, 422 draft (List)
- 📊 **Funnel de recrutement** : 66 hired → 42 applied (Bar Chart)
- 🥧 **Postes ouverts par rôle** : 36 postes répartis (Donut + Table)

---

## 🎯 Stratégie de Tagging

Les tags permettent un filtrage puissant et une analyse granulaire. Chaque métrique est enrichie avec :

### Tags Système (automatiques)
```python
tags = ["env:dev", "source:mongo", "app:socium"]
```

### Tags Métier (dynamiques)
```python
# Exemples par produit
"status:hired"              # JOB
"period:2025-09"            # PAYROLL
"collection:employees"      # SYSTEM
"type:Congé"                # WORKFLOW
```

### Utilisation dans Datadog
```
# Filtrer les candidatures "hired" uniquement
socium.v10.job.funnel{status:hired}

# Comparer les masses salariales par période
socium.v10.payroll.gross_salary by {period}

# Volumétrie par collection MongoDB
socium.v10.system.collection.count by {collection}
```


---

## 🎓 Compétences Démontrées

### Ingénierie de Données
- ✅ Extraction de KPIs complexes depuis MongoDB (pipelines d'agrégation)
- ✅ Transformation et normalisation de données temporelles
- ✅ Stratégie de tagging pour analyse multi-dimensionnelle

### Architecture & DevOps
- ✅ Containerisation Docker multi-services (MongoDB + Python)
- ✅ Healthchecks et orchestration Docker Compose
- ✅ Gestion de secrets et configuration (environnement variables)

### Observabilité & Monitoring
- ✅ Intégration Datadog Metrics API v2
- ✅ Conception de dashboards métier (Product-Specific)
- ✅ Time Series, Donut Charts, Bar Charts, TreeMaps

### Data Engineering
- ✅ Génération de données synthétiques réalistes (Faker)
- ✅ Modélisation NoSQL pour une plateforme HR-Tech
- ✅ Pipeline ETL (Extract, Transform, Load)

---

## 📂 Structure du Projet

```
HR Data Analytic/
├── docker-compose.yml              # Orchestration multi-conteneurs
├── .env                            # Configuration (API keys, MongoDB)
├── README.md                       # Documentation complète
│
├── mongo/
│   ├── socium_generator_v5.py      # Générateur de données synthétiques
│   └── requirements.txt            # Dépendances (faker, pymongo)
│
├── metrics-agent/
│   ├── Dockerfile                  # Image Python pour le pipeline
│   ├── socium_datadog_pipeline_v10.py  # Pipeline MongoDB → Datadog
│   └── requirements.txt            # Dépendances (datadog-api-client, pymongo)
│
└── screenshots/                    # Captures Datadog
    ├── Perf_kpis.png
    ├── Payroll.png
    └── Job.png
```

---

## 🔮 Évolutions Futures

### Phase 1 : Industrialisation
- [ ] Cron job automatique (toutes les heures)
- [ ] Alertes Datadog sur anomalies métier (baisse du flux de candidatures)
- [ ] Intégration CI/CD (GitHub Actions)

### Phase 2 : Enrichissement
- [ ] Dashboard "Executive" pour le C-Level
- [ ] Calcul de métriques dérivées (taux de conversion, délais moyens)
- [ ] Segmentation par client (multi-tenancy)

### Phase 3 : Scalabilité
- [ ] Migration vers MongoDB Atlas (cloud-native)
- [ ] Pipeline Apache Airflow pour orchestration complexe
- [ ] Intégration GCP BigQuery pour analytics avancés

---

## 👤 À Propos

**Candidat** : Hamath Dieudonne  
**Position ciblée** : Data & Analytics Intern @ Socium  
**Localisation** : Dakar, Sénégal  

### Pourquoi ce projet ?

> "J'ai conçu ce pipeline pour démontrer concrètement ma capacité à transformer des données brutes en insights stratégiques. Plutôt qu'un simple CV, ce repository illustre ma maîtrise de l'architecture data moderne : MongoDB, Python, Docker, et Datadog. Chaque ligne de code reflète ma compréhension des enjeux métier d'une HR-Tech et mon approche pragmatique de l'ingénierie de données."

### Contact
- 📧 Email : [dhamathdieudonne@gmail.com](mailto:dhamathdieudonne@gmail.com)
- 💼 LinkedIn : [linkedin.com/in/hamzo](https://www.linkedin.com/in/hamzo)
- 🐙 GitHub : [github.com/hamath-dieudonne](https://github.com/hamath-dieudonne)

---

## 📜 Licence

Ce projet est développé dans le cadre d'une candidature à un poste de Data & Analytics Intern chez Socium. Le code est mis à disposition à des fins de démonstration technique.

---

<div align="center">

**Construit avec ❤️ pour Socium HR-Tech**

[![MongoDB](https://img.shields.io/badge/MongoDB-green?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Datadog](https://img.shields.io/badge/Datadog-purple?style=for-the-badge&logo=datadog&logoColor=white)](https://www.datadoghq.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>
