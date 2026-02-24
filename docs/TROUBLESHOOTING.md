# 🔧 TROUBLESHOOTING - GUIDE DE DÉPANNAGE

## 🆘 Problème: Le backend ne démarre pas

### ❌ Erreur: `Cannot find module 'dotenv'`
```bash
cd backend
npm install
npm run dev
```

### ❌ Erreur: `ECONNREFUSED 127.0.0.1:27017`
**Cause:** MongoDB n'est pas en cours d'exécution
```bash
# Vérifier MongoDB
mongosh

# Si MongoDB n'est pas installé, modifier .env:
# MONGODB_URI=mongodb://127.0.0.1:27017/learning
# Ou utiliser MongoDB Atlas
```

### ❌ Erreur: `config.mysql is undefined`
**Cause:** config.ts n'a pas la config MySQL
**Vérification:** Ouvrez `backend/src/config.ts`
- Doit contenir la section `mysql:` avec host, port, user, password, database
- ✅ **Déjà corrigé dans cet audit**

### ❌ Erreur: `Missing required env var: JWT_SECRET`
```bash
# Vérifier backend/.env contient:
JWT_SECRET=dev-secret-key-change-in-production-12345678
```

### ❌ Erreur: Port 4000 déjà utilisé
```bash
# Option 1: Changer le port
# Modifier .env: PORT=5000

# Option 2: Tuer le processus (Windows)
netstat -ano | findstr :4000
taskkill /PID <PID> /F

# Option 3: Tuer le processus (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 4000).OwningProcess | Stop-Process -Force
```

### ❌ Erreur: `TypeError: Cannot read properties of undefined (reading 'mysql')`
**Cause:** config.ts n'exporte pas correctement mysql
**Vérification:**
```typescript
// Doit être dans config.ts:
export const config: AppConfig = {
  // ...
  mysql: {
    host: process.env.MYSQL_HOST || 'localhost',
    port: Number(process.env.MYSQL_PORT || 3306),
    user: process.env.MYSQL_USER || 'root',
    password: process.env.MYSQL_PASSWORD || 'root',
    database: process.env.MYSQL_DATABASE || 'smartlearn'
  }
};
```

---

## 🆘 Problème: Le frontend ne démarre pas

### ❌ Erreur: `Cannot find module './pages/CourseDetailPage'`
**Cause:** CourseDetailPage.tsx n'existe pas
**Vérification:**
```bash
ls frontend/src/pages/CourseDetailPage.tsx
```
- ✅ **Fichier créé dans cet audit**

### ❌ Erreur: `VITE_API_BASE_URL is not defined`
```bash
# Vérifier frontend/.env contient:
VITE_API_BASE_URL=http://localhost:4000
```

### ❌ Erreur: Port 5173 déjà utilisé
```bash
# Tuer le processus (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process -Force

# Ou vite choisira automatiquement un autre port
```

### ❌ Erreur: `from-primary-600 is not a valid CSS class`
**Cause:** Tailwind n'a pas la couleur `primary`
**Vérification:** Ouvrir `frontend/tailwind.config.js`
- Doit contenir:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        600: '#2563eb', // ou votre couleur
      }
    }
  }
}
```

---

## 🆘 Problème: Signup/Login ne fonctionne pas

### ❌ Erreur 500 lors du signup
```bash
# Vérifier les logs du backend terminal
# Chercher: "Connected to MongoDB"

# Tester directement:
curl -X POST http://localhost:4000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

### ❌ Erreur `User.findOne is not a function`
**Cause:** Le modèle User n'est pas chargé correctement
**Vérification:**
```bash
# Dans backend/src/controllers/authController.ts
# Doit importer: import User from '../models/User';
```

### ❌ Erreur `Invalid token` lors du login
```bash
# Vérifier que JWT_SECRET est le même dans .env
# Vérifier que le token est passé correctement:
Authorization: Bearer <token>
```

### ❌ Impossible de se connecter mais signup fonctionne
**Cause:** Password hash incorrect
```bash
# Vérifier que bcrypt est installé:
npm list bcrypt

# Vérifier authController.ts a:
const ok = await bcrypt.compare(password, user.passwordHash);
```

---

## 🆘 Problème: Les routes protégées retournent 401

### ❌ GET /api/auth/me retourne 401
```bash
# Vérifier:
1. Token valide (non expiré)
2. Header Authorization: "Bearer <token>"
3. Middleware auth.ts a été mis à jour

# Tester:
TOKEN="your_token_here"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:4000/api/auth/me
```

### ❌ GET /api/recommendations retourne 401
**Cause:** Même que ci-dessus + userId pas trouvé
**Vérification:**
```typescript
// Dans middleware/auth.ts, doit vérifier:
if (!payload.sub) return res.status(401).json({ error: 'Invalid token: missing user ID' });
```

---

## 🆘 Problème: Les interactions/recommandations ne marchent pas

### ❌ POST /api/interactions/record retourne 400
```bash
# Vérifier les paramètres:
# - course: string (ID valide)
# - action: "view" | "enroll" | "progress" | "complete"
# - progress: optional number 0-100
# - metadata: optional object

curl -X POST http://localhost:4000/api/interactions/record \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "course": "65a1234567890abc",
    "action": "view"
  }'
```

### ❌ GET /api/recommendations retourne un tableau vide
**Cause:** Pas assez d'interactions pour les recommandations
```bash
# Enregistrer quelques interactions d'abord:
curl -X POST http://localhost:4000/api/interactions/record \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course": "...", "action": "view"}'

# Puis tester les recommandations
```

---

## 🆘 Problème: Les cours ne s'affichent pas

### ❌ GET /api/courses retourne `[]` (tableau vide)
**Cause:** Pas de cours dans MongoDB
**Solution:**
```bash
# Lancer le seed script
cd backend
npm run seed

# Ou manuellement, ajouter dans MongoDB:
db.courses.insertOne({
  title: "Learn React",
  description: "Learn React from basics",
  tags: ["react", "javascript", "frontend"],
  level: "beginner"
})
```

### ❌ GET /api/courses/mysql retourne une erreur
**Cause:** MySQL n'est pas configuré correctement
```bash
# Vérifier:
1. MySQL est en cours d'exécution: docker ps | grep mysql
2. La base de données existe: docker exec mysql-container mysql -u root -proot -e "SELECT 1 FROM courses;"
3. Les données sont importées: docker exec mysql-container mysql -u root -proot smartlearn < database/mysql/seed.sql

# Si erreur "table 'smartlearn.courses' doesn't exist":
# Importer le schéma:
docker exec mysql-container mysql -u root -proot smartlearn < database/mysql/schema.sql
```

---

## 🆘 Problème: Les types TypeScript ne matchent pas

### ❌ Erreur: `Type 'string' is not assignable to type 'ObjectId'`
**Cause:** Conflit entre string et ObjectId MongoDB
**Solution:**
```typescript
// Utiliser string dans les routes/API
const courseId: string = req.body.course;

// Mongoose convertira automatiquement en ObjectId
const interaction = new Interaction({ 
  user: userId, // ObjectId automatique
  course: courseId, // String converti en ObjectId
  action: req.body.action
});
```

### ❌ Erreur: `Property 'userId' does not exist on type 'Request'`
**Cause:** Interface AuthRequest non correctement typée
**Vérification:**
```typescript
// Dans authController.ts, doit avoir:
import { AuthRequest } from '../middleware/auth';

export async function getMe(req: AuthRequest, res: Response) {
  const userId = req.userId; // ✅ Maintenant disponible
}
```

---

## 🆘 Problème: La navigation ne fonctionne pas

### ❌ Cliquer sur un cours n'ouvre pas la page détail
**Cause:** Route `/courses/:id` n'existe pas
**Vérification:**
- [ ] `frontend/src/main.tsx` a la route
- [ ] `frontend/src/pages/CourseDetailPage.tsx` existe
- [ ] L'import dans main.tsx est correct
- ✅ **Tous vérifiés dans cet audit**

### ❌ Impossible d'accéder à `http://localhost:5173/courses/123`
**Cause:** ProtectedRoute ou router non configuré
**Vérification:**
```typescript
// main.tsx doit avoir:
<Route
  path="/courses/:id"
  element={
    <ProtectedRoute>
      <CourseDetailPage />
    </ProtectedRoute>
  }
/>
```

---

## 🆘 Problème: Les styles ne s'affichent pas correctement

### ❌ Couleurs du gradient ne s'affichent pas
```bash
# Vérifier tailwind.config.js a la couleur primary
# Sinon ajouter:
theme: {
  extend: {
    colors: {
      primary: {
        600: '#2563eb'
      }
    }
  }
}

# Rebuild:
npm run dev
```

### ❌ Les animations Framer Motion ne marchent pas
```bash
# Vérifier que framer-motion est installé:
npm list framer-motion

# Sinon:
npm install framer-motion
```

---

## 🧪 Tests rapides pour vérifier l'installation

```bash
# 1. Backend respond?
curl http://localhost:4000/health

# 2. Frontend charge?
curl http://localhost:5173

# 3. Database connectée?
curl http://localhost:4000/api/courses

# 4. Auth fonctionne?
curl -X POST http://localhost:4000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"Test1234"}'

# Utiliser test_api.ps1 pour tous les tests à la fois
./test_api.ps1
```

---

## 📞 Ressources

- [AUDIT_REPORT.md](./AUDIT_REPORT.md) - Rapport d'audit complet
- [CHECKLIST_DEMARRAGE.md](./CHECKLIST_DEMARRAGE.md) - Guide étape-par-étape
- [CORRECTIONS_APPLIQUEES.md](./CORRECTIONS_APPLIQUEES.md) - Snippets de code
- [test_api.ps1](./test_api.ps1) - Tests automatisés

---

**Toujours pas résolu? Cherchez l'erreur exacte ici ou dans [AUDIT_REPORT.md](./AUDIT_REPORT.md) 🔍**
