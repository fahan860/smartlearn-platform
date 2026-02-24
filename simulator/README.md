# Smart Learning Platform - Data Generator

## Phase 1: Data Generation & Population

Ce module génère des données synthétiques réalistes pour entraîner les modèles ML et tester la plateforme.

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Utilisation](#utilisation)
6. [Schémas de Données](#schémas-de-données)
7. [Processus de Génération](#processus-de-génération)
8. [Validation](#validation)
9. [Dépannage](#dépannage)

---

## 🎯 Vue d'ensemble

### Objectifs
- Générer **1200+ utilisateurs** avec profils réalistes
- Créer **150+ cours** diversifiés (6 catégories, 3 niveaux)
- Produire **15000+ interactions** (views, enrolls, progress, completions)
- Fournir des données prêtes pour l'import MongoDB et l'analyse Spark

### Caractéristiques
- ✅ **Données réalistes**: Utilise Faker pour noms, emails, dates
- ✅ **Distribution configurable**: Paramètres YAML pour contrôle fin
- ✅ **Reproductibilité**: Seed aléatoire pour résultats cohérents
- ✅ **Formats multiples**: Export JSON (MongoDB) et CSV (Spark/Analytics)
- ✅ **Métadonnées riches**: Tags, ratings, prerequisites, outcomes
- ✅ **Progression réaliste**: Interactions suivent un parcours logique

---

## 🏗️ Architecture

```
simulator/
├── config/
│   └── config.yaml           # Configuration de génération
├── src/
│   └── data_generator.py     # Générateur principal
├── scripts/
│   └── import_to_mongodb.py  # Script d'import MongoDB
├── requirements.txt          # Dépendances Python
└── README.md                 # Cette documentation

data/
├── raw/
│   ├── users/               # Données utilisateurs générées
│   ├── courses/             # Données cours générées
│   └── interactions/        # Données interactions générées
├── processed/               # (Phase 2: Spark ETL)
└── output/                  # (Phase 3: Recommendations)
```

---

## 🚀 Installation

### Prérequis
- Python 3.8+
- MongoDB 4.4+ (local ou Atlas)
- pip (gestionnaire de paquets Python)

### Étapes

1. **Installer les dépendances Python**
   ```bash
   cd simulator
   pip install -r requirements.txt
   ```

2. **Vérifier l'installation**
   ```bash
   python -c "import faker, pandas, pymongo; print('✓ All dependencies installed')"
   ```

3. **Configurer MongoDB**
   - Local: `mongod --dbpath ./data/mongodb`
   - Atlas: Obtenir l'URI de connexion

---

## ⚙️ Configuration

### Fichier: `simulator/config/config.yaml`

#### Paramètres Principaux

```yaml
generation:
  num_users: 1200          # Nombre d'utilisateurs
  num_courses: 150         # Nombre de cours
  num_interactions: 15000  # Nombre d'interactions
  
  # Distribution des niveaux utilisateurs
  user_types:
    beginner: 0.40         # 40% débutants
    intermediate: 0.35     # 35% intermédiaires
    advanced: 0.25         # 25% avancés
  
  # Distribution des niveaux de cours
  course_levels:
    beginner: 0.45         # 45% débutant
    intermediate: 0.35     # 35% intermédiaire
    advanced: 0.20         # 20% avancé
```

#### Catégories de Cours

6 catégories avec poids relatifs:
- **Programming** (25%): Python, JavaScript, Java, C++, Go, Rust, TypeScript
- **Data Science** (20%): ML, Deep Learning, Data Analysis, Statistics
- **Web Development** (20%): React, Angular, Vue.js, Node.js, REST APIs
- **Cloud & DevOps** (15%): AWS, Azure, Docker, Kubernetes, CI/CD
- **Mobile Development** (10%): React Native, Flutter, iOS, Android
- **Cybersecurity** (10%): Network Security, Ethical Hacking, Cryptography

#### Patterns d'Interaction

```yaml
interaction_weights:
  view: 1.0       # Tous les utilisateurs voient des cours
  enroll: 0.3     # 30% des vues → inscription
  progress: 0.7   # 70% des inscrits → progression
  complete: 0.4   # 40% des progressions → complétion
```

---

## 📖 Utilisation

### 1. Générer les Données

**Commande de base:**
```bash
python simulator/src/data_generator.py
```

**Sortie attendue:**
```
======================================================================
Smart Learning Platform - Data Generator
Phase 1: Synthetic Data Generation
======================================================================

Generating 1200 users...
Creating users: 100%|████████████████████| 1200/1200 [00:05<00:00, 233.45it/s]
✓ Generated 1200 users

Generating 150 courses...
Creating courses: 100%|███████████████████| 150/150 [00:02<00:00, 67.23it/s]
✓ Generated 150 courses

Generating 15000 interactions...
Creating interactions: 100%|████████| 15000/15000 [00:08<00:00, 1765.43it/s]
✓ Generated 15000 interactions

Saving generated data...
  Saved: data/raw/users/users_20260126_143022.json
  Saved: data/raw/users/users_20260126_143022.csv
  Saved: data/raw/courses/courses_20260126_143022.json
  Saved: data/raw/courses/courses_20260126_143022.csv
  Saved: data/raw/interactions/interactions_20260126_143022.json
  Saved: data/raw/interactions/interactions_20260126_143022.csv
  Saved summary: data/generation_summary_20260126_143022.json
✓ Data saved successfully to data/

======================================================================
✓ Data generation complete!
======================================================================

Generated:
  • 1200 users
  • 150 courses
  • 15000 interactions

Next steps:
  1. Review generated data in data/raw/
  2. Run import script: python simulator/scripts/import_to_mongodb.py
  3. Verify data in MongoDB
```

### 2. Importer dans MongoDB

**Commande de base:**
```bash
python simulator/scripts/import_to_mongodb.py
```

**Avec options:**
```bash
# Nettoyer les collections existantes avant import
python simulator/scripts/import_to_mongodb.py --clear

# Spécifier URI MongoDB personnalisé
python simulator/scripts/import_to_mongodb.py --db-uri "mongodb://user:pass@host:27017"

# Utiliser une base de données différente
python simulator/scripts/import_to_mongodb.py --db-name "my_learning_platform"

# Toutes options combinées
python simulator/scripts/import_to_mongodb.py \
  --clear \
  --db-uri "mongodb://localhost:27017" \
  --db-name "smart_learning" \
  --data-dir "data/raw"
```

**Sortie attendue:**
```
======================================================================
Smart Learning Platform - MongoDB Data Import
======================================================================

Locating data files...

Found data files:
  • users: users_20260126_143022.json
  • courses: courses_20260126_143022.json
  • interactions: interactions_20260126_143022.json

Loading data files...
  ✓ Loaded 1200 records from users_20260126_143022.json
  ✓ Loaded 150 records from courses_20260126_143022.json
  ✓ Loaded 15000 records from interactions_20260126_143022.json

Connecting to MongoDB: mongodb://localhost:27017
✓ Connected to database: smart_learning

Clearing existing collections...
  • Deleted 0 documents from 'users'
  • Deleted 0 documents from 'courses'
  • Deleted 0 documents from 'interactions'

Importing data to MongoDB...
  ✓ Imported 1200 documents into 'users'
  ✓ Imported 150 documents into 'courses'
  ✓ Imported 15000 documents into 'interactions'

Creating indexes...
  ✓ Created index 'email_1' on 'users'
  ✓ Created index 'username_1' on 'users'
  ✓ Created index 'profile.level_1' on 'users'
  ✓ Created index 'category_1' on 'courses'
  ✓ Created index 'topic_1' on 'courses'
  ✓ Created index 'level_1' on 'courses'
  ✓ Created index 'status_1' on 'courses'
  ✓ Created index 'tags_1' on 'courses'
  ✓ Created index 'userId_1' on 'interactions'
  ✓ Created index 'courseId_1' on 'interactions'
  ✓ Created index 'type_1' on 'interactions'
  ✓ Created index 'timestamp_-1' on 'interactions'
  ✓ Created index 'userId_1_courseId_1' on 'interactions'

Verifying imported data...
  • users: 1200 documents
  • courses: 150 documents
  • interactions: 15000 documents

======================================================================
✓ Import completed successfully!
======================================================================

Database: smart_learning
Total documents: 16350

Next steps:
  1. Verify data in MongoDB: mongosh
  2. Start the backend server
  3. Test API endpoints
```

### 3. Vérifier les Données

**MongoDB Shell:**
```bash
mongosh

use smart_learning

# Compter les documents
db.users.countDocuments()      // 1200
db.courses.countDocuments()    // 150
db.interactions.countDocuments() // 15000

# Exemples de requêtes
db.users.findOne()
db.courses.find({ level: "beginner" }).limit(5)
db.interactions.find({ type: "complete" }).count()

# Statistiques par catégorie
db.courses.aggregate([
  { $group: { _id: "$category", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])

# Interactions par type
db.interactions.aggregate([
  { $group: { _id: "$type", count: { $sum: 1 } } }
])
```

---

## 📊 Schémas de Données

### User Schema

```json
{
  "_id": "user_00001",
  "username": "john_doe_123",
  "email": "john.doe@example.com",
  "password": "$2b$10$hashedpassword",
  "profile": {
    "firstName": "John",
    "lastName": "Doe",
    "level": "intermediate",
    "interests": ["Programming", "Data Science", "Web Development"],
    "learningGoals": ["Master advanced concepts", "Build portfolio projects"],
    "avatar": "https://i.pravatar.cc/150?u=1",
    "bio": "Passionate developer learning new technologies...",
    "location": "New York",
    "timezone": "EST"
  },
  "statistics": {
    "coursesEnrolled": 0,
    "coursesCompleted": 0,
    "totalLearningTime": 0,
    "currentStreak": 0,
    "longestStreak": 0
  },
  "preferences": {
    "emailNotifications": true,
    "weeklyDigest": false,
    "darkMode": true,
    "language": "en"
  },
  "createdAt": "2025-03-15T10:30:00.000Z",
  "updatedAt": "2026-01-20T14:22:00.000Z",
  "lastLoginAt": "2026-01-25T09:15:00.000Z"
}
```

### Course Schema

```json
{
  "_id": "course_00001",
  "title": "Complete Python Beginner Course",
  "slug": "complete-python-beginner-course",
  "description": "A comprehensive beginner-level course covering Python...",
  "category": "Programming",
  "topic": "Python",
  "level": "beginner",
  "instructor": {
    "name": "Dr. Sarah Johnson",
    "title": "Senior Software Engineer",
    "bio": "10+ years of experience in software development...",
    "avatar": "https://i.pravatar.cc/150?u=instructor1",
    "rating": 4.8
  },
  "content": {
    "duration": 3600,
    "modules": 8,
    "lessons": 45,
    "exercises": 30,
    "projects": 3,
    "language": "English",
    "subtitles": ["en", "es", "fr", "de"]
  },
  "pricing": {
    "type": "paid",
    "amount": 49.99,
    "currency": "USD"
  },
  "enrollment": {
    "studentsEnrolled": 2450,
    "maxStudents": null,
    "startDate": "2025-06-01T00:00:00.000Z",
    "endDate": null
  },
  "ratings": {
    "average": 4.6,
    "count": 320,
    "distribution": {
      "5": 200,
      "4": 80,
      "3": 30,
      "2": 8,
      "1": 2
    }
  },
  "tags": ["python", "programming", "beginner-friendly", "hands-on", "project-based"],
  "prerequisites": ["Basic computer skills", "Willingness to learn"],
  "outcomes": [
    "Master Python concepts",
    "Build real-world projects using Python",
    "Solve complex problems",
    "Apply best practices"
  ],
  "status": "active",
  "featured": true,
  "certificate": true,
  "createdAt": "2025-05-01T00:00:00.000Z",
  "updatedAt": "2026-01-10T00:00:00.000Z"
}
```

### Interaction Schema

```json
{
  "_id": "interaction_000001",
  "userId": "user_00042",
  "courseId": "course_00015",
  "type": "complete",
  "timestamp": "2026-01-15T14:30:00.000Z",
  "metadata": {
    "courseTitle": "Complete Python Beginner Course",
    "courseCategory": "Programming",
    "courseTopic": "Python"
  },
  "device": "desktop",
  "platform": "web",
  "sessionId": "session_123456",
  "completion": {
    "completedAt": "2026-01-15T14:30:00.000Z",
    "finalGrade": 92,
    "certificate": true,
    "certificateId": "cert_00000001",
    "timeSpent": 12600
  }
}
```

**Types d'Interaction:**
- `view`: Consultation d'un cours
- `enroll`: Inscription à un cours
- `progress`: Progression dans un cours
- `complete`: Complétion d'un cours

---

## 🔄 Processus de Génération

### Workflow Détaillé

```mermaid
graph TD
    A[Start] --> B[Load Config]
    B --> C[Set Random Seed]
    C --> D[Generate Users]
    D --> E[Generate Courses]
    E --> F[Generate Interactions]
    F --> G[Save JSON/CSV]
    G --> H[Generate Summary]
    H --> I[End]
```

### 1. Génération des Utilisateurs

**Algorithme:**
1. Pour chaque utilisateur (1-1200):
   - Déterminer le niveau (beginner/intermediate/advanced) selon distribution
   - Générer profil avec Faker (nom, email, location)
   - Assigner 2-5 intérêts aléatoires
   - Créer 1-3 objectifs d'apprentissage basés sur le niveau
   - Générer statistiques initiales (zéro pour nouvelles données)
   - Assigner préférences aléatoires
   - Créer timestamps (création, update, dernier login)

**Distribution:**
- 40% Beginners: ~480 utilisateurs
- 35% Intermediate: ~420 utilisateurs
- 25% Advanced: ~300 utilisateurs

### 2. Génération des Cours

**Algorithme:**
1. Pour chaque cours (1-150):
   - Sélectionner catégorie selon poids (Programming: 25%, Data Science: 20%, etc.)
   - Choisir topic dans la catégorie
   - Déterminer niveau selon distribution
   - Générer titre contextuel
   - Créer profil instructeur réaliste
   - Définir contenu (durée, modules, leçons, exercices)
   - Assigner pricing (free/paid/subscription)
   - Générer ratings avec distribution réaliste (skew vers 4-5 étoiles)
   - Créer tags, prérequis, outcomes
   - Définir statut (85% active, 10% draft, 5% archived)

**Distribution par Catégorie:**
- Programming: ~38 cours
- Data Science: ~30 cours
- Web Development: ~30 cours
- Cloud & DevOps: ~22 cours
- Mobile Development: ~15 cours
- Cybersecurity: ~15 cours

### 3. Génération des Interactions

**Algorithme:**
1. Pour chaque interaction (1-15000):
   - Sélectionner utilisateur aléatoire
   - Sélectionner cours actif aléatoire
   - Déterminer type selon progression réaliste:
     * 40% view (6000 interactions)
     * 20% enroll (3000 interactions)
     * 25% progress (3750 interactions)
     * 15% complete (2250 interactions)
   - Générer timestamp dans les 180 derniers jours
   - Créer metadata spécifique au type
   - Assigner device/platform aléatoire

**Progression Réaliste:**
- Un utilisateur peut voir plusieurs cours (view)
- Inscription (enroll) nécessite d'avoir vu le cours
- Progression (progress) suit l'inscription
- Complétion (complete) termine la progression

---

## ✅ Validation

### Checksums Attendus

Après génération avec `random_seed: 42`:

```yaml
Expected Counts:
  users: 1200
  courses: 150
  interactions: 15000

User Distribution:
  beginner: ~480 (40%)
  intermediate: ~420 (35%)
  advanced: ~300 (25%)

Course Distribution by Level:
  beginner: ~68 (45%)
  intermediate: ~52 (35%)
  advanced: ~30 (20%)

Course Distribution by Status:
  active: ~128 (85%)
  draft: ~15 (10%)
  archived: ~7 (5%)

Interaction Distribution:
  view: ~6000 (40%)
  enroll: ~3000 (20%)
  progress: ~3750 (25%)
  complete: ~2250 (15%)
```

### Tests de Validation

**1. Vérifier les comptes:**
```bash
python -c "
import json
print('Users:', len(json.load(open('data/raw/users/users_*.json'))))
print('Courses:', len(json.load(open('data/raw/courses/courses_*.json'))))
print('Interactions:', len(json.load(open('data/raw/interactions/interactions_*.json'))))
"
```

**2. Vérifier l'intégrité:**
```python
import json

# Charger les données
users = json.load(open('data/raw/users/users_latest.json'))
courses = json.load(open('data/raw/courses/courses_latest.json'))
interactions = json.load(open('data/raw/interactions/interactions_latest.json'))

# Vérifier les IDs uniques
assert len(set(u['_id'] for u in users)) == len(users)
assert len(set(c['_id'] for c in courses)) == len(courses)
assert len(set(i['_id'] for i in interactions)) == len(interactions)

# Vérifier les références
user_ids = set(u['_id'] for u in users)
course_ids = set(c['_id'] for c in courses)

for interaction in interactions:
    assert interaction['userId'] in user_ids, f"Invalid userId: {interaction['userId']}"
    assert interaction['courseId'] in course_ids, f"Invalid courseId: {interaction['courseId']}"

print("✓ All validations passed!")
```

**3. Vérifier MongoDB:**
```javascript
// Dans mongosh
use smart_learning

// Vérifier les comptes
db.users.countDocuments()
db.courses.countDocuments()
db.interactions.countDocuments()

// Vérifier l'intégrité référentielle
var orphanedInteractions = db.interactions.aggregate([
  {
    $lookup: {
      from: "users",
      localField: "userId",
      foreignField: "_id",
      as: "user"
    }
  },
  {
    $lookup: {
      from: "courses",
      localField: "courseId",
      foreignField: "_id",
      as: "course"
    }
  },
  {
    $match: {
      $or: [
        { user: { $size: 0 } },
        { course: { $size: 0 } }
      ]
    }
  },
  { $count: "orphaned" }
]).toArray()

print("Orphaned interactions:", orphanedInteractions.length > 0 ? orphanedInteractions[0].orphaned : 0)
```

---

## 🔧 Dépannage

### Problème: Import Error - Module Not Found

**Symptôme:**
```
ModuleNotFoundError: No module named 'faker'
```

**Solution:**
```bash
pip install -r simulator/requirements.txt
```

### Problème: MongoDB Connection Failed

**Symptôme:**
```
✗ Failed to connect to MongoDB: [Errno 111] Connection refused
```

**Solutions:**
1. Vérifier que MongoDB est démarré:
   ```bash
   # Windows
   net start MongoDB
   
   # Linux/Mac
   sudo systemctl start mongod
   ```

2. Vérifier le port:
   ```bash
   netstat -an | grep 27017
   ```

3. Utiliser URI explicite:
   ```bash
   python simulator/scripts/import_to_mongodb.py --db-uri "mongodb://127.0.0.1:27017"
   ```

### Problème: YAML Parse Error

**Symptôme:**
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Solution:**
- Vérifier l'indentation dans `config.yaml` (utiliser des espaces, pas des tabs)
- Valider le YAML: https://www.yamllint.com/

### Problème: Duplicate Key Error lors de l'import

**Symptôme:**
```
BulkWriteError: E11000 duplicate key error collection
```

**Solution:**
- Utiliser `--clear` pour nettoyer les collections:
  ```bash
  python simulator/scripts/import_to_mongodb.py --clear
  ```

### Problème: Insufficient Disk Space

**Symptôme:**
```
OSError: [Errno 28] No space left on device
```

**Solution:**
1. Vérifier l'espace disque:
   ```bash
   df -h
   ```

2. Réduire les quantités dans `config.yaml`:
   ```yaml
   generation:
     num_users: 500        # Réduit de 1200
     num_courses: 50       # Réduit de 150
     num_interactions: 5000 # Réduit de 15000
   ```

### Problème: Generation Takes Too Long

**Symptôme:**
Le script s'exécute pendant plus de 5 minutes

**Solutions:**
1. Vérifier les ressources système (CPU, RAM)
2. Réduire les quantités temporairement
3. Désactiver un format d'export:
   ```yaml
   output:
     formats:
       - "json"  # Retirer "csv" si non nécessaire
   ```

---

## 📈 Statistiques et Métriques

### Fichier Summary

Chaque génération crée un fichier `generation_summary_TIMESTAMP.json`:

```json
{
  "generation_timestamp": "2026-01-26T14:30:22.123456",
  "config": { ... },
  "statistics": {
    "users": {
      "total": 1200,
      "by_level": {
        "beginner": 480,
        "intermediate": 420,
        "advanced": 300
      }
    },
    "courses": {
      "total": 150,
      "by_category": {
        "Programming": 38,
        "Data Science": 30,
        "Web Development": 30,
        "Cloud & DevOps": 22,
        "Mobile Development": 15,
        "Cybersecurity": 15
      },
      "by_level": {
        "beginner": 68,
        "intermediate": 52,
        "advanced": 30
      },
      "by_status": {
        "active": 128,
        "draft": 15,
        "archived": 7
      }
    },
    "interactions": {
      "total": 15000,
      "by_type": {
        "view": 6000,
        "enroll": 3000,
        "progress": 3750,
        "complete": 2250
      }
    }
  }
}
```

---

## 🎓 Bonnes Pratiques

### 1. Configuration

- **Toujours utiliser un seed**: Pour reproductibilité dans les tests
- **Ajuster les quantités**: Selon capacité de l'environnement
- **Documenter les changements**: Noter les modifications de config

### 2. Génération

- **Backup avant regénération**: Sauvegarder les données existantes
- **Vérifier les timestamps**: S'assurer que les fichiers sont récents
- **Valider immédiatement**: Tester après chaque génération

### 3. Import

- **Utiliser --clear avec précaution**: Efface toutes les données existantes
- **Vérifier les indexes**: Les indexes améliorent les performances
- **Monitorer les logs**: Surveiller les erreurs pendant l'import

### 4. Production

- **Ne pas utiliser en production**: Ces données sont synthétiques
- **Séparer les environnements**: Dev, staging, production
- **Protéger les données réelles**: Ne jamais mélanger avec données synthétiques

---

## 🔗 Intégration avec les Autres Phases

### Phase 2: Spark ETL (À venir)
- Les CSV générés seront consommés par Spark
- Feature engineering sur les données brutes
- Agrégation pour ML (user_features, course_features)

### Phase 3: ML Models (À venir)
- Entraînement des modèles sur données agrégées
- Collaborative filtering (ALS)
- Content-based filtering
- Hybrid recommendations

### Phase 4: ML Service (À venir)
- API Flask consommant les modèles entraînés
- Serving des recommendations en temps réel
- A/B testing des algorithmes

---

## 📞 Support

Pour questions ou problèmes:
1. Consulter cette documentation
2. Vérifier les logs: `simulator/logs/data_generation.log`
3. Examiner le fichier summary pour statistiques
4. Valider la configuration YAML

---

## ✨ Prochaines Étapes

Une fois Phase 1 complétée:

1. ✅ **Données générées** (data/raw/)
2. ✅ **MongoDB populé** (users, courses, interactions)
3. ⏳ **Phase 2**: Configurer Spark pour ETL
4. ⏳ **Phase 3**: Développer feature engineering
5. ⏳ **Phase 4**: Entraîner modèles ML
6. ⏳ **Phase 5**: Déployer ML service

---

**Dernière mise à jour:** 26 janvier 2026  
**Version:** 1.0.0  
**Auteur:** Smart Learning Platform Team
