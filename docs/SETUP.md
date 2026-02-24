# 🎓 LearnHub - Setup & Run Instructions

## ✅ Prerequisites Checklist

Before starting, ensure you have:

- [x] Node.js 18+ installed (`node --version`)
- [x] npm installed (`npm --version`)
- [ ] MongoDB Atlas account OR local MongoDB running
- [ ] Backend dependencies installed (`cd backend && npm install`)
- [ ] Frontend dependencies installed (`cd frontend && npm install`)

## 🚀 Method 1: Automated Start (Easiest)

### Windows

**Option A: Using Batch File**
```cmd
start.bat
```

**Option B: Using PowerShell**
```powershell
.\start.ps1
```

This will:
1. Check/create .env files
2. Start backend on port 4000
3. Start frontend on port 3000
4. Open in separate terminal windows

## 🔧 Method 2: Manual Start (Step-by-Step)

### Step 1: Configure Backend

```bash
cd backend
```

Create `.env` file (copy from `.env.example`):
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/learning
JWT_SECRET=your-super-secret-random-string-here
PORT=4000
```

**Important**: 
- Replace `MONGODB_URI` with your actual MongoDB connection string
- Generate a strong `JWT_SECRET` (use a random 32+ character string)

### Step 2: Seed Database (Optional but Recommended)

```bash
npm run seed
```

This creates:
- Demo user: `demo@example.com` / `Password123!`
- 3 sample courses
- 1 learning path

### Step 3: Start Backend

```bash
npm run dev
```

✅ Backend should now be running at `http://localhost:4000`

You should see:
```
Connected to MongoDB
Server running on port 4000
```

### Step 4: Start Frontend (New Terminal)

Open a **new terminal window**:

```bash
cd frontend
npm run dev
```

✅ Frontend should now be running at `http://localhost:3000`

You should see:
```
VITE v5.x.x ready in xxx ms

➜  Local:   http://localhost:3000/
```

### Step 5: Open in Browser

Navigate to: **http://localhost:3000**

## 📱 Using the Application

### First Time Setup

1. **Landing Page** → You'll see the homepage
2. **Click "Sign Up"** in the top right
3. **Create Account**:
   - Name: Your name
   - Email: Your email
   - Password: Min 8 characters
4. **Auto Login** → Redirects to dashboard

### Using Demo Account

If you ran `npm run seed`:
- Email: `demo@example.com`
- Password: `Password123!`

### Main Features

1. **Dashboard** (`/dashboard`)
   - View your learning stats
   - See recommended courses
   - Quick access to popular courses

2. **Courses** (`/courses`)
   - Browse all available courses
   - Search by title, description, tags
   - Filter by level (beginner/intermediate/advanced)
   - Filter by tag (python, data-science, ml, etc.)

3. **Recommendations** (`/recommendations`)
   - AI-powered personalized suggestions
   - Based on your interaction history
   - Updates as you interact with courses

4. **Interactions**
   - Click any course → Records "view"
   - Click "Enroll Now" → Records "enroll"
   - Your interactions improve recommendations

## 🔍 Testing the System

### Test Flow

1. **Sign up** with a new account
2. **Browse courses** - Click on 2-3 courses
3. **Check dashboard** - See your stats update
4. **View recommendations** - See personalized suggestions
5. **Enroll in course** - Click "Enroll Now" button
6. **Check stats** - See enrollment count increase

### Verify Backend API

Test endpoints directly:

```bash
# Health check
curl http://localhost:4000/health

# List courses (public)
curl http://localhost:4000/api/courses

# Login (get JWT token)
curl -X POST http://localhost:4000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"Password123!"}'
```

## 🐛 Troubleshooting

### Backend won't start

**Problem**: "MONGODB_URI not set"
- **Solution**: Create `.env` file in `backend/` folder with MongoDB connection string

**Problem**: "Mongo connection error"
- **Solution**: Check your MongoDB Atlas connection string is correct
- Ensure your IP is whitelisted in MongoDB Atlas
- Check username/password are correct

**Problem**: Port 4000 already in use
- **Solution**: Change PORT in `.env` to another port (e.g., 4001)
- Update frontend `.env` to match: `VITE_API_BASE_URL=http://localhost:4001`

### Frontend won't start

**Problem**: "Cannot find module"
- **Solution**: Run `npm install` in frontend folder

**Problem**: Port 3000 already in use
- **Solution**: Vite will automatically suggest another port (usually 3001)

**Problem**: "Network Error" when trying to login/signup
- **Solution**: Ensure backend is running on port 4000
- Check `.env` has correct API URL

### Authentication issues

**Problem**: "Unauthorized" errors
- **Solution**: Token expired, logout and login again
- Clear browser localStorage and try again

**Problem**: Can't login with correct credentials
- **Solution**: Check backend logs for errors
- Ensure password is at least 8 characters

### Build errors

**Problem**: TypeScript errors during build
- **Solution**: Run `npm run build` to see specific errors
- Ensure all dependencies installed: `npm install`

## 📦 Production Build

### Backend

```bash
cd backend
npm run build
npm start
```

### Frontend

```bash
cd frontend
npm run build
npm run preview  # Test production build locally
```

Deploy `dist/` folder to your hosting service.

## 🌍 Environment Variables

### Backend (.env)

```env
# Required
MONGODB_URI=mongodb+srv://...          # MongoDB connection string
JWT_SECRET=random-secret-key           # JWT signing secret

# Optional
PORT=4000                              # Server port (default: 4000)
ML_SERVICE_URL=http://ml-service:5000  # ML service URL (optional)
NODE_ENV=development                   # Environment (development/production)
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:4000  # Backend API URL
```

## 📊 Project Status

✅ **Completed Features**:
- User authentication (signup/login)
- JWT token management
- Protected routes
- Course catalog with search/filters
- User dashboard with stats
- Interaction tracking
- AI-powered recommendations
- Responsive design
- Smooth animations
- Error handling
- MongoDB integration
- Docker support
- Testing setup

## 🎯 Next Steps (Optional Enhancements)

- [ ] Add course detail page
- [ ] Implement learning paths
- [ ] Add user profile page
- [ ] Course progress tracking
- [ ] Real ML model integration
- [ ] Add course ratings/reviews
- [ ] Implement course creation UI
- [ ] Add social features
- [ ] Email notifications
- [ ] Advanced analytics

## 📝 Notes

- Backend uses JWT tokens that expire in 7 days
- Emails are automatically normalized (lowercase, trimmed)
- Passwords are hashed with bcrypt (12 rounds)
- Frontend stores JWT in localStorage
- Recommendations improve as you interact with more courses
- Cold start users see popular courses until they build interaction history

## 🎉 Success Indicators

You'll know everything is working when:

1. ✅ Backend shows "Connected to MongoDB"
2. ✅ Backend shows "Server running on port 4000"
3. ✅ Frontend shows "Local: http://localhost:3000"
4. ✅ You can sign up and create an account
5. ✅ Dashboard shows your stats
6. ✅ You can browse and search courses
7. ✅ Recommendations page shows personalized courses

## 💬 Need Help?

Check these in order:

1. **Browser Console** (F12) - Look for JavaScript errors
2. **Backend Terminal** - Look for server errors
3. **Network Tab** (F12) - Check API requests/responses
4. **README files** in backend/ and frontend/ folders
5. **.env files** - Ensure they're configured correctly

---

**Enjoy your learning platform! 🚀**
