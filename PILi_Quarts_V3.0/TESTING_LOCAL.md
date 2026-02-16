# PILi Quarts - Local Testing Guide

## 🧪 Testing Locally Before Deployment

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git

---

## 🚀 Quick Start - Local Testing

### 1. Setup Backend

```bash
cd workspace-modern/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your values

# Initialize database
python scripts/db_migrate.py init

# Seed demo data
python scripts/seed_db.py

# Run backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend running at**: http://localhost:8000  
**API Docs**: http://localhost:8000/docs

---

### 2. Setup Frontend

```bash
cd workspace-modern/frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit .env.local:
# VITE_API_URL=http://localhost:8000
# VITE_WS_URL=ws://localhost:8000

# Run frontend
npm run dev
```

**Frontend running at**: http://localhost:5173

---

## ✅ Testing Checklist

### Backend Tests

```bash
cd workspace-modern/backend

# Run all tests
pytest

# Run with coverage
pytest --cov=modules --cov-report=html

# Run specific test types
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only

# View coverage report
start htmlcov/index.html  # Windows
```

### API Tests (Manual)

1. **Health Check**
   - Visit: http://localhost:8000/health
   - Expected: `{"status": "healthy"}`

2. **API Info**
   - Visit: http://localhost:8000/api/info
   - Expected: Module information

3. **PILI Chat**
   - POST to http://localhost:8000/api/pili/chat
   - Body: `{"message": "Hola PILI", "context": {}}`
   - Expected: AI response

4. **WebSocket**
   - Connect to: ws://localhost:8000/ws/pili/test-user-123
   - Send: `{"message": "Test"}`
   - Expected: Real-time response

### Frontend Tests

1. **Home Page**
   - Visit: http://localhost:5173
   - Expected: App loads

2. **PILI Chat Component**
   - Test chat interface
   - Send messages
   - Check WebSocket connection status

3. **API Integration**
   - Check network tab
   - Verify API calls to localhost:8000
   - Check for errors

---

## 🔍 Common Issues & Solutions

### Backend Issues

**Issue**: Database connection error
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Check DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/pili_quarts
```

**Issue**: Import errors
```bash
# Make sure you're in venv
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: Migration errors
```bash
# Check current revision
python scripts/db_migrate.py current

# Reset and re-run
python scripts/db_migrate.py downgrade
python scripts/db_migrate.py upgrade
```

### Frontend Issues

**Issue**: API connection refused
```bash
# Check backend is running
curl http://localhost:8000/health

# Check VITE_API_URL in .env.local
VITE_API_URL=http://localhost:8000
```

**Issue**: WebSocket connection failed
```bash
# Check VITE_WS_URL in .env.local
VITE_WS_URL=ws://localhost:8000

# Check browser console for errors
```

**Issue**: Build errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Performance Testing

### Load Testing (Optional)

```bash
# Install locust
pip install locust

# Create locustfile.py (example)
# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

### Database Performance

```bash
# Check query performance
psql pili_quarts

# Analyze queries
EXPLAIN ANALYZE SELECT * FROM users;

# Check indexes
\di
```

---

## 🌐 Deployment Platforms Comparison

### Option 1: Supabase (Backend) + Vercel (Frontend)

**Pros**:
- ✅ Managed PostgreSQL
- ✅ Built-in Auth
- ✅ File Storage
- ✅ Realtime subscriptions
- ✅ Auto-scaling
- ✅ Free tier

**Cons**:
- ❌ Vendor lock-in
- ❌ Limited customization
- ❌ Costs scale with usage

**Setup**:
```bash
# Frontend to Vercel
cd workspace-modern/frontend
vercel deploy

# Backend to Supabase
# Use Supabase CLI or dashboard
supabase init
supabase db push
```

---

### Option 2: Railway (Full Stack)

**Pros**:
- ✅ Deploy backend + frontend + DB
- ✅ Simple configuration
- ✅ Git-based deployment
- ✅ Free $5/month credit

**Cons**:
- ❌ Costs after free tier
- ❌ Less features than Supabase

**Setup**:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

---

### Option 3: Render (Full Stack)

**Pros**:
- ✅ Free tier for web services
- ✅ Managed PostgreSQL
- ✅ Auto-deploy from Git
- ✅ SSL certificates

**Cons**:
- ❌ Free tier spins down after inactivity
- ❌ Slower cold starts

**Setup**:
```bash
# Create render.yaml
# Push to GitHub
# Connect Render to repo
```

---

### Option 4: Self-Hosted (VPS)

**Pros**:
- ✅ Full control
- ✅ Predictable costs
- ✅ No vendor lock-in

**Cons**:
- ❌ Manual setup
- ❌ Maintenance overhead
- ❌ Security responsibility

**Providers**:
- DigitalOcean ($6/month)
- Linode ($5/month)
- Vultr ($6/month)

---

## 🎯 Recommended Approach

### For PILi Quarts:

**Development**:
- Local testing (as above)

**Staging**:
- Frontend: Vercel (free)
- Backend: Railway or Render (free tier)
- Database: Supabase (free tier)

**Production**:
- Frontend: Vercel ($20/month)
- Backend: Railway ($10-20/month)
- Database: Supabase ($25/month)

**Total**: ~$55-65/month

---

## 📝 Deployment Files Needed

### For Vercel (Frontend)
- ✅ `vercel.json` (created)
- ✅ `.env.example`
- ✅ `package.json`

### For Supabase (Backend)
- ✅ `supabase/config.toml` (created)
- ✅ Database migrations
- ✅ Edge functions (if using)

### For Railway/Render
- `railway.json` or `render.yaml`
- `Procfile`
- Environment variables

---

## 🔐 Environment Variables for Production

### Frontend (.env.production)
```env
VITE_API_URL=https://your-backend.railway.app
VITE_WS_URL=wss://your-backend.railway.app
VITE_APP_NAME=PILi Quarts
VITE_ENABLE_WEBSOCKET=true
```

### Backend (.env.production)
```env
DATABASE_URL=postgresql://user:pass@db.supabase.co/postgres
GEMINI_API_KEY=your-key
SECRET_KEY=your-secret-key
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend.vercel.app
```

---

## 🚀 Next Steps

1. **Test Locally** ✅ (Do this now)
   - Run backend
   - Run frontend
   - Test all features
   - Run test suite

2. **Fix Issues** (If any)
   - Debug errors
   - Optimize performance
   - Update documentation

3. **Choose Platform**
   - Evaluate options
   - Create accounts
   - Setup projects

4. **Deploy Staging**
   - Deploy to staging
   - Test in production-like environment
   - Gather feedback

5. **Deploy Production**
   - Final testing
   - Deploy to production
   - Monitor performance

---

**Start testing locally now! 🧪**
