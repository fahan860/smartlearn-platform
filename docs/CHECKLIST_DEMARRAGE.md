# ✅ SMARTLEARN - CHECKLIST DE DÉMARRAGE

## 🔧 AVANT DE DÉMARRER

### 1. Configurer les variables d'environnement

**Backend (`backend/.env`):**
```
# Vérifiez que le fichier existe et contient:
NODE_ENV=development
MONGODB_URI=mongodb://127.0.0.1:27017/learning
JWT_SECRET=dev-secret-key-change-in-production-12345678
PORT=4000
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=smartlearn
ML_SERVICE_URL=http://ml-service:8000
```

**Frontend (`frontend/.env`):**
```
VITE_API_BASE_URL=http://localhost:4000
```

### 2. Installer les dépendances

```bash
# Backend
cd backend
npm install

# Frontend
cd frontend
npm install
```

---

## 🚀 DÉMARRER LE PROJET

### Étape 1: MongoDB
```bash
# Option A: MongoDB local (déjà en cours?)
# Vérifiez que MongoDB écoute sur 127.0.0.1:27017

# Option B: MongoDB Atlas
# Mettez à jour MONGODB_URI dans backend/.env
```

### Étape 2: MySQL (Docker)
```bash
# Lancer le container MySQL
docker-compose up -d mysql

# Attendre que MySQL soit prêt (environ 30 secondes)
docker ps | grep mysql

# Importer le schéma
docker exec mysql-container mysql -u root -proot smartlearn < database/mysql/seed.sql
```

### Étape 3: Backend
```bash
cd backend
npm run dev
# ✅ Vous devriez voir:
# Connected to MongoDB
# Server running on port 4000
```

### Étape 4: Frontend
```bash
cd frontend
npm run dev
# ✅ Vous devriez voir:
# VITE v5.0.8 ready in XXX ms
# ➜  Local:   http://localhost:5173/
```

---

## 🧪 TESTER LES ROUTES

### Routes publiques (pas besoin de token)
```bash
# Vérifier que le server répond
curl http://localhost:4000/
curl http://localhost:4000/health

# Voir les cours (depuis MongoDB)
curl http://localhost:4000/api/courses

# Voir les cours depuis MySQL
curl http://localhost:4000/api/courses/mysql
```

### Créer un compte et se connecter
```bash
# Signup
curl -X POST http://localhost:4000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'

# Réponse:
# {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}

# Copier le token pour les prochaines requêtes
TOKEN="votre_token_ici"

# Récupérer le profil
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:4000/api/auth/me

# Voir mes interactions
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:4000/api/interactions/me

# Enregistrer une interaction
curl -X POST http://localhost:4000/api/interactions/record \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "course": "65a1234567890abc",
    "action": "view"
  }'

# Obtenir les recommandations
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:4000/api/recommendations
```

---

## 🌐 TESTER LE FRONTEND

### Ouvrir le navigateur
```
http://localhost:5173/
```

### Actions à tester
1. ✅ Cliquer sur "Sign Up" → Créer un compte
2. ✅ Se connecter
3. ✅ Voir le Dashboard
4. ✅ Naviguer vers "Courses"
5. ✅ Cliquer sur un cours → Voir détails
6. ✅ Cliquer "Enroll Now" → Vérifier l'interaction
7. ✅ Naviguer vers "For You" (Recommendations)
8. ✅ Cliquer Logout

---

## 🐛 DÉBOGUER LES PROBLÈMES

### MongoDB ne répond pas
```bash
# Vérifier que MongoDB est en cours d'exécution
mongosh

# Si pas installé localement, vérifiez MONGODB_URI
# Devrait être: mongodb://127.0.0.1:27017/learning
```

### MySQL ne marche pas
```bash
# Vérifier le container
docker ps
docker logs mysql-container

# Relancer le container
docker-compose restart mysql

# Vérifier la connection
docker exec mysql-container mysql -u root -proot -e "SELECT 1;"
```

### Backend ne démarre pas
```bash
# Vérifier les erreurs dans le terminal
# Chercher "Connected to MongoDB" et "Server running on port 4000"

# Si erreur "config.mysql is undefined":
# ✅ Déjà corrigé! Assurez-vous d'avoir mis à jour config.ts

# Si erreur JWT_SECRET:
# Vérifiez que .env a JWT_SECRET configuré
```

### Frontend n'accède pas au backend
```bash
# Vérifier VITE_API_BASE_URL dans frontend/.env
# Devrait être: http://localhost:4000

# Vérifier les logs du navigateur (F12 → Console)
```

### Routes protégées retournent 401
```bash
# Le token a expiré ou est invalide
# Reconnectez-vous pour obtenir un nouveau token

# Vérifiez que le token est dans le header:
# Authorization: Bearer <token>
```

---

## 📊 VÉRIFICATION POST-DÉMARRAGE

Tous les éléments suivants doivent être ✅:

- [ ] Backend démarre sans erreur
- [ ] Frontend accessible sur http://localhost:5173
- [ ] Signup/Login fonctionne
- [ ] Cours affichés dans la liste
- [ ] Interaction enregistrée au clic
- [ ] Recommandations générées
- [ ] Détails course accessible
- [ ] Logout fonctionne
- [ ] MySQL connecté (optionnel, pour getCoursesFromMySQL)

---

## 🎓 PROCHAINES ÉTAPES

### Ajouter des données
```bash
# Seed MongoDB avec des données
cd backend
npm run seed
```

### Importer des cours depuis MySQL
```bash
# Les données sont dans database/mysql/seed.sql
# Importez-les avec:
docker exec mysql-container mysql -u root -proot smartlearn < database/mysql/seed.sql
```

### Déployer en production
- [ ] Changer JWT_SECRET vers une clé aléatoire longue
- [ ] Configurer MongoDB Atlas
- [ ] Configurer une vraie base MySQL
- [ ] Ajouter des variables d'env de production
- [ ] Build le frontend: `npm run build`
- [ ] Déployer sur un serveur (Heroku, AWS, DigitalOcean, etc.)

---

## 📞 SUPPORT

Si vous rencontrez un problème:
1. Vérifiez les logs du terminal
2. Consultez [AUDIT_REPORT.md](./AUDIT_REPORT.md) pour tous les changements
3. Vérifiez que toutes les dépendances sont installées
4. Assurez-vous que les ports 4000 et 5173 sont libres

---

**Bon développement! 🚀**
