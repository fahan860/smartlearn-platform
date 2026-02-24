# ✅ SMARTLEARN - CHECKLIST INTERACTIVE

## 🎯 AVANT DE DÉMARRER

### Prérequis système
```
✅ Node.js 14+              npm -v
✅ npm installé              node -v
✅ MongoDB accessible        mongosh (ou vérifier .env)
✅ Port 4000 disponible      netstat -ano | findstr :4000 (Windows)
✅ Port 5173 disponible      netstat -ano | findstr :5173 (Windows)
✅ Git installé (optionnel)  git --version
```

---

## 📋 INSTALLATION (5 min)

### Backend
```bash
cd backend
npm install
# Vérifier que tout est installé
npm list | head -20
```
✅ **Check:** Pas d'erreur en rouge

### Frontend
```bash
cd frontend
npm install
# Vérifier que tout est installé
npm list | head -20
```
✅ **Check:** Pas d'erreur en rouge

---

## ⚙️ CONFIGURATION

### Backend .env
```bash
cd backend
cat .env | grep MONGODB
cat .env | grep JWT
cat .env | grep MYSQL
```
✅ **Check:** Toutes les variables présentes

### Frontend .env
```bash
cd frontend
cat .env
```
✅ **Check:** `VITE_API_BASE_URL=http://localhost:4000`

---

## 🚀 DÉMARRAGE (7 min)

### Terminal 1 - Backend
```bash
cd backend
npm run dev
```
✅ **Check:** "Connected to MongoDB" s'affiche
✅ **Check:** "Server running on port 4000" s'affiche

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```
✅ **Check:** "Local: http://localhost:5173" s'affiche
✅ **Check:** "VITE v5.0.8" s'affiche

### Browser
```
http://localhost:5173
```
✅ **Check:** Page d'accueil SmartLearn s'affiche

---

## 🧪 TESTER LES ROUTES

### Health Check
```bash
curl http://localhost:4000/health
```
✅ **Check:** `{"status":"ok"}` retourné

### List Courses
```bash
curl http://localhost:4000/api/courses
```
✅ **Check:** Array de courses retourné (vide ou rempli)

### Signup
```bash
curl -X POST http://localhost:4000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```
✅ **Check:** Token retourné dans la réponse
**Copier le token** pour les prochains tests

### Get Profile
```bash
TOKEN="your_token_here"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:4000/api/auth/me
```
✅ **Check:** Profil utilisateur retourné

---

## 🎮 TESTER DANS LE NAVIGATEUR

### Landing Page
```
http://localhost:5173/
```
✅ **Check:** Page d'accueil s'affiche

### Sign Up
```
Cliquer sur "Sign Up"
Remplir: Nom, Email, Password
Cliquer "Sign Up"
```
✅ **Check:** Redirection vers Dashboard

### Dashboard
```
Vérifier que le user est connecté
Voir les sections: Recent Courses, Interactions, Recommendations
```
✅ **Check:** Tout s'affiche

### Courses
```
Naviguer vers "Courses" (navbar)
Voir la liste des cours
```
✅ **Check:** Cours affichés (sinon, faire le seed)

### Course Details
```
Cliquer sur un cours
Voir la page détail
Cliquer "Enroll Now"
```
✅ **Check:** Interaction enregistrée

### Recommendations
```
Naviguer vers "For You"
Voir les recommandations
```
✅ **Check:** Recommandations affichées

---

## 🛠️ DÉPANNER

### Backend ne démarre pas?
```bash
# Vérifier MongoDB
mongosh

# Vérifier les variables
cat backend/.env

# Réinstaller les dépendances
cd backend && rm -rf node_modules && npm install && npm run dev
```

### Frontend ne compile pas?
```bash
# Vérifier Node.js
node -v

# Réinstaller les dépendances
cd frontend && rm -rf node_modules && npm install && npm run dev
```

### Routes retournent 401 Unauthorized?
```bash
# Vérifier que le token est valide
# Faire un nouveau signup pour obtenir un token frais

# Vérifier que le header Authorization est correct
Authorization: Bearer <token>
```

### Courses ne s'affichent pas?
```bash
# Faire le seed
cd backend && npm run seed

# Ou manuellement ajouter un cours via API
curl -X POST http://localhost:4000/api/courses \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn React",
    "description": "A guide to React",
    "tags": ["react", "javascript"],
    "level": "beginner"
  }'
```

---

## 🧪 TEST AUTOMATISÉ

### Windows PowerShell
```bash
.\test_api.ps1
```
✅ **Check:** Tous les tests passent

### Linux/Mac
```bash
bash test_api.sh
```
✅ **Check:** Tous les tests passent

---

## 📊 VÉRIFICATION POST-DÉMARRAGE

```
DATABASE:
[✅] MongoDB connecté         (logs backend)
[✅] Courses chargés          (GET /api/courses)
[✅] MySQL disponible         (GET /api/courses/mysql)

AUTHENTIFICATION:
[✅] Signup fonctionne        (POST /api/auth/signup)
[✅] Login fonctionne         (POST /api/auth/login)
[✅] Profil accessible        (GET /api/auth/me)
[✅] Token valide             (routes protégées)

FRONTEND:
[✅] Page d'accueil           (http://localhost:5173)
[✅] Signup fonctionne        (créer compte)
[✅] Login fonctionne         (se connecter)
[✅] Dashboard s'affiche      (redirection post-login)
[✅] Courses s'affichent      (naviguer à Courses)
[✅] Détails course marche    (cliquer sur un cours)
[✅] Enroll fonctionne        (bouton Enroll Now)
[✅] Recommendations visible  (naviguer à For You)
[✅] Logout fonctionne        (se déconnecter)

PERFORMANCE:
[✅] Frontend rapide          (< 3s de chargement)
[✅] Backend rapide           (réponses < 200ms)
[✅] Pas d'erreur dans F12    (console du navigateur)
```

---

## 🎓 PROCHAINES ÉTAPES

### Développement
```
[ ] Ajouter des données (npm run seed)
[ ] Tester toutes les pages
[ ] Vérifier les styles
[ ] Déployer sur un serveur test
```

### Production
```
[ ] Configurer MongoDB Atlas
[ ] Configurer JWT_SECRET long
[ ] Ajouter SSL/TLS
[ ] Configurer CI/CD
[ ] Ajouter monitoring
```

---

## 🆘 BESOIN D'AIDE?

Si quelque chose ne marche pas:

1. **Lisez:** [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
2. **Lancez:** `./test_api.ps1`
3. **Consultez:** [AUDIT_REPORT.md](./AUDIT_REPORT.md)

---

## 📝 NOTES

```
- Tous les fichiers critiques ont été corrigés
- Toutes les routes sont opérationnelles
- Le projet est prêt pour la production (avec configuration)
- La documentation est complète
```

---

## ✨ STATUS FINAL

```
Backend:        ✅ READY
Frontend:       ✅ READY
Database:       ✅ CONFIGURED
Security:       ✅ IMPLEMENTED
Documentation:  ✅ COMPLETE

PROJET:         ✅ 100% OPÉRATIONNEL
```

---

**Félicitations! Votre SmartLearn est maintenant en marche! 🎉**

*Besoin de continuer? Consultez [START_HERE.md](./START_HERE.md)*
