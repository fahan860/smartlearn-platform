# LearnHub Frontend

Modern, professional React + TypeScript frontend for the LearnHub learning recommendation platform.

## Features

- 🎨 **Modern UI** - Clean, responsive design with Tailwind CSS
- ⚡ **Fast** - Built with Vite for lightning-fast development
- 🔐 **Authentication** - JWT-based auth with protected routes
- 📱 **Responsive** - Mobile-first design that works on all devices
- ✨ **Animations** - Smooth transitions using Framer Motion
- 🎯 **Type-Safe** - Full TypeScript support

## Quick Start

### Prerequisites

- Node.js 18+
- Backend API running on `http://localhost:4000`

### Installation

```bash
cd frontend
npm install
```

### Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Default config connects to `http://localhost:4000` for the backend API.

### Development

```bash
npm run dev
```

Opens at http://localhost:3000 with hot reload enabled.

### Build for Production

```bash
npm run build
```

Production files output to `dist/`.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── CourseCard.tsx
│   │   ├── Layout.tsx
│   │   └── ProtectedRoute.tsx
│   ├── contexts/         # React contexts
│   │   └── AuthContext.tsx
│   ├── pages/            # Page components
│   │   ├── LandingPage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── SignupPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── CoursesPage.tsx
│   │   └── RecommendationsPage.tsx
│   ├── services/         # API client
│   │   └── api.ts
│   ├── index.css         # Global styles
│   └── main.tsx          # App entry point
├── public/               # Static assets
└── index.html
```

## Pages

- **Landing** (`/`) - Hero section, features, CTAs
- **Login** (`/login`) - User authentication
- **Sign Up** (`/signup`) - Account creation
- **Dashboard** (`/dashboard`) - User stats, recent courses, recommendations
- **Courses** (`/courses`) - Browse catalog with search and filters
- **Recommendations** (`/recommendations`) - AI-powered personalized suggestions

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Router** - Navigation
- **Axios** - HTTP client
- **React Hot Toast** - Notifications
- **Lucide React** - Icons

## API Integration

The app communicates with the backend API at `http://localhost:4000`:

- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login
- `GET /api/courses` - List courses (with filters)
- `GET /api/recommendations` - Get personalized recommendations
- `POST /api/interactions/record` - Track user interactions
- `GET /api/interactions/me` - Get user's interaction history

JWT tokens are stored in `localStorage` and automatically included in requests.

## Design System

### Colors
- Primary: Blue gradient (`from-primary-600 to-indigo-600`)
- Success: Green
- Warning: Orange
- Error: Red

### Typography
- Font: Inter (Google Fonts)
- Sizes: Responsive with Tailwind utilities

### Components
- Cards with hover effects
- Gradient buttons with animations
- Form inputs with focus states
- Loading spinners
- Toast notifications

## Notes

- Backend must be running before starting frontend
- Protected routes redirect to login if not authenticated
- Email normalization handled by backend
- JWT expires after 7 days
