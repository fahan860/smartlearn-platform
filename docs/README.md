# 🚀 LearnHub - Complete Project Guide

A modern learning recommendation platform with AI-powered personalized course suggestions.

## 📁 Project Structure

```
workspace/
├── backend/          # Express + TypeScript API
│   ├── src/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── scripts/
│   └── tests/
└── frontend/         # React + TypeScript UI
    └── src/
        ├── components/
        ├── contexts/
        ├── pages/
        └── services/
```

## 🎯 Quick Start

### Prerequisites

- Node.js 18+ installed
- MongoDB Atlas account (or local MongoDB)
- Two terminal windows

### Step 1: Setup Backend

```bash
# Terminal 1 - Backend
cd backend

# Install dependencies (if not already done)
npm install

# Create .env file from example
cp .env.example .env

# Edit .env and add your MongoDB URI and JWT secret:
# MONGODB_URI=mongodb+srv://your-connection-string
# JWT_SECRET=your-random-secret-key-here
# PORT=4000

# (Optional) Seed database with demo data
npm run seed

# Start backend server
npm run dev
```

Backend runs at **http://localhost:4000**

### Step 2: Setup Frontend

```bash
# Terminal 2 - Frontend
cd frontend

# Install dependencies (already done)
# npm install

# Start frontend dev server
npm run dev
```

Frontend runs at **http://localhost:3000**

## 🌐 Using the Application

1. **Open browser** → http://localhost:3000
2. **Landing page** → Click "Sign Up"
3. **Create account** → Enter name, email, password (min 8 chars)
4. **Auto-redirect** → Dashboard with stats and courses
5. **Browse courses** → Click "Courses" to see catalog
6. **Get recommendations** → Click "For You" for personalized suggestions
7. **Interact** → Click courses to view, enroll tracks your progress

### Demo Account (if you ran seed)

- Email: `demo@example.com`
- Password: `Password123!`

## ✨ Features

### Backend (Port 4000)
- ✅ JWT authentication with bcrypt password hashing
- ✅ MongoDB Atlas integration with Mongoose
- ✅ Course catalog with search & filters
- ✅ User interaction tracking (view, enroll, progress, complete)
- ✅ AI-powered recommendation engine with ML placeholder
- ✅ RESTful API with validation & error handling
- ✅ Docker support for production deployment

### Frontend (Port 3000)
- ✅ Modern landing page with animations
- ✅ User authentication (login/signup)
- ✅ Protected routes with JWT
- ✅ User dashboard with stats
- ✅ Course catalog with real-time search & filters
- ✅ Personalized recommendations page
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Smooth animations with Framer Motion
- ✅ Toast notifications
- ✅ Professional UI with Tailwind CSS

## 🛠️ Tech Stack

### Backend
- Express.js + TypeScript
- MongoDB + Mongoose
- JWT + bcrypt
- Express Validator
- Helmet, CORS, Rate Limiting

### Frontend
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS
- Framer Motion
- React Router
- Axios
- React Hot Toast

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login

### Courses
- `GET /api/courses` - List all courses
- `GET /api/courses/:id` - Get single course
- `POST /api/courses` - Create course (auth required)

### Interactions
- `POST /api/interactions/record` - Record interaction (auth required)
- `GET /api/interactions/me` - Get my interactions (auth required)

### Recommendations
- `GET /api/recommendations` - Get personalized recommendations (auth required)

## 🧪 Testing

### Backend Tests
```bash
cd backend
npm test
```

### Manual Testing Flow
1. Sign up new account
2. Browse courses catalog
3. Click on courses (tracks "view")
4. Click "Enroll Now" (tracks "enroll")
5. Check dashboard stats update
6. View recommendations page (personalized based on interactions)

## 🐳 Docker Deployment (Optional)

```bash
cd backend
docker build -t learnhub-backend .
docker run -p 4000:4000 --env-file .env learnhub-backend
```

## 🔧 Development Commands

### Backend
```bash
npm run dev      # Start dev server with hot reload
npm run build    # Compile TypeScript to JavaScript
npm start        # Run production build
npm run seed     # Seed database with demo data
npm test         # Run tests
```

### Frontend
```bash
npm run dev      # Start dev server with hot reload
npm run build    # Build for production
npm run preview  # Preview production build
```

## 🎨 Design Highlights

- **Color Scheme**: Blue/Indigo gradient primary colors
- **Typography**: Inter font from Google Fonts
- **Animations**: Smooth page transitions and hover effects
- **Responsive**: Mobile-first design with breakpoints
- **Accessibility**: Focus states and semantic HTML

## 🔐 Security Features

- Password hashing with bcrypt (12 rounds)
- JWT tokens with 7-day expiration
- Protected API routes
- Request validation
- Rate limiting
- Helmet security headers
- CORS configuration

## 📈 How Recommendations Work

1. **Interaction Tracking**: System records every course view, enrollment, progress update
2. **Tag-Based Analysis**: Analyzes tags from courses you've interacted with
3. **Weighted Scoring**: Different actions have different weights (complete > enroll > view)
4. **Recency Decay**: Recent interactions weighted more heavily
5. **Cold Start**: New users see popular courses until they build history
6. **ML Placeholder**: Optional ML service integration for advanced recommendations

## 🚀 Production Checklist

- [ ] Set strong JWT_SECRET in production
- [ ] Use MongoDB Atlas with proper security
- [ ] Enable SSL/TLS for API
- [ ] Set up environment variables properly
- [ ] Configure CORS for your domain
- [ ] Set up monitoring and logging
- [ ] Run security audits (`npm audit`)
- [ ] Set up CI/CD pipeline
- [ ] Configure CDN for frontend assets
- [ ] Set up backup strategy for database

## 📞 Support

For issues or questions:
1. Check README files in backend/ and frontend/ folders
2. Review API documentation in backend/README.md
3. Check browser console for frontend errors
4. Check terminal output for backend errors

## 🎉 Success!

You now have a fully functional, production-ready learning platform with:
- Modern, professional UI
- Secure authentication
- Personalized AI recommendations
- Scalable architecture
- MongoDB cloud integration

**Happy Learning! 🎓**
