# ⚡ Quick Reference Card

## 🚀 Start Commands

```bash
# Full Stack (Automated)
start.bat              # Windows batch
.\start.ps1           # PowerShell

# Backend Only
cd backend
npm run dev           # Port 4000

# Frontend Only  
cd frontend
npm run dev           # Port 3000
```

## 🌐 URLs

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:4000
- **Health Check:** http://localhost:4000/health

## 🔑 Demo Account

```
Email: demo@example.com
Password: Password123!
```
*(Available after running `npm run seed` in backend)*

## 📁 Key Files

### Backend
```
backend/
├── .env                    # Config (create from .env.example)
├── src/server.ts           # Entry point
├── src/app.ts              # Express app
├── src/config.ts           # Central config
├── src/controllers/        # Route handlers
├── src/models/             # Mongoose schemas
├── src/routes/             # API routes
└── src/services/           # Business logic
```

### Frontend
```
frontend/
├── .env                    # Config (create from .env.example)
├── src/main.tsx            # Entry point
├── src/pages/              # Page components
├── src/components/         # Reusable UI
├── src/contexts/           # React contexts
└── src/services/api.ts     # API client
```

## 🔧 Environment Variables

### Backend (.env)
```env
MONGODB_URI=mongodb+srv://...
JWT_SECRET=your-secret-key
PORT=4000
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:4000
```

## 📡 API Endpoints

### Public
```
POST /api/auth/signup       # Create account
POST /api/auth/login        # Login
GET  /api/courses           # List courses
```

### Protected (Requires JWT)
```
GET  /api/recommendations   # Get recommendations
POST /api/interactions/record    # Track interaction
GET  /api/interactions/me   # Get my interactions
POST /api/courses           # Create course
```

## 🎨 Main Pages

| Route | Auth | Description |
|-------|------|-------------|
| `/` | No | Landing page |
| `/login` | No | Login form |
| `/signup` | No | Registration |
| `/dashboard` | Yes | User dashboard |
| `/courses` | Yes | Course catalog |
| `/recommendations` | Yes | Personalized suggestions |

## 🛠️ Common Commands

### Backend
```bash
npm run dev      # Start dev server
npm run build    # Compile TypeScript
npm start        # Run production
npm run seed     # Seed database
npm test         # Run tests
```

### Frontend
```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

## 🐛 Quick Fixes

### "MONGODB_URI not set"
```bash
cd backend
cp .env.example .env
# Edit .env with your MongoDB URI
```

### "Cannot connect to MongoDB"
- Check MongoDB Atlas IP whitelist
- Verify connection string
- Check username/password

### "Network Error" in frontend
- Ensure backend is running (port 4000)
- Check frontend .env has correct API URL

### "Unauthorized" errors
- Token expired → Logout and login again
- Clear localStorage in browser DevTools

## 📊 Project Stats

- **Backend:** Express + TypeScript + MongoDB
- **Frontend:** React + TypeScript + Vite
- **Total Files:** 40+ source files
- **Lines of Code:** ~3500+ LOC
- **Build Time:** < 6 seconds
- **Dependencies:** 280+ packages

## ✅ Feature Checklist

- [x] User authentication (JWT)
- [x] Course catalog with search/filters
- [x] Interaction tracking
- [x] AI-powered recommendations
- [x] User dashboard with stats
- [x] Responsive design
- [x] Smooth animations
- [x] Error handling
- [x] Production-ready Docker
- [x] Test suite

## 🎯 Test Checklist

1. [ ] Sign up new account
2. [ ] Login with credentials
3. [ ] View dashboard stats
4. [ ] Browse courses catalog
5. [ ] Search for courses
6. [ ] Filter by level/tag
7. [ ] Click course (tracks view)
8. [ ] Click enroll (tracks enroll)
9. [ ] Check updated stats
10. [ ] View recommendations

## 📝 Important Notes

- JWT tokens expire in 7 days
- Emails are automatically lowercased
- Passwords must be 8+ characters
- Rate limit: 100 requests per 15 minutes
- Recommendations improve with interactions
- Cold start users see popular courses

## 🔗 Documentation

- `README.md` - Project overview
- `SETUP.md` - Detailed setup guide
- `FEATURES.md` - Visual & feature documentation
- `backend/README.md` - Backend API docs
- `frontend/README.md` - Frontend docs

## 🎉 Success Indicators

✅ Backend shows: "Connected to MongoDB"
✅ Backend shows: "Server running on port 4000"
✅ Frontend shows: "Local: http://localhost:3000"
✅ Can create account and login
✅ Dashboard shows stats
✅ Can browse and search courses
✅ Recommendations display

---

**Quick Reference for LearnHub Platform** 📚
